"""sitemap module: website sitemap utility"""
import io
import re


"""
example XML sitemap:
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

DEFAULT_SITEMAP_NAME = 'sitemap.xml'


class Sitemap(object):

    """Website sitemap built from links.
    Can be output to a sitemap file.
    """

    def __init__(self, links):
        """
        Sitemap init

        Args:
            links (list of str): A list of the URLs
                that should be in the sitemap.
                These should likely correspond
                to links on a web page.
        """
        self.links = links

    @staticmethod
    def _ensure_file_extension(filepath):
        """verify that the file name has the xml file entension"""
        ext_pattern = r'\.xml$'
        match = re.search(ext_pattern, filepath)
        # ensure correct file extension
        if not match:
            filepath = '{path}.xml'.format(path=filepath)
        return filepath

    @property
    def xml(self):
        """build XML content for sitemap
        TODO: XML template would be better for code separation
        """
        _xml = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        _xml += u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for url in self.links:
            _xml += (u'\t<url>\n'
                     u'\t\t<loc>{url}</loc>\n'
                     u'\t</url>\n'
                     ).format(url=url)

        _xml += u'</urlset>\n'
        return _xml

    def export(self, filepath=DEFAULT_SITEMAP_NAME):
        """export a sitemap file"""
        filepath = self._ensure_file_extension(filepath)

        with io.open(filepath, encoding='utf-8', mode='w') as fi:
            fi.write(self.xml)
