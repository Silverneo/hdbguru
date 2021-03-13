-- SUPERMARKET
with temp AS (
SELECT t1.HDB_ID, smkt.DESCRIPTION, ST_DistanceSphere(t1.geom, smkt.geom) AS DISTANCE
FROM api.tbl_hdb_addr_info t1 LEFT JOIN api.tbl_smkt_addr_info smkt
ON ST_DistanceSphere(t1.geom, smkt.geom) <= 2000
)
SELECT * INTO api.TBL_STATS_HDB_SUPERMARKET FROM (
SELECT HDB_ID, DESCRIPTION AS MARKET_ID, DISTANCE AS MARKET_DIST,
SUM(CASE WHEN (DISTANCE > 1000) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MARKET_CNT_1KM_2KM,
SUM(CASE WHEN (DISTANCE <= 1000 AND DISTANCE > 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MARKET_CNT_500_1KM,
SUM(CASE WHEN (DISTANCE <= 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MARKET_CNT_WTH_500
FROM temp
ORDER BY HDB_ID, DISTANCE
) t;

-- SCHOOL
with temp AS (
SELECT t1.HDB_ID, t2.SCHOOL_NAME, ST_DistanceSphere(t1.geom, t2.geom) AS DISTANCE
FROM api.tbl_hdb_addr_info t1 LEFT JOIN api.tbl_school_info t2
ON ST_DistanceSphere(t1.geom, t2.geom) <= 2000
AND t2.MAINLEVEL_CODE IN ('PRIMARY', 'MIXED LEVELS')
)
SELECT * INTO api.TBL_STATS_HDB_SCHOOL FROM (
SELECT HDB_ID, SCHOOL_NAME, DISTANCE AS SCHOOL_DIST,
SUM(CASE WHEN (DISTANCE > 1000) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS SCHOOL_CNT_1KM_2KM,
SUM(CASE WHEN (DISTANCE <= 1000 AND DISTANCE > 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS SCHOOL_CNT_500_1KM,
SUM(CASE WHEN (DISTANCE <= 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS SCHOOL_CNT_WTH_500
FROM temp
ORDER BY HDB_ID, DISTANCE
) t;

-- HAWKER CENTER
with temp AS (
SELECT t1.HDB_ID, t2.NAME, ST_DistanceSphere(t1.geom, t2.geom) AS DISTANCE
FROM api.tbl_hdb_addr_info t1 LEFT JOIN api.tbl_hawker_addr_info t2
ON ST_DistanceSphere(t1.geom, t2.geom) <= 2000
)
SELECT * INTO api.TBL_STATS_HDB_HAWKER FROM (
SELECT HDB_ID, NAME AS HAWKER_NAME, DISTANCE AS HAWKER_DISTANCE,
SUM(CASE WHEN (DISTANCE > 1000) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS HAWKER_CNT_1KM_2KM,
SUM(CASE WHEN (DISTANCE <= 1000 AND DISTANCE > 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS HAWKER_CNT_500_1KM,
SUM(CASE WHEN (DISTANCE <= 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS HAWKER_CNT_WTH_500
FROM temp
ORDER BY HDB_ID, DISTANCE
) t;

-- MRT/LRT
with temp AS (
SELECT t1.HDB_ID, t2.NAME, ST_DistanceSphere(t1.geom, t2.geom) AS DISTANCE
FROM api.tbl_hdb_addr_info t1 LEFT JOIN api.tbl_mrt_lrt_addr_info t2
ON ST_DistanceSphere(t1.geom, t2.geom) <= 2000
)
SELECT * INTO api.TBL_STATS_HDB_STATION FROM (
SELECT HDB_ID, NAME AS STATION_NAME, DISTANCE AS STATION_DISTANCE,
SUM(CASE WHEN (DISTANCE > 1000) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS STATION_CNT_1KM_2KM,
SUM(CASE WHEN (DISTANCE <= 1000 AND DISTANCE > 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS STATION_CNT_500_1KM,
SUM(CASE WHEN (DISTANCE <= 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS STATION_CNT_WTH_500
FROM temp
ORDER BY HDB_ID, DISTANCE
) t;

-- MALL
with temp AS (
SELECT t1.HDB_ID, t2.NAME, ST_DistanceSphere(t1.geom, t2.geom) AS DISTANCE
FROM api.tbl_hdb_addr_info t1 LEFT JOIN api.tbl_mrt_lrt_addr_info t2
ON ST_DistanceSphere(t1.geom, t2.geom) <= 2000
)
SELECT * INTO api.TBL_STATS_HDB_MALL FROM (
SELECT HDB_ID, NAME AS MALL_NAME, DISTANCE AS MALL_DISTANCE,
SUM(CASE WHEN (DISTANCE > 1000) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MALL_CNT_1KM_2KM,
SUM(CASE WHEN (DISTANCE <= 1000 AND DISTANCE > 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MALL_CNT_500_1KM,
SUM(CASE WHEN (DISTANCE <= 500) THEN 1 ELSE 0 END) OVER (PARTITION BY HDB_ID) AS MALL_CNT_WTH_500
FROM temp
ORDER BY HDB_ID, DISTANCE
) t;

CREATE OR REPLACE VIEW api.VW_STATS_HDB_SURROUNDINGS AS (
	with t1 AS (
	SELECT DISTINCT HDB_ID, HAWKER_CNT_1KM_2KM, HAWKER_CNT_500_1KM, HAWKER_CNT_WTH_500 FROM api.tbl_stats_hdb_hawker
	),
	t2 AS (
	SELECT DISTINCT HDB_ID, SCHOOL_CNT_1KM_2KM, SCHOOL_CNT_500_1KM, SCHOOL_CNT_WTH_500 FROM api.tbl_stats_hdb_school
	),
	t3 AS (
	SELECT DISTINCT HDB_ID, STATION_CNT_1KM_2KM, STATION_CNT_500_1KM, STATION_CNT_WTH_500 FROM api.tbl_stats_hdb_station
	),
	t4 AS (
	SELECT DISTINCT HDB_ID, MARKET_CNT_1KM_2KM, MARKET_CNT_500_1KM, MARKET_CNT_WTH_500 FROM api.tbl_stats_hdb_supermarket
	),
	t5 AS (
	SELECT DISTINCT HDB_ID, MALL_CNT_1KM_2KM, MALL_CNT_500_1KM, MALL_CNT_WTH_500 FROM api.tbl_stats_hdb_mall
	)
	SELECT t1.*,
	SCHOOL_CNT_1KM_2KM, SCHOOL_CNT_500_1KM, SCHOOL_CNT_WTH_500,
	STATION_CNT_1KM_2KM, STATION_CNT_500_1KM, STATION_CNT_WTH_500,
	MARKET_CNT_1KM_2KM, MARKET_CNT_500_1KM, MARKET_CNT_WTH_500,
	MALL_CNT_1KM_2KM, MALL_CNT_500_1KM, MALL_CNT_WTH_500
	FROM t1
	LEFT JOIN t2 ON t1.HDB_ID = t2.HDB_ID
	LEFT JOIN t3 ON t1.HDB_ID = t3.HDB_ID
	LEFT JOIN t4 ON t1.HDB_ID = t4.HDB_ID
	LEFT JOIN t5 ON t1.HDB_ID = t5.HDB_ID
);
