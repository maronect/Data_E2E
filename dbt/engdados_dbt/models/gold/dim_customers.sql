with customers as (
    select *
    from {{ ref('silver_customers') }}
)

select
    customer_id,
    name,
    email,
    state,
    created_at
from customers