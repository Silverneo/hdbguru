import pathlib
import pandas as pd
import numpy as np

from .utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_json(data_dir / 'hawker_centre_info_001.json')

    return df


def format_data(df):

    df = df.rename(columns={'ADDRESS_MYENV': 'ADDRESS', 'ADDRESSPOSTALCODE': "POSTAL_CODE"})

    df['POSTAL_CODE'] = format_sg_postal(df['POSTAL_CODE'].astype('Int64'))

    df = df[['NAME', 'DESCRIPTION', 'STATUS', 'NO_OF_FOOD_STALLS', 'NO_OF_MARKET_STALLS', "REGION", "POSTAL_CODE", "ADDRESS", 'LATITUDE', 'LONGITUDE']]

    for col in ['STATUS', 'REGION']:
        df[col] = df[col].str.upper()

    for col in ['NO_OF_FOOD_STALLS', 'NO_OF_MARKET_STALLS']:
        df[col] = df[col].astype('Int64')

    df = df[df['LATITUDE'].notnull()].reset_index(drop=True)

    return df


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/onnemap-theme-hawkercentre"))
    df = format_data(df)

    dump(df, pathlib.Path("data/_processed/TBL_HAWKER_ADDR_INFO.csv.gzip"))

