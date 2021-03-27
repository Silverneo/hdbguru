nearby_mrt_sql = """
with tmp AS
(
    SELECT 
        name,
        latitude,
        longitude,
        ST_DistanceSphere(
          ST_SetSRID(ST_Point({}, {}), 4326),
          geom
        ) as distance_to_target
    FROM api.tbl_mrt_lrt_addr_info 
    ORDER BY distance_to_target
)

SELECT *
FROM tmp
WHERE distance_to_target <= 2000
LIMIT {}
"""

nearby_hawker_sql = """
with tmp AS
(
    SELECT 
        name,
        latitude,
        longitude,
        ST_DistanceSphere(
          ST_SetSRID(ST_Point({}, {}), 4326),
          geom
        ) as distance_to_target
    FROM api.tbl_hawker_addr_info 
    ORDER BY distance_to_target
)

SELECT *
FROM tmp
WHERE distance_to_target <= 2000
LIMIT {}
"""

nearby_mall_sql = """
with tmp AS
(
    SELECT 
        name,
        latitude,
        longitude,
        ST_DistanceSphere(
          ST_SetSRID(ST_Point({}, {}), 4326),
          geom
        ) as distance_to_target
    FROM api.tbl_mall_addr_info 
    ORDER BY distance_to_target
)

SELECT *
FROM tmp
WHERE distance_to_target <= 2000
LIMIT {}
"""

nearby_school_sql = """
with tmp AS
(
    SELECT 
        school_name as name,
        latitude,
        longitude,
        ST_DistanceSphere(
          ST_SetSRID(ST_Point({}, {}), 4326),
          geom
        ) as distance_to_target
    FROM api.tbl_school_info 
    ORDER BY distance_to_target
)

SELECT *
FROM tmp
WHERE distance_to_target <= 2000
LIMIT {}
"""

nearby_hdb_sql = """
SELECT *
FROM 
(
    SELECT 
        hdb_id,
        town,
        block,
        street_name,
        address,
        building,
        ST_DistanceSphere(
          ST_SetSRID(ST_Point({}, {}), 4326),
          geom
        ) as distance_to_target,
        postal_code,
        latitude,
        longitude
    FROM api.tbl_hdb_addr_info 
    ORDER BY distance_to_target
    LIMIT {}
) AS hdb_addr_tbl
INNER JOIN
(
    SELECT *
    FROM api.vw_stats_hdb_surroundings
) AS hdb_surround_tbl
ON hdb_addr_tbl.hdb_id = hdb_surround_tbl.hdb_id
INNER JOIN
(
    SELECT 
        hdb_id,
        CAST(AVG(price_psf) AS INT) AS avg_price_psf,
        lease_commence_date,
        flat_type,
        CAST(AVG(floor_area_sqm) AS INT) AS floor_area_sqm
    FROM api.tbl_hdb_resale_price
    WHERE month > date('{}-01-01')
    GROUP BY hdb_id,lease_commence_date, flat_type
) AS hdb_price_tbl
ON hdb_addr_tbl.hdb_id = hdb_price_tbl.hdb_id
ORDER BY hdb_addr_tbl.distance_to_target
"""