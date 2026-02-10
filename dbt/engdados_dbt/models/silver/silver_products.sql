with src as (
    select
        ingestion_date,
        payload
    from staging.products_raw
),

typed as (
    select
        ingestion_date,
        (payload ->> 'product_id')::int as product_id,
        payload ->> 'title' as title,
        payload ->> 'category' as category,
        (payload ->> 'price')::numeric(12,2) as price,
        (payload ->> 'rating_rate')::numeric(5,2) as rating_rate,
        (payload ->> 'rating_count')::int as rating_count
    from src
)

select *
from typed
where product_id is not null
