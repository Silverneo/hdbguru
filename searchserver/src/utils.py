import requests
import numpy as np
import pandas as pd

onemapSearchUrl = "https://developers.onemap.sg/commonapi/search?searchVal={}&returnGeom=Y&getAddrDetails=Y"

def onemap_search(where):
    res = requests.get(onemapSearchUrl.format(where))

    if res.status_code != 200:
        return None
    try:
        res = res.json()
    except Exception as e:
        return None

    if res['found'] == 0:
        return None

    return res['results'][0]

def distance_score(dist):
    if dist <= 1000:
        return 5
    elif 1000 < dist <= 5000:
        return 4
    elif 5000 < dist <= 10000:
        return 3
    elif 10000 < dist <= 15000:
        return 2
    else:
        return 1
    
def price_score(price):
    if price <= 500:
        return 5
    elif 500 < price <= 600:
        return 4
    elif 600 < price <= 700:
        return 3
    elif 700 < price <= 800:
        return 2
    else:
        return 1

def lease_score(lease):
    if lease >= 90:
        return 5
    elif 80 <= lease < 90:
        return 4
    elif 70 <= lease < 80:
        return 3
    elif 60 <= lease < 70:
        return 2
    else:
        return 1
    
def surrounding_score(n_500, n_1000, n_2000):
    
    if n_500 >= 2:
        score = 5 
    elif n_500 == 1:
        score = 4 
    elif n_1000 >= 2:
        score = 3 
    elif n_1000 == 1:
        score = 2 
    elif n_2000 >= 1:
        score = 1 
    else:
        score = 0

    return score


def school_score(n_500, n_1000, n_2000):

    if n_500+n_1000 >= 3:
        score = 5 
    elif n_500+n_1000 == 2:
        score = 4 
    elif n_500+n_1000 == 1:
        score = 3
    elif n_2000 >= 2:
        score = 2
    elif n_2000 == 1:
        score = 1
    else:
        score = 0

    return score

def min_max_norm(x, x_max, x_min):
    return 5*(x-x_min)/(x_max-x_min)

def compute_score(user_matrix_norm, row):
    dist_s = distance_score(row['distance_to_target'])
    price_s = price_score(row['avg_price_psf'])
    lease_s = lease_score(row['remain_lease'])
    
    transport_s = surrounding_score(row['station_cnt_wth_500'], row['station_cnt_500_1km'], row['station_cnt_1km_2km'])
    mall_s = surrounding_score(row['mall_cnt_wth_500'], row['mall_cnt_500_1km'], row['mall_cnt_1km_2km'])
    hawker_s = surrounding_score(row['hawker_cnt_wth_500'], row['hawker_cnt_500_1km'], row['hawker_cnt_1km_2km'])
    school_s = school_score(row['school_cnt_wth_500'], row['school_cnt_500_1km'], row['school_cnt_1km_2km'])
    
    score = user_matrix_norm * np.array([dist_s, price_s, lease_s, transport_s, mall_s, hawker_s, school_s])
    return sum(score)

