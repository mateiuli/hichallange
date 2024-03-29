from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import os, sys

app = Flask(__name__)

# Collection
mongo_db_col_events = None

def init_db():
	global mongo_db_col_events
	# Database client
	mongo_client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
	# Database object
	mongo_db_wiki = mongo_client.db_wiki
	# Events collection
	mongo_db_col_events = mongo_client.db_wiki.events

@app.route("/", methods=['GET'])
def index():
	# Get query string; extract day, year and category
	day = request.args.get('day')
	year = request.args.get('year')
	category = request.args.get('category')
	keyword = request.args.get('keyword')

	# Query dict
	qdict = {}

	if category:
		qdict['category'] = category.strip().lower()	
	if year:
		qdict['year'] = year.strip().upper()	
	if day:
		qdict['day'] = day.strip().lower().capitalize().replace("_", " ")
	if keyword:
		qdict['$text'] = {"$search" : keyword.strip()}

	# List of results
	res = []
	if qdict:
		cursor = mongo_db_col_events.find(
				qdict, 
				{
					"category": 1,
					"day" : 1,
					"year" : 1,
					"title" : 1,
					"_id" : 0
				})

		res = [doc for doc in cursor]

	return dumps({"results" : res})

if __name__ == "__main__":
	if len(sys.argv) > 2 and sys.argv[1] == "--dbserver":
		os.environ['DB_PORT_27017_TCP_ADDR'] = sys.argv[2]
	
	# Connect to database, get collection handler
	init_db()
	app.run(host='0.0.0.0')