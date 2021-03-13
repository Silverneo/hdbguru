import pandas as pd
import pathlib

def strip_spaces(df: pd.DataFrame):
    return df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

def format_sg_postal(x):
    return x.apply(lambda x: x if pd.isnull(x) else f"{str(x):0>6s}")

def dump(df: pd.DataFrame, path: pathlib.Path, sep: str = "|"):

    if any(
        df.select_dtypes(include=["object"]).apply(
            lambda x: any(x.str.contains(sep, regex=False))
        )
    ):
        print(f"WARNING - SEP[{sep}] exists in the data")

    df.to_csv(path, sep=sep, index=False)