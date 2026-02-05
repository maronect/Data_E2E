import os
from datetime import date
import boto3
from botocore.client import Config

def get_s3_client():
    endpoint = os.getenv("MINIO_ENDPOINT")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    if not endpoint or not access_key or not secret_key:
        raise RuntimeError("Missing MinIO env vars: MINIO_ENDPOINT/MINIO_ACCESS_KEY/MINIO_SECRET_KEY")

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

def ensure_bucket(s3, bucket: str):
    try:
        s3.head_bucket(Bucket=bucket)
    except Exception:
        s3.create_bucket(Bucket=bucket)

def upload_bytes(s3, bucket: str, key: str, content: bytes, content_type: str = "text/csv"):
    s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)

def dated_key(prefix: str, ingestion_date: date, filename: str) -> str:
    return f"{prefix}/dt={ingestion_date.isoformat()}/{filename}"
