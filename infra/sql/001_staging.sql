CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.orders_raw (
  ingestion_date date NOT NULL,
  payload jsonb NOT NULL,
  ingested_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS staging.customers_raw (
  ingestion_date date NOT NULL,
  payload jsonb NOT NULL,
  ingested_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS staging.products_raw (
  ingestion_date date NOT NULL,
  payload jsonb NOT NULL,
  ingested_at timestamp NOT NULL DEFAULT now()
);"