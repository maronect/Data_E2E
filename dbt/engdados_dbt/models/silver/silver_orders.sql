with src as (
    select
        ingestion_date,
        payload
    from staging.orders_raw
),

typed as (
    select
        ingestion_date,
        payload ->> 'order_id'    as order_id,
        payload ->> 'customer_id' as customer_id,
        (payload ->> 'product_id')::int as product_id,
        (payload ->> 'quantity')::int as quantity,
        (payload ->> 'unit_price')::numeric(12,2) as unit_price,
        (payload ->> 'order_total')::numeric(12,2) as order_total,
        (payload ->> 'order_ts')::timestamp as order_ts,
        payload ->> 'payment_method' as payment_method
    from src
)

select *
from typed
where order_id is not null
