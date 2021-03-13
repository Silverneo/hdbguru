import pathlib
import pandas as pd
import numpy as np

from .utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_json(data_dir / "supermarket_info_001.json")
    assert (
        df.shape[0] == df["DESCRIPTION"].unique().size
    ), "DESCRIPTION is not unique, pls check"

    return df


def format_data(df):

    df["POSTAL_CODE"] = format_sg_postal(df["POSTCODE"])

    df = df.rename(columns={"BLK_HOUSE": "BLOCK", "STR_NAME": "STREET_NAME"})

    df[["LATITUDE", "LONGITUDE"]] = df["LatLng"].str.split(",", expand=True)

    df["LATITUDE"] = df["LATITUDE"].astype(float)
    df["LONGITUDE"] = df["LONGITUDE"].astype(float)

    return df[
        [
            "NAME",
            "DESCRIPTION",
            "BLOCK",
            "STREET_NAME",
            "UNIT_NO",
            "POSTAL_CODE",
            "LATITUDE",
            "LONGITUDE",
        ]
    ]


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/onemap-theme-supermarkets"))
    df = format_data(df)

    dump(df, pathlib.Path("data/_processed/TBL_SMKT_ADDR_INFO.csv.gzip"))

