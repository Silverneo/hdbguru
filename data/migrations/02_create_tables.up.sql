CREATE TABLE IF NOT EXISTS api.TBL_HDB_RESAL_PRICE (
    MONTH DATE NOT NULL,
    TOWN VARCHAR(50) NOT NULL,
    BLOCK VARCHAR(10) NOT NULL,
    STREET_NAME VARCHAR(300) NOT NULL,
    FLAT_TYPE VARCHAR(50) NULL,
    FLAT_MODEL VARCHAR(50) NULL,
    LEASE_COMMENCE_DATE INT NULL,
    FLOOR_AREA_SQM REAL NULL,
    RESALE_PRICE REAL NULL,
    STOREY_RANGE_FROM SMALLINT NULL,
    STOREY_RANGE_TO SMALLINT NULL
);

CREATE TABLE IF NOT EXISTS api.TBL_HDB_ADDR_INFO (
    TOWN VARCHAR(50) NOT NULL,
    BLOCK VARCHAR(10) NOT NULL,
    STREET_NAME VARCHAR(300) NOT NULL,
    POSTAL_CODE VARCHAR(10) NOT NULL,
    ADDRESS VARCHAR(300) NOT NULL,
    BUILDING VARCHAR(100) NOT NULL,
    LATITUDE REAL NOT NULL,
    LONGITUDE REAL NOT NULL,
    X REAL NOT NULL,
    Y REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS api.TBL_HDB_PROP_INFO (
    TOWN VARCHAR(50) NOT NULL,
    BLOCK VARCHAR(10) NOT NULL,
    STREET_NAME VARCHAR(300) NOT NULL,
    MAX_FLOOR_LVL INT NOT NULL,
    YEAR_COMPLETED INT NOT NULL,
    RESIDENTIAL INT,
    COMMERCIAL INT,
    MARKET_HAWKER INT,
    MISCELLANEOUS INT,
    MULTISTOREY_CARPARK INT,
    PRECINCT_PAVILION INT,
    TOTAL_DWELLING_UNITS INT,
    CNT_1ROOM_SOLD INT,
    CNT_2ROOM_SOLD INT,
    CNT_3ROOM_SOLD INT,
    CNT_4ROOM_SOLD INT,
    CNT_5ROOM_SOLD INT,
    EXEC_SOLD INT,
    MULTIGEN_SOLD INT,
    STUDIO_APARTMENT_SOLD INT,
    CNT_1ROOM_RENTAL INT,
    CNT_2ROOM_RENTAL INT,
    CNT_3ROOM_RENTAL INT,
    OTHER_ROOM_RENTAL INT
);

CREATE TABLE IF NOT EXISTS api.TBL_SCHOOL_INFO (
    SCHOOL_NAME VARCHAR(100) NOT NULL,
    URL_ADDRESS VARCHAR(100),
    ADDRESS VARCHAR(100) NOT NULL,
    POSTAL_CODE VARCHAR(10) NOT NULL,
    TELEPHONE_NO VARCHAR(50),
    TELEPHONE_NO_2 VARCHAR(50),
    FAX_NO VARCHAR(50),
    FAX_NO_2 VARCHAR(50),
    EMAIL_ADDRESS VARCHAR(50),
    MRT_DESC VARCHAR(100),
    BUS_DESC VARCHAR(300),
    PRINCIPAL_NAME VARCHAR(50),
    VISIONSTATEMENT_DESC VARCHAR(5000),
    MISSIONSTATEMENT_DESC VARCHAR(5000),
    PHILOSOPHY_CULTURE_ETHOS VARCHAR(5000),
    DGP_CODE VARCHAR(20),
    ZONE_CODE VARCHAR(10),
    TYPE_CODE VARCHAR(50),
    NATURE_CODE VARCHAR(50),
    SESSION_CODE VARCHAR(50),
    MAINLEVEL_CODE VARCHAR(50),
    SAP_IND INT,
    AUTONOMOUS_IND INT,
    GIFTED_IND INT,
    IP_IND INT,
    MOTHERTONGUE1_CODE VARCHAR(10),
    MOTHERTONGUE2_CODE VARCHAR(10),
    MOTHERTONGUE3_CODE VARCHAR(10),
    SPECIAL_SDP_OFFERED VARCHAR(5000),
    ROAD_NAME VARCHAR(100) NOT NULL,
    LATITUDE REAL NOT NULL,
    LONGITUDE REAL NOT NULL,
    X REAL NOT NULL,
    Y REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS api.TBL_MRT_LRT_ADDR_INFO (
    NAME VARCHAR(50) NOT NULL,
    TYPE VARCHAR(10) NOT NULL,
    LATITUDE REAL NOT NULL,
    LONGITUDE REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS api.TBL_SMKT_ADDR_INFO (
NAME VARCHAR(100) NOT NULL,
DESCRIPTION	VARCHAR(50) NOT NULL,
BLOCK	VARCHAR(10) NOT NULL,
STREET_NAME	VARCHAR(50) NOT NULL,
UNIT_NO	VARCHAR(10),
POSTAL_CODE	VARCHAR(10) NOT NULL,
LATITUDE	REAL NOT NULL,
LONGITUDE	REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS api.TBL_HAWKER_ADDR_INFO (
NAME VARCHAR(100) NOT NULL,
LATITUDE	REAL NOT NULL,
LONGITUDE	REAL NOT NULL
);