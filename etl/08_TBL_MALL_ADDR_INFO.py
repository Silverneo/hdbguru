import pandas as pd
import numpy as np

from .utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_csv(data_dir / "TBL_SHOPPING_MALL_ADDR_INFO.csv")
    df = df[df['LATITUDE'].notnull()].reset_index(drop=True)

    assert df.shape[0] == df['NAME'].unique().size, "NAME is not unique, pls check"

    return df


def format_data(df):

    df["NAME"] = df["NAME"].str.upper()
    df = df.replace('NIL', np.nan)

    df["POSTAL_CODE"] = format_sg_postal(df["POSTAL_CODE"])

    return df[["NAME", "BLOCK", "STREET_NAME", "POSTAL_CODE", "ADDRESS", "BUILDING", "LATITUDE", "LONGITUDE", "X", "Y"]]


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_mingxuan"))
    df = format_data(df)

    dump(df, pathlib.Path("data/_processed/TBL_MALL_ADDR_INFO.csv.gzip"))

