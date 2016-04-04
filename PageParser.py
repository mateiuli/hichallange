import re, io, wikipedia

class PageParser(object):
	"""
	Given a page by it's title it searches on wikipedia for the page and
	parse it's content using regex to extract valuable informations.
	"""

	def __init__(self, save_action):
		# Patterns used to extract category, year and title
		self.patterns = {
			'category' : re.compile(r'^==(.*)==$', re.M|re.I),
			'info' : re.compile(u'^([0-9]+.*)\u2013(.*)$', re.M|re.I|re.UNICODE),
			'info_no_year' : re.compile(r'^(.*)([^:])$', re.M|re.I)
		};

		# List of allowed categories
		self.categories = ['deaths', 'births', 'events', 'holidays and observances']

		# Method to call when one piece of information was parsed completly
		self.save_action = save_action

	def parse_page(self, title):
		# Get page content in plain text format
		page_title, content = self.__get_wiki_content(title)
		
		# Current category
		category = None

		# Iterate over each line and extract information 
		for line in content.splitlines():
			# Check if the current line is a category title
			match = self.patterns['category'].match(line)
			if match is not None:
				# Current line is a category title
				category = match.group(1).strip().lower()

				if category not in self.categories:
					category = None

				# Next line contains events from this category
				continue

			if category is not None:
				# Check if the current line represents a year + content
				match = self.patterns['info'].match(line)
				if match is not None:
					# Current lnie is a pair 'year - content'
					kwargs = {
							"category" : category,
							"day" : page_title,
							"year" : match.group(1).strip(),
							"title" : match.group(2).strip()
						}

					# Save information
					self.save_action(**kwargs)
				else:
					# Or maybe it is from a category that doesn't have an year associated
					# One such category is 'holidays and observances'
					match = self.patterns['info_no_year'].match(line)
					if match is not None:
						kwargs = {
								"category" : category,
								"day" : page_title,
								"title" : match.group().strip()
							}

						# Save information
						self.save_action(**kwargs)

	def __get_wiki_content(self, title):
		page = wikipedia.page(title)

		if page is not None:
			return page.title, page.content
		else:
			return None;
