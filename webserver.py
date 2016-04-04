from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Database client
mongo_client = MongoClient('smallville', 27017)
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
	app.run()