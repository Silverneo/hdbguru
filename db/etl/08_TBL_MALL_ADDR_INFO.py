import pandas as pd
import numpy as np

from .utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_csv(data_dir / "sg-shopping-malls.csv")

    assert df.shape[0] == df['NAME'].unique().size, "NAME is not unique, pls check"

    return df


def format_data(df):
    return df

if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_raw/cs5228-kaggle-dataset"))
    df = format_data(df)

    dump(df, pathlib.Path("data/_processed/TBL_MALL_ADDR_INFO.csv.gzip"))

