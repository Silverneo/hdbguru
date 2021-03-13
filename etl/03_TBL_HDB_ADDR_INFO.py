import pathlib
import pandas as pd
import numpy as np
from .utils import *
from .one_map_api import reverse_geocode


def load_data(data_dir: pathlib.Path):

    ldf = []

    for f in pathlib.Path("data/_raw/onemap-hdb-addresses/").glob("*json"):
        ldf.append(pd.read_json(f))
    df_addr = pd.concat(ldf, ignore_index=True)

    df_addr = df_addr.rename(columns={"HDB_ADDRESS": "_KEYWORD_"})  # TODO - REMOVE

    return df_addr


def _handle_exceptions(df: pd.DataFrame) -> pd.DataFrame:

    df_exp = pd.read_csv("data/_static/HDB_ADDR_EXCEPTIONS.csv")

    mask = df["_KEYWORD_"].isin(df_exp["_KEYWORD_"])

    df_dup, df = df.loc[mask].copy(), df.loc[~mask].copy()

    df_dup = df_dup.merge(df_exp)

    assert df_dup.shape[0] == df_exp.shape[0]

    df: pd.DataFrame = pd.concat([df, df_dup], ignore_index=True)

    return df


def _add_keys(df):

    _df = pd.read_csv("data/_processed/TBL_HDB_PROP_INFO.csv.gzip", sep="|")
    _df["_KEYWORD_"] = _df["BLOCK"] + " " + _df["STREET_NAME"]

    df = pd.merge(df, _df[["_KEYWORD_", "BLOCK", "STREET_NAME", "TOWN"]], how="left")
    assert df["BLOCK"].isnull().sum() == 0

    return df


def _rank_buildings(df):

    df["_SCORE"] = 0

    df["_SCORE"] = df["_SCORE"] + np.where(
        df["BUILDING"].str.contains(
            r"ACADEMY|STUDENT|PRESCHOOL|SCHOOL|SKOOL|LEARNING|LEARNERS|DEVELOPMENT|CHILDREN|CHILD CARE|KINDERGARTEN"
        ),
        1,
        0,
    )
    df["_SCORE"] = df["_SCORE"] + np.where(
        df["BUILDING"].str.contains(r"7 ELEVEN|GIANT|FAIRPRICE|NTUC"), 1, 0
    )
    df["_SCORE"] = df["_SCORE"] + np.where(
        df["BUILDING"].str.contains(r"COMMUNITY|SPORTS|SWIMMING|LIBRARY|SERVICE"), 1, 0
    )
    df["_SCORE"] = df["_SCORE"] + np.where(
        df["BUILDING"].str.contains(r"POST OFFICE|SPORTS|SWIMMING|POLICE"), 1, 0
    )
    df["_SCORE"] = df["_SCORE"] + np.where(
        df["BUILDING"].str.contains(r"DBS|UOB|OCBC|POSB|STANDARD CHARTERED|MAYBANK"),
        1,
        0,
    )

    return (
        df.sort_values(["_KEYWORD_", "_SCORE"])
        .groupby(["_KEYWORD_"])
        .first()
        .reset_index()
    )


def format_data(df):

    df = df.rename(columns={"POSTAL": "POSTAL_CODE"})

    ## REMOVE EMPTY POSTAL CODE
    df = df[df["POSTAL_CODE"] != "NIL"]

    ## ADD TOWN/BLK/STEET
    df = _add_keys(df)

    ## KEEP BLOCK NUMBER MATCHING ONE
    df = df[df["BLK_NO"] == df["BLOCK"]].reset_index(drop=True)

    ## REMOVE EXCEPTIONS - WAS HANDLED MANUALLY
    df = _handle_exceptions(df)

    ## SANITY CHECK
    df = pd.merge(
        df,
        df.groupby(["_KEYWORD_"])["POSTAL_CODE"]
        .nunique()
        .to_frame(name="POST_CNT")
        .reset_index(),
    )
    assert df[df["POST_CNT"] > 1].shape[0] == 0, "address with more than 1 postal code"

    ## RANK TO GET THE MOST RELATED ADDR INFO
    df = _rank_buildings(df)

    df = df[
        [
            "TOWN",
            "BLOCK",
            "STREET_NAME",
            "POSTAL_CODE",
            "ADDRESS",
            "BUILDING",
            "LATITUDE",
            "LONGITUDE",
            "X",
            "Y",
        ]
    ]

    return df


