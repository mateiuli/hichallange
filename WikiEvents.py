from pymongo import MongoClient
from PageParser import PageParser
from datetime import timedelta, date
from timeit import default_timer as timer
from multiprocessing.pool import ThreadPool
import locale, os

class WikiEvents(object):

	def __init__(self, dbserver):
		# Wikipedia page parser
		self.parser = PageParser(self.save)
		# Database client
		self.client = MongoClient(dbserver, 27017)
		# Database object
		self.db_wiki = self.client.db_wiki
		# Events collection
		self.col_events = self.client.db_wiki.events	
		# Change locale to english US
		#locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

	def save(self, **kwargs):
		self.col_events.insert_one(kwargs)

	def start(self):
		# Iterate over all days of a leap year (2016 is one)
		start_date = date(2016, 1, 1)
		end_date = date(2017, 1, 1)
		start = timer()
		
		for curr_date in self.__date_range(start_date, end_date):
			page_title = '{d:%B}_{d.day}'.format(d=curr_date)
			print "Parsing page: ", page_title,
			self.parser.parse_page(page_title)

		end = timer()
		print "Time elapsed: ", end - start

		# Create text index on title (for title search)
		self.col_events.createIndex({"title": "text"})
		self.col_events.createIndex({"year": "1", "category" : "1", "day" : "1"})

	def __date_range(self, start_date, end_date):
		""" Generates dates between start_date and end_date """
		for n in range(int((end_date - start_date).days)):
			yield start_date + timedelta(n)

if __name__ == "__main__":
	if len(sys.argv) > 2:
		if sys.argv[1] == "--dbserver":
			dbserver = sys.argv[2]
		else:
			dbserver = os.environ['DB_PORT_27017_TCP_ADDR']
	
	# Connect to database, get collection handler
	wp = WikiEvents(dbserver)
	wp.start()