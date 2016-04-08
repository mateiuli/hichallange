import locale, os, sys, pymongo, socket
from pymongo import MongoClient
from PageParser import PageParser
from datetime import timedelta, date
from timeit import default_timer as timer

class FetchWiki(object):

	def __init__(self, dbserver):
		"""
		Initialize parser, connects to mongodb server and creates indexes
		if they don't exist.

		- dbserver: mongodb server's address.
		"""
		# Wikipedia page parser
		self.parser = PageParser(self.save)
		# Database client
		self.client = MongoClient(dbserver, 27017)
		# Database object
		self.db_wiki = self.client['db_wiki']
		# Events collection
		self.col_events = self.db_wiki['events']
		# Create text index on title (for title search) (if not exist)
		self.col_events.ensure_index([("title", pymongo.TEXT)])
		# Create indexes for year, day and category
		self.col_events.ensure_index([
			("year", pymongo.ASCENDING), 
			("category", pymongo.ASCENDING), 
			("day", pymongo.ASCENDING)])
		
	def save(self, **kwargs):
		""" Inserts into database a new entry """
		self.col_events.insert_one(kwargs)

	def start(self):
		""" Starts the parsing process """
		# Iterate over all days of a leap year (2016 is one)
		start_date = date(2016, 1, 1)
		end_date = date(2017, 1, 1)
		start = timer()
		
		for curr_date in self.__date_range(start_date, end_date):
			page_title = '{d:%B}_{d.day}'.format(d=curr_date)
			self.parse(page_title)

		end = timer()
		print "Time elapsed: ", end - start

	def parse(self, page_title):
		""" 
		Calls the parser for a given page title, 
		the parser calls save method
		"""

		try:
			print "Parsing page '%s'" % page_title,
			self.parser.parse_page(page_title)
			print " .... OK"
		except Exception:
			print " ... failed"

	def __date_range(self, start_date, end_date):
		""" Generates dates between start_date and end_date """
		for n in range(int((end_date - start_date).days)):
			yield start_date + timedelta(n)

if __name__ == "__main__":
	dbserver = ""

	if len(sys.argv) > 2 and sys.argv[1] == "--dbserver":
		dbserver = sys.argv[2]
	else:
		dbserver = os.environ['DB_PORT_27017_TCP_ADDR']
	
	# Connect to database, get collection handler
	wp = FetchWiki(dbserver)
	wp.start()