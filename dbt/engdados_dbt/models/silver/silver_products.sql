with src as (
    select
        ingestion_date,
        payload
    from staging.products_raw
),

latest as (
    select max(ingestion_date) as max_ingestion_date
    from src
),

filtered as (
    select s.*
    from src s
    join latest l
      on s.ingestion_date = l.max_ingestion_date
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
    from filtered
)

select *
from typed
where product_id is not null
