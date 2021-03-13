COPY api.TBL_HDB_RESAL_PRICE FROM '/tmp/data/_processed/TBL_HDB_RESALE_PRICE.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_HDB_ADDR_INFO FROM '/tmp/data/_processed/TBL_HDB_ADDR_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_HDB_PROP_INFO FROM '/tmp/data/_processed/TBL_HDB_PROP_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_SCHOOL_INFO FROM '/tmp/data/_processed/TBL_SCHOOL_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_MRT_LRT_ADDR_INFO FROM '/tmp/data/_processed/TBL_MRT_LRT_ADDR_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_SMKT_ADDR_INFO FROM '/tmp/data/_processed/TBL_SMKT_ADDR_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_HAWKER_ADDR_INFO FROM '/tmp/data/_processed/TBL_HAWKER_ADDR_INFO.csv.gzip' delimiter '|' CSV HEADER;
COPY api.TBL_MALL_ADDR_INFO FROM '/tmp/data/_processed/TBL_MALL_ADDR_INFO.csv.gzip' delimiter '|' CSV HEADER;
