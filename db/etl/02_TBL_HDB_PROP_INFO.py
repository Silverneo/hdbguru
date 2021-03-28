import pandas as pd
import numpy as np
import pathlib
from .utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_csv(data_dir / "hdb-property-information.csv")

    return df


def _convert_town_code_to_name(x):

    d = (
        pd.read_csv("data/_static/HDB_TOWN_CODE_MAP.csv")
        .set_index("TOWN_CODE")["TOWN"]
        .to_dict()
    )

    name = x.replace(d)

    assert name.isnull().sum() == 0, "There are missing town code, pls check"

    return name


def format_data(df):

    df.columns = df.columns.str.upper()

    # Standardize certain column names
    df = df.rename(
        columns={
            "BLK_NO": "BLOCK",
            "STREET": "STREET_NAME",
            "BLDG_CONTRACT_TOWN": "TOWN",
            "1ROOM_SOLD": "CNT_1ROOM_SOLD",
            "2ROOM_SOLD": "CNT_2ROOM_SOLD",
            "3ROOM_SOLD": "CNT_3ROOM_SOLD",
            "4ROOM_SOLD": "CNT_4ROOM_SOLD",
            "5ROOM_SOLD": "CNT_5ROOM_SOLD",
            "1ROOM_RENTAL": "CNT_1ROOM_RENTAL",
            "2ROOM_RENTAL": "CNT_2ROOM_RENTAL",
            "3ROOM_RENTAL": "CNT_3ROOM_RENTAL",
        }
    )

    df["TOWN"] = _convert_town_code_to_name(df["TOWN"])

    df = strip_spaces(df)

    flag_cols = [
        "RESIDENTIAL",
        "COMMERCIAL",
        "MARKET_HAWKER",
        "MISCELLANEOUS",
        "MULTISTOREY_CARPARK",
        "PRECINCT_PAVILION",
    ]

    for x in flag_cols:
        df[x] = np.where(df[x] == "Y", 1, 0)

    _keys = ["TOWN", "BLOCK", "STREET_NAME"]

    df = df[_keys + [x for x in df.columns if x not in _keys]]

    return df


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/hdb-property-information/"))
    df = format_data(df)
    dump(df, pathlib.Path("data/_processed/TBL_HDB_PROP_INFO.csv.gzip"))

