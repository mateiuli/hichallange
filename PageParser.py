import re, io, wikipedia

class PageParser(object):
	"""
	Given a page by it's title it searches on wikipedia for the page and
	parse it's content using regex to extract valuable informations.
	"""

	def __init__(self, save_action):
		# Patterns used to extract category, year and title
		self.patterns = {
			'category'	: re.compile(r'^==(.*)==$', re.M|re.I),
			'info'			: re.compile(u'^([0-9]+) \u2013 (.*)$', re.M|re.I|re.UNICODE)
		};

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
				category = match.group(1).strip()

			# Check if the current line represents a year + content
			match = self.patterns['info'].match(line)
			if match is not None:
				# Current lnie is a pair 'year - content'
				year = match.group(1).strip()
				content = match.group(2).strip()

				# Save information into database
				if category is not None:
					self.save_action(page_title, category, year, content)

	def __get_wiki_content(self, title):
		page = wikipedia.page(title)

		if page is not None:
			return page.title, page.content
		else:
			return None;
