import re, wikipedia, io

# Page title to search for
page_title = "March 13"

# Grab text content
content = wikipedia.page(page_title).content

# Regex patterns for categories and content
category_pattern = re.compile(u'^==(.*)==$', re.M|re.I)
info_pattern = re.compile(u'^([0-9]+) \u2013 (.*)$', re.M|re.I|re.UNICODE)

# Extract all categories
result = category_pattern.match("== Events ==")

print result

#for line in content.splitlines():
	#print "line: ", line