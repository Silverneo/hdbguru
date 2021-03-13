ALTER TABLE api.tbl_hdb_addr_info ADD COLUMN HDB_ID VARCHAR(8);
UPDATE api.tbl_hdb_addr_info SET HDB_ID = SUBSTR(MD5(TOWN || BLOCK || STREET_NAME), 1, 8);
ALTER TABLE api.tbl_hdb_addr_info ADD PRIMARY KEY (HDB_ID);
