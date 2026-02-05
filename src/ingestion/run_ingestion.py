import os
import io
import random
import requests
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
from datetime import date, datetime, time

from src.common.minio_client import get_s3_client, ensure_bucket, upload_bytes, dated_key
from src.common.db import insert_json_rows

fake = Faker("pt_BR")

def fetch_products():
    url = os.getenv("PRODUCTS_API_URL", "https://fakestoreapi.com/products")
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    products = r.json()
    # Keep only key fields (good practice: don't store everything blindly)
    cleaned = []
    for p in products:
        cleaned.append({
            "product_id": p.get("id"),
            "title": p.get("title"),
            "category": p.get("category"),
            "price": float(p.get("price")) if p.get("price") is not None else None,
            "rating_rate": (p.get("rating") or {}).get("rate"),
            "rating_count": (p.get("rating") or {}).get("count"),
        })
    return cleaned

def gen_customers(n: int):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": f"C{100000+i}",
            "name": fake.name(),
            "email": fake.email(),
            "state": fake.estado_sigla(),
            "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
        })
    return customers

def gen_orders(customers: list[dict], products: list[dict], n: int, ingestion_date: date):
    orders = []
    start_dt = datetime.combine(ingestion_date, time.min)
    end_dt = datetime.combine(ingestion_date, time.max)

    for i in range(n):
        c = random.choice(customers)
        p = random.choice(products)
        qty = random.randint(1, 4)
        price = p["price"] if p["price"] is not None else round(random.uniform(10, 300), 2)

        orders.append({
            "order_id": f"O{ingestion_date.strftime('%Y%m%d')}{10000+i}",
            "customer_id": c["customer_id"],
            "product_id": p["product_id"],
            "quantity": qty,
            "unit_price": price,
            "order_total": round(qty * price, 2),
            "order_ts": fake.date_time_between(start_date=start_dt, end_date=end_dt).isoformat(),
            "payment_method": random.choice(["pix", "credit_card", "debit_card", "boleto"]),
        })
    return orders


def to_csv_bytes(rows: list[dict]) -> bytes:
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def main():
    load_dotenv()

    ingestion_date = date.today()

    bucket = os.getenv("MINIO_BUCKET", "lake")
    s3 = get_s3_client()
    ensure_bucket(s3, bucket)

    print(f"[INFO] ingestion_date={ingestion_date.isoformat()} bucket={bucket}")

    # 1) External source: products API
    print("[INFO] fetching products from API...")
    products = fetch_products()
    print(f"[INFO] products fetched: {len(products)}")

    # 2) Internal-like sources: customers + orders (fake)
    customers = gen_customers(n=200)
    orders = gen_orders(customers, products, n=800, ingestion_date=ingestion_date)

    # 3) Upload RAW files to lake
    print("[INFO] uploading raw files to MinIO...")
    prod_key = dated_key("raw/products", ingestion_date, "products.csv")
    cust_key = dated_key("raw/customers", ingestion_date, "customers.csv")
    ord_key  = dated_key("raw/orders", ingestion_date, "orders.csv")

    upload_bytes(s3, bucket, prod_key, to_csv_bytes(products))
    upload_bytes(s3, bucket, cust_key, to_csv_bytes(customers))
    upload_bytes(s3, bucket, ord_key,  to_csv_bytes(orders))

    print(f"[OK] uploaded: s3://{bucket}/{prod_key}")
    print(f"[OK] uploaded: s3://{bucket}/{cust_key}")
    print(f"[OK] uploaded: s3://{bucket}/{ord_key}")

    # 4) Insert into Postgres staging as JSONB
    print("[INFO] inserting into Postgres staging...")
    inserted_products = insert_json_rows("staging.products_raw", ingestion_date, products) if False else 0
    inserted_customers = insert_json_rows("staging.customers_raw", ingestion_date, customers)
    inserted_orders = insert_json_rows("staging.orders_raw", ingestion_date, orders)

    print(f"[OK] inserted customers_raw: {inserted_customers}")
    print(f"[OK] inserted orders_raw: {inserted_orders}")

    print("[DONE] ingestion pipeline completed.")

if __name__ == "__main__":
    main()
