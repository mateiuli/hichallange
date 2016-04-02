from pymongo import MongoClient
from PageParser import PageParser

class WikiParser(object):

	def __init__(self):
		"""

		"""

		# Wikipedia page parser
		self.parser = PageParser(self.__save)
		# Database client
		self.client = MongoClient('smallville', 27017)
		# Database object
		self.db_wiki = self.client.db_wiki
		# Events collection
		self.col_events = self.client.db_wiki.events

		self.parser.parse_page('march 13')

	def __save(self, page_title, category, year, content):
		print "Saving page_title = %s, category = %s, year = %s, content = %s" % (page_title, category, year, content)
		self.col_events.insert_one({
				"category" 		: category,
				"day"					: page_title,
				"year"				: year,
				"content"			: content
			})

wp = WikiParser()