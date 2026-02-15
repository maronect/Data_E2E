with products as (
    select *
    from {{ ref('silver_products') }}
)

select
    product_id,
    title,
    category,
    price,
    rating_rate,
    rating_count
from products
