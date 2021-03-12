import pandas as pd
import numpy as np

from utils import *


def load_data(data_dir: pathlib.Path):

    df = pd.read_csv(data_dir / "TBL_MRT_LRT_ADDR_INFO.csv")

    return df


def format_data(df):
    return df


if __name__ == "__main__":

    df = load_data(pathlib.Path("data/_mingxuan"))
    df = format_data(df)

    dump(df, pathlib.Path("data/_processed/TBL_MRT_LRT_ADDR_INFO.csv.gzip"))

