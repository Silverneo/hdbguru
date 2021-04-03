import pathlib 
from datetime import datetime
import hashlib
import argparse

import requests
from sqlalchemy import create_engine
import pandas as pd

def get_latest_data(data_url):
    
    headers = {
      'Cookie': '__cfduid=d6631c09624d16591b25d24f75c538ebc1612666474'
    }

    response = requests.request("GET", data_url, headers=headers)

    df = pd.DataFrame(response.json()['result']['records'])
    if len(df) > 0:
        df = df.drop(
            ["remaining_lease",'_id'], axis=1
        )
    return df

def clean_n_insert(df, db):

    df.dropna(inplace=True)

    df['resale_price'] = df['resale_price'].astype('float')
    df['floor_area_sqm'] = df['floor_area_sqm'].astype('float')

    df['hdb_id'] = (df['town']+df['block']+df['street_name']).apply(lambda x: hashlib.md5(x.encode()).hexdigest()[:8])

    df['price_psm'] = df['resale_price'] / df['floor_area_sqm']
    df['price_psf'] = df['price_psm'] / 10.764

    df['month'] = df['month'].apply(lambda x: x+"-01")

    df['storey_range_from'] = df['storey_range'].apply(lambda x: x.split('TO')[0])
    df['storey_range_to'] = df['storey_range'].apply(lambda x: x.split('TO')[1])

    df = df.drop(columns={'storey_range'})

    df.to_sql('tbl_hdb_resale_price', con=db, schema='api', if_exists='append', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--dbaddr", default="127.0.0.1:5432", help="the db address.")
    args = parser.parse_args()

    # need to use postgresql:// instead of postgres://
    db_string = "postgresql://hgadmin:pwd123456@{}/hdbguru".format(args.dbaddr)
    db = create_engine(db_string)

    hdb_resale_url = """https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee&limit=100000&filters={"month":"%s-%s"}"""

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")

    df = get_latest_data(hdb_resale_url % (year, month))

    if len(df) > 0:
        clean_n_insert(df, db)
