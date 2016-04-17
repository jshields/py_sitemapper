"""sitemap module: website sitemap utility"""
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

# - All data values in a Sitemap must be entity-escaped. TODO
# - The file itself must be UTF-8 encoded.
# - All URLs in a Sitemap must be from a single host,
#   such as www.example.com or store.example.com


class Sitemap(object):
    """website sitemap built from links"""

    def __init__(self, links):
        self.links = links

    @staticmethod
    def _ensure_file_extension(filepath):
        """verify that the file name has the xml file entension"""
        ext_pattern = r'\.xml$'
        match = re.search(ext_pattern, filepath)
        # ensure correct file extension
        if not match:
            filepath = '{}.xml'.format(filepath)
        return filepath

    @property
    def xml(self):
        """build XML content for sitemap"""
        _xml = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        _xml += u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for l in self.links:
            _xml += u'\t<url>\n<loc>%s</loc>\n\t</url>\n' % l

        _xml += u'</urlset>\n'
        return _xml

    def export(self, filepath='sitemap.xml'):
        """export a sitemap file"""
        filepath = _ensure_file_extension(filepath)

        import ipdb
        ipdb.set_trace()

        with open(filepath, encoding='utf-8', mode='w') as f:
            f.write(self.xml)
