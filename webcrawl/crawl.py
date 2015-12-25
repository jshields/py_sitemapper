"""crawl module"""
import urllib2
import requests

class Session(object):
	"""requests session wrapper"""

	def __init__(self, base_url):
		self.session = requests.Session()
		self.base_url = base_url
		self.links = []

	def fully_qualify_links(self):
		"""determine if a link is fully qualified with the domain name,
		if not then prepend with the base URL
		"""
		#for l in self.links:
		#l = '{}/{}'.format(self.base_url, l)

	def try_get_html(self, endpoint):
		"""GET requests a URI, fails silently,
		the request may be a guess or dead link
		"""
		url = '{}/{}'.format(self.base_url, endpoint)
		response = self.session.get(url)

		if response.status_code != requests.codes.OK:
			return None
		else:
			return response.content
