select
    id as distribution_center_id,
    name as distribution_center_name,
    latitude,
    longitude,
    distribution_center_geom
from {{ ref('stg_distribution_centers') }}

