select
    ii.id as inventory_item_id,

    ii.product_id,
    p.category as product_category,
    p.department as product_department,
    p.brand as product_brand,

    ii.product_distribution_center_id as distribution_center_id,

    ii.cost,
    p.retail_price,

    ii.created_at as inventory_created_at,
    ii.sold_at,

    case
        when ii.sold_at is null then true
        else false
    end as is_in_stock,

    case
        when ii.sold_at is not null then true
        else false
    end as is_sold

from {{ ref('stg_inventory_items') }} ii
left join {{ ref('stg_products') }} p
  on ii.product_id = p.id

