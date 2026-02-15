with orders as (
    select *
    from {{ ref('silver_orders') }}
)

select
    order_id,
    customer_id,
    product_id,
    order_ts,
    payment_method,
    quantity,
    unit_price,
    order_total,
    ingestion_date
from orders
