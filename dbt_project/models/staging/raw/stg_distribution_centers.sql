select
    id,
    name,
    latitude,
    longitude,
    distribution_center_geom
from {{ source('ecomm', 'distribution_centers') }}

