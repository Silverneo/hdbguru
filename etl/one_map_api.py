import requests
import time
from multiprocessing import Pool

import json
import re
import pandas as pd

ONEMAP_AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjcyMzYsInVzZXJfaWQiOjcyMzYsImVtYWlsIjoiY2h1bm1lbmcxOTkxQGdtYWlsLmNvbSIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTYxNTY1MDcwNCwiZXhwIjoxNjE2MDgyNzA0LCJuYmYiOjE2MTU2NTA3MDQsImp0aSI6IjhlMGQzNmE1ZTc1YjBlYTY5OTE0NDAzOWI4MjM1NzAxIn0.8YbkzmWVmENQPHJoh2O7GkRhE7fTJ4GgehprH9kvtr0"


def reverse_geocode(lat, long, buffer, addr_type):

    results = []

    response = requests.get(
        f"https://developers.onemap.sg/privateapi/commonsvc/revgeocode?"
        f"location={lat},{long}"
        f"&buffer={buffer}"
        f"&addressType={addr_type}"
        f"&token={ONEMAP_AUTH_TOKEN}"
    ).json()

    if "GeocodeInfo" in response:
        return response["GeocodeInfo"]
    else:
        return None


def search_value(keyword: str, geometry: bool = True, detail: bool = True):

    page = 1
    results = []

    geometry_flag = "Y" if geometry else "N"
    detail_flag = "Y" if detail else "N"

    while True:
        # TODO - add special handling to exit loop if things go wrong
        try:
            response = requests.get(
                f"http://developers.onemap.sg/commonapi/search?"
                f"searchVal={keyword}"
                f"&returnGeom={geometry_flag}"
                f"&getAddrDetails={detail_flag}"
                f"&pageNum={page}"
            ).json()

        except requests.exceptions.ConnectionError as e:
            print(f"Fetching {keyword:40s} failed. Retrying in 2 sec ...")
            time.sleep(2)
            continue
        except:  # other exceptions, return empty value
            break

        if response["found"] == 0:
            break

        for res in response["results"]:
            res["_KEYWORD_"] = keyword

        results = results + response["results"]

        if response["totalNumPages"] > page:
            page = page + 1
        else:
            break

    return results


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


## TODO TODO
def remap_address_keywords(keywords, dir="UP"):

    new_keywords = []

    rewords = {
        "ST.": "SAINT",
        "CL": "CLOSE",
        "RD": "ROAD",
        "CTRL": "CENTRAL",
    }

    for keyword in keywords:
        for k, v in rewords.items():
            if dir == "UP":
                keyword = re.sub(f"\b{k}\b", v, keyword)
            else:
                keyword = re.sub(f"\b{v}\b", k, keyword)


def query_api(keywords, file_name, n=5):
    pool = Pool(processes=n)

    i = 1

    for sub_list in _chunks(keywords, 1000):

        print(f"== Processing chunk [{i:03d}]...")

        res = pool.map(search_value, sub_list)

        res = [x for x in res if x]  # remove empty result

        jstr = json.dumps([y for x in res for y in x], indent=2, sort_keys=True)

        with open(f"{file_name}_{i:03d}.json", "wb") as f:
            f.write(jstr.encode("utf-8"))

        i = i + 1
        time.sleep(5)


def query_onemap_api(keywords, n=5):
    pool = Pool(processes=n)

    i = 1

    jres = []

    for sub_list in _chunks(keywords, 1000):

        print(f"== Processing chunk [{i:03d}]...")

        res = pool.map(search_value, sub_list)

        res = [x for x in res if x]  # remove empty result

        jstr = json.dumps([y for x in res for y in x], indent=2, sort_keys=True)

        jres.append(jstr)

        i = i + 1
        time.sleep(5)

    return jres


def search_hdb_address():

    df = pd.read_csv("data/_processed/TBL_HDB_PROP_INFO.csv.gzip", sep="|")

    all_hdb_addresses = (df["BLOCK"] + " " + df["STREET_NAME"]).unique().tolist()

    query_api(all_hdb_addresses, "hdb_building_info")


def search_school_address():

    df = pd.read_csv(
        "data/_processed/TBL_SCHOOL_INFO.csv.gzip",
        sep="|",
        dtype={"POSTAL_CODE": "str"},
    )

    # all_school_addresses = (df["ADDRESS"] + " " + df["POSTAL_CODE"]).unique().tolist()
    all_school_addresses = (df["ADDRESS"]).unique().tolist()
    query_api(all_school_addresses, "school_building_info")


if __name__ == "__main__":

    # search_hdb_address()
    search_school_address()
