import pandas as pd
import pathlib
from utils import *


def load_data(data_dir: pathlib.Path):

    # w/o remanining lease
    df_99 = pd.read_csv(
        data_dir / "resale-flat-prices-based-on-approval-date-1990-1999.csv"
    )
    df_12 = pd.read_csv(
        data_dir / "resale-flat-prices-based-on-approval-date-2000-feb-2012.csv"
    )
    df_14 = pd.read_csv(
        data_dir
        / "resale-flat-prices-based-on-registration-date-from-mar-2012-to-dec-2014.csv"
    )

    # w/  remaining_lease
    df_16 = pd.read_csv(
        data_dir
        / "resale-flat-prices-based-on-registration-date-from-jan-2015-to-dec-2016.csv"
    )
    df_21 = pd.read_csv(
        data_dir
        / "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv"
    )

    # Merge all together
    df_1 = pd.concat([df_99, df_12, df_14], ignore_index=True)
    df_2 = pd.concat([df_16, df_21], ignore_index=True).drop(
        ["remaining_lease"], axis=1
    )

    df = pd.concat([df_1, df_2], ignore_index=True)

    return df


def format_data(df: pd.DataFrame) -> pd.DataFrame:

    _cols = [
        "MONTH",
        "TOWN",
        "BLOCK",
        "STREET_NAME",
        "FLAT_TYPE",
        "FLAT_MODEL",
        "LEASE_COMMENCE_DATE",
        "STOREY_RANGE",
        "FLOOR_AREA_SQM",
        "RESALE_PRICE",
    ]

    df.columns = df.columns.str.upper()

    assert all([x in df.columns for x in _cols])

    # Set month to month end
    df["MONTH"] = pd.to_datetime(df["MONTH"]) + pd.offsets.MonthEnd(0)

    # Calculate storey range from & to
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                df["STOREY_RANGE"].str.extract(r"(\d+) TO (\d+)").values,
                columns=["STOREY_RANGE_FROM", "STOREY_RANGE_TO"],
            ),
        ],
        axis=1,
    ).drop(["STOREY_RANGE"], axis=1)

    df["STOREY_RANGE_FROM"] = df["STOREY_RANGE_FROM"].astype("int")
    df["STOREY_RANGE_TO"] = df["STOREY_RANGE_TO"].astype("int")

    _cols.remove("STOREY_RANGE")
    _cols = _cols + ["STOREY_RANGE_FROM", "STOREY_RANGE_TO"]

    # UPPERCASE ALL CATS
    for x in ["TOWN", "FLAT_TYPE", "STREET_NAME", "FLAT_MODEL"]:
        df[x] = df[x].str.upper()

    # Cleanup FLAT_TYPE MULTI GENERATION CAT
    df["FLAT_TYPE"] = df["FLAT_TYPE"].replace({"MULTI GENERATION": "MULTI-GENERATION"})

    return df[_cols]


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/resale-flat-prices/"))
    df = format_data(df)
    dump(df, pathlib.Path("data/_processed/TBL_HDB_RESALE_PRICE.csv.gzip"))
