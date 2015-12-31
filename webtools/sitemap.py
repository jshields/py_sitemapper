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
# TODO
# All data values in a Sitemap must be entity-escaped. The file itself must be UTF-8 encoded.
# all URLs in a Sitemap must be from a single host, such as www.example.com or store.example.com

class Sitemap(object):
    """website XML sitemap"""

    def __init__(self, links):
       self.links = links

    def xml(self):
       """build XML content for sitemap"""
       xml = u'<?xml version="1.0" encoding="UTF-8"?>\n'
       xml += u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

       for l in self.links:
         xml += u'\t<url>\n<loc>%s</loc>\n\t</url>\n' % l

       xml += u'</urlset>'
       return xml

    @staticmethod
    def _ensure_file_extension(filepath):
        """verify that the file name has the xml file entension"""
        ext_pattern = r'\.xml$'
        match = re.search(ext_pattern, filepath)
        # ensure correct file extension
        if not match:
            filepath = '{}.xml'.format(filepath)
        return filepath
 

    def export(self, filepath='sitemap.xml'):
       """export a sitemap file"""
       filepath = _ensure_file_extension(filepath)

       f = open(filepath, 'w')
       # TODO make sure we write in utf-8
       f.write(self.xml())
       f.close()
