import os
import sys
import time
import json
import argparse
import logging
import datetime

import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import flask
from flask import Flask, request, jsonify, Response, redirect, url_for

from utils import *
from sql import *

logger = logging.getLogger('searchserver')
if not logger.handlers:
	log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
	file_handler = logging.StreamHandler(sys.stdout)
	file_handler.setFormatter(log_formatter)
	file_handler.setLevel(logging.INFO)
	logger.setLevel(logging.INFO)
	logger.addHandler(file_handler)

app = Flask("app")

@app.route("/")
def index():
	return 'CS5224 - HDBguru\n'

@app.route("/api/v1/get_nearby_hdb", methods=["GET"])
def get_nearby_hdb():
	where = request.args['where']

	w_distance = request.args.get('w_distance', default=2.5, type=float)
	w_price = request.args.get('w_price', default=2.5, type=float)
	w_lease = request.args.get('w_lease', default=2.5, type=float)
	w_transport = request.args.get('w_transport', default=2.5, type=float)
	w_shopping = request.args.get('w_shopping', default=2.5, type=float)
	w_dining = request.args.get('w_dining', default=2.5, type=float)
	w_education = request.args.get('w_education', default=2.5, type=float)

	topn = request.args.get('topn', default=20, type=int)

	user_matrix = np.array([w_distance, w_price, w_lease, w_transport, w_shopping, w_dining, w_education])
	user_matrix_norm = user_matrix / sum(user_matrix)

	r = onemap_search(where)
	if r is None:
		logger.warning("place not found: {}".format(where))
		return None, 503

	query_lang = r['LONGITUDE']
	query_lat = r['LATITUDE']
	max_return = topn
	cur_year = datetime.date.today().year

	df = pd.read_sql(nearby_hdb_sql.format(query_lang, query_lat, max_return, cur_year-10), db)

	# drop duplicated columns
	df = df.loc[:,~df.columns.duplicated()]

	df['remain_lease'] = df['lease_commence_date'].apply(lambda x: 99-(cur_year-x))
	df['floor_area_sqft'] = df['floor_area_sqm'] * 10.7639
	df['avg_resale_price'] = df.apply(lambda row: row['avg_price_psf'] * row['floor_area_sqft'], axis=1)

	df = df.drop_duplicates(subset=['hdb_id'])

	# compute score base on user matrix
	df['score'] = df.apply(lambda row: compute_score(user_matrix_norm, row), axis=1)

	x_max = df['score'].max()
	x_min = df['score'].min()
	df['score'] = df['score'].apply(lambda x: min_max_norm(x, x_max, x_min))

	results = df.to_dict(orient='records')
	logger.info("request get_nearby_hdb succeed: {}".format(results))
	return jsonify(results), 200

@app.route("/api/v1/get_neighbor_detail", methods=["GET"])
def get_neighbor_detail():
	latitude = request.args.get('latitude', type=float)
	longitude = request.args.get('longitude', type=float)

	topn = request.args.get('topn', default=5, type=int)

	df_mall = pd.read_sql(nearby_mall_sql.format(longitude, latitude, topn), db)
	df_school = pd.read_sql(nearby_school_sql.format(longitude, latitude, topn), db)
	df_mrt = pd.read_sql(nearby_mrt_sql.format(longitude, latitude, topn), db)
	df_hawker = pd.read_sql(nearby_hawker_sql.format(longitude, latitude, topn), db)

	results = {
		'mall' : df_mall.to_dict(orient='records'),
		'school' : df_school.to_dict(orient='records'),
		'mrt' : df_mrt.to_dict(orient='records'),
		'hawker' : df_hawker.to_dict(orient='records')
	}

	logger.info("request get_neighbor_detail succeed: {}".format(results))
	return jsonify(results), 200

if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
	parser.add_argument("--port", default=31001, help="the flask server port number.")
	parser.add_argument("--dbaddr", default="127.0.0.1:5432", help="the db address.")
	args = parser.parse_args()

	# need to use postgresql:// instead of postgres://
	db_string = "postgresql://hgadmin:pwd123456@{}/hdbguru".format(args.dbaddr)
	db = create_engine(db_string)

	app.run(host='0.0.0.0', port=args.port, threaded=True, debug=False)