def get_cs5288_dataset():

    df = pd.read_csv("data/_raw/cs5228-kaggle-dataset/test.csv")
    df = pd.concat(
        [df, pd.read_csv("data/_raw/cs5228-kaggle-dataset/train.csv")],
        ignore_index=True,
        sort=False,
    )

    df.columns = df.columns.str.upper()

    # UPPERCASE ALL CATS
    for x in [
        "TOWN",
        "FLAT_TYPE",
        "STREET_NAME",
        "FLAT_MODEL",
        "SUBZONE",
        "PLANNING_AREA",
        "REGION",
    ]:
        df[x] = df[x].str.upper()

    df = df[
        [
            "TOWN",
            "BLOCK",
            "STREET_NAME",
            "LATITUDE",
            "LONGITUDE",
            "SUBZONE",
            "PLANNING_AREA",
            "REGION",
        ]
    ].drop_duplicates()

    df = df.rename(columns={"STREET_NAME": "FULL_STREET_NAME"})

    df_price = pd.read_csv("data/_processed/TBL_HDB_RESALE_PRICE.csv.gzip", sep="|")
    df_price = df_price[["TOWN", "BLOCK", "STREET_NAME"]].drop_duplicates()
    df_price["FULL_STREET_NAME"] = expand_street_name(df_price["STREET_NAME"])

    df = pd.merge(df, df_price, how="left", on=["TOWN", "BLOCK", "FULL_STREET_NAME"])

    df["STREET_NAME"] = np.where(
        df["STREET_NAME"].isnull(),
        expand_street_name(df["FULL_STREET_NAME"], reverse=True),
        df["STREET_NAME"],
    )

    assert (
        df["STREET_NAME"].isnull().sum() == 0
    ), "Still got missing street name, pls check"

    return df


def add_extra(df_addr):
    def anti_join(df, dff):
        df = df.merge(dff, how="outer", indicator=True)
        return df[df["_merge"] == "left_only"].drop("_merge", axis=1)

    df = get_cs5288_dataset()

    df_extra = anti_join(df, df_addr[["TOWN", "BLOCK", "STREET_NAME"]])[
        ["TOWN", "BLOCK", "STREET_NAME", "LATITUDE", "LONGITUDE"]
    ]

    res = df_extra.apply(
        lambda x: reverse_geocode(x["LATITUDE"], x["LONGITUDE"], 10, "All"), axis=1
    )

    ldf = []

    for i in range(len(res)):
        ldf.append(pd.DataFrame(res.iloc[i]).head(1))

    _tmp = pd.concat(ldf, ignore_index=True)
    _tmp = _tmp.rename(
        columns={
            "BUILDINGNAME": "BUILDING",
            "ROAD": "ADDRESS",
            "XCOORD": "X",
            "YCOORD": "Y",
            "POSTALCODE": "POSTAL_CODE",
        }
    )
    _tmp["BUILDING"] = _tmp["BUILDING"].str.upper().replace("NULL", "NIL")
    _tmp["ADDRESS"] = (
        _tmp["BLOCK"] + " " + _tmp["ADDRESS"] + " SINGAPORE " + _tmp["POSTAL_CODE"]
    )
    _tmp["POSTAL_CODE"] = format_sg_postal(_tmp["POSTAL_CODE"])
    _tmp = _tmp[["POSTAL_CODE", "ADDRESS", "BUILDING", "X", "Y"]]

    return (
        pd.concat(
            [df_addr, pd.concat([df_extra.reset_index(drop=True), _tmp], axis=1)],
            ignore_index=True,
            sort=False,
        ),
        df[["TOWN", "BLOCK", "STREET_NAME", "SUBZONE", "PLANNING_AREA", "REGION"]],
    )


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/onemap-hdb-addresses"))
    df = format_data(df)
    df, df_extra = add_extra(df)

    dump(df, pathlib.Path("data/_processed/TBL_HDB_ADDR_INFO.csv.gzip"))
    dump(df_extra, pathlib.Path("data/_processed/TBL_HDB_EXTRA_INFO.csv.gzip"))
