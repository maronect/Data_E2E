with src as (
    select
        ingestion_date,
        payload
    from staging.customers_raw
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
        payload ->> 'customer_id' as customer_id,
        payload ->> 'name'        as name,
        payload ->> 'email'       as email,
        payload ->> 'state'       as state,
        (payload ->> 'created_at')::timestamp as created_at
    from filtered
)

select *
from typed
where customer_id is not null
