select
    oi.id as order_item_id,
    o.order_id,
    o.user_id,
    o.status as order_status,
    date(o.created_at) as order_date_id, 
    o.created_at as order_created_at,
    oi.product_id,
    p.category as product_category,
    p.department as product_department,
    p.brand as product_brand,
    oi.sale_price,
    p.cost,
    (oi.sale_price - p.cost) as gross_margin,
    p.distribution_center_id,
    oi.created_at as item_created_at,
    oi.shipped_at,
    oi.delivered_at,
    oi.returned_at

from {{ ref('stg_order_items') }} oi
join {{ ref('stg_orders') }} o
  on oi.order_id = o.order_id
join {{ ref('stg_products') }} p
  on oi.product_id = p.id

