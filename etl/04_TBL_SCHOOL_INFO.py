import pathlib
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

from .utils import *
from .one_map_api import query_onemap_api


def get_school_address_info(df):

    # Get address info using OneMap API
    school_addresses = df["ADDRESS"].unique().tolist()
    res = query_onemap_api(school_addresses)

    df_addr = pd.concat([pd.read_json(s) for s in res], ignore_index=True)

    df = df[["SCHOOL_NAME", "ADDRESS"]].copy()
    df["_KEYWORD_"] = df["ADDRESS"]
    df = df[["SCHOOL_NAME", "_KEYWORD_"]].merge(df_addr, how="left", on=["_KEYWORD_"])

    # Add fuzz match score based on school name & search val from OneMap API results
    df["_SCORE_"] = df.apply(
        lambda row: fuzz.ratio(str(row["SCHOOL_NAME"]), str(row["SEARCHVAL"])), axis=1
    )

    # Take the highest score for each school
    df = df.sort_values(["SCHOOL_NAME", "_SCORE_"], ascending=[True, False])
    df = (
        df.groupby(["SCHOOL_NAME"])
        .first()
        .reset_index()
        .drop(["_KEYWORD_", "_SCORE_"], axis=1)
    )

    # Reset school address exceptions which pulled manually
    df_exp = pd.read_csv("data/_static/SCHOOL_ADDR_EXCEPTIONS.csv")

    df = df.set_index(["SCHOOL_NAME"])
    df.update(df_exp.set_index(["SCHOOL_NAME"]))
    df = df.reset_index()

    assert df["LATITUDE"].isnull().sum() == 0, "Missing geo info, pls check"

    return df[["SCHOOL_NAME", "ROAD_NAME", "LATITUDE", "LONGITUDE", "X", "Y"]]


def load_data(data_dir: pathlib.Path):

    df = pd.read_csv(
        data_dir / "general-information-of-schools.csv", dtype={"postal_code": "str"}
    )

    return df


def format_data(df):

    df.columns = df.columns.str.upper()
    df = strip_spaces(df)

    ## DROP VP COLUMNS
    df = df.drop([x for x in df.columns if x.endswith("_VP_NAME")], axis=1)

    df = df.replace("na", np.nan)

    flag_cols = [
        "SAP_IND",
        "AUTONOMOUS_IND",
        "GIFTED_IND",
        "IP_IND",
    ]

    for x in flag_cols:
        df[x] = np.where(df[x].isnull(), -1, np.where(df[x].str.upper() == "YES", 1, 0))

    df["ADDRESS"] = df["ADDRESS"].str.upper()
    df["SCHOOL_NAME"] = df["SCHOOL_NAME"].str.upper()
    df["EMAIL_ADDRESS"] = df["EMAIL_ADDRESS"].str.upper()

    # Format postal codes
    df["POSTAL_CODE"] = df["POSTAL_CODE"].apply(lambda x: f"{x:0>6s}")

    def align_tel_no(df, x):
        df[x] = (
            df[x].str.replace(r"\s", "", regex=True).str.extract(r"(65)*(\d{8,})")[1]
        )

    # Format tel numbers
    for col in ["TELEPHONE_NO", "TELEPHONE_NO_2", "FAX_NO", "FAX_NO_2"]:
        align_tel_no(df, col)

    return df


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/school-directory-and-information"))
    df = format_data(df)

    # Add address info by querying OneMap API
    df_addr = get_school_address_info(df)
    df = df.merge(df_addr)

    dump(df, pathlib.Path("data/_processed/TBL_SCHOOL_INFO.csv.gzip"))

