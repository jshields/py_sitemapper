"""parse module"""
import requests
from HTMLParser import HTMLParser
#from requests.auth import HTTPBasicAuth
#from getpass import getpass

class Session(object):
    """requests session wrapper"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        headers = {
                    "Accept": "text/html"
                  }
        self.session.headers.update(headers)

    @staticmethod
    def validate_url(url):
        """return a boolean specifying valid or invalid url"""
        # TODO
        #url_pattern = r'http[s]://[A-Za-z0-9]\.[A-Za-z0-9]\.[A-Za-z0-9]'
        #re.search()
        #response = self.session.get(url)
        #if response.status_code != requests.codes.OK:
        return True
    
    def try_get_html(self, endpoint, validate=False):
        """GET requests a URI, fails silently by default,
        the request may be a guess or dead link
        """
        url = '{}/{}'.format(self.base_url, endpoint)
        response = self.session.get(url)

        if validate:
            isgood = validate_url(url)
            if not isgood:
                raise ValueError('URL is malformed or incomplete.')

        return response.content

class Page(object):
    """page of a site"""

    def __init__(self, content):
        self.content = content
        self._links = None

    class LinksHTMLParser(HTMLParser):
        """HTMLParser subclass to get hrefs from anchors"""

        def __init__(self):
            HTMLParser.__init__(self)
            self._parsed_links = []

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self._parsed_links.append(attr[1])

        def close(self):
            HTMLParser.close(self)
            return self._parsed_links

    def _clean_links(self, links):
        """only return hypertext references - not hash navs, mailto, or tel links"""
        clean = []

        for l in self.links:
            if Session.validate_url(l):
                clean.append(l)

        return clean

    def _fully_qualify_links(self, links):
        """determine if a link is fully qualified with the domain name,
        if not then prepend with the base URL
        """
        # TODO
        return links
        #for l in self._links:
        #l = '{}/{}'.format(self.base_url, l)

    def _parse_links(self):
        """use LinksHTMLParser to extract hrefs on page"""
        html = self.content
        self._links = []
        parser = self.LinksHTMLParser()
        parser.feed(html)
        parser.close()

    @property
    def links(self):
        """anchors on the current page content"""
        if self._links == None:
            links = self._parse_links()
            links = self._fully_qualify_links(links)
            links = self._clean_links(links)
            self._links = links
        return self._links
