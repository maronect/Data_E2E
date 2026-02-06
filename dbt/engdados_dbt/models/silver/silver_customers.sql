with src as (
    select
        ingestion_date,
        payload
    from staging.customers_raw
),

typed as (
    select
        ingestion_date,
        payload ->> 'customer_id' as customer_id,
        payload ->> 'name'        as name,
        payload ->> 'email'       as email,
        payload ->> 'state'       as state,
        (payload ->> 'created_at')::timestamp as created_at
    from src
)

select *
from typed
where customer_id is not null