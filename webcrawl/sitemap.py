"""sitemap module"""
import re

# example XML sitemap
"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> 
  <url>
    <loc>http://www.example.com/foo.html</loc> 
  </url>
</urlset>
"""

class Sitemap(object):
	"""website XML sitemap"""

	def __init__(self, links):
		self.links = links

	def xml(self):
		"""build XML content for sitemap"""
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

		for l in self.links:
			xml += '\t<url>\n<loc>%s</loc>\n\t</url>\n' % l

		xml += '</urlset>'

		return xml
 

	def export(self, filepath='sitemap.xml'):
		"""export a sitemap file"""
		ext_pattern = r'\.xml$'
		match = re.search(ext_pattern, filepath)

		# ensure correct file extension
		if not match:
			filepath = '{}.xml'.format(filepath)

		f = open(filepath, 'w')

		f.write(self.xml())

		f.close()
