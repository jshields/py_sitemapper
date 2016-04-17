"""parse module: parse web content"""
import requests
import re
import urlparse
from HTMLParser import HTMLParser
#from requests.auth import HTTPBasicAuth
#from getpass import getpass


class Session(object):
    """requests session wrapper"""

    @staticmethod
    def getStatusByCode(code):
        """function for finding request status by code"""
        # may need further manipulation before dict zipping
        # because there are more string aliases than there are numeric codes
        orig = vars(requests.codes)
        flipped = dict(zip(orig.values(), orig.keys()))
        code = int(code)
        return flipped[code].upper()

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        headers = {
                    'Accept': 'text/html'
                  }
        self.session.headers.update(headers)

    def try_get_html(self, endpoint):
        """GET requests a URI, fails silently by default,
        the request may be a guess or dead link.
        Designed to work with links for relative URIs, not external or full URLs.
        """
        url = '{}/{}'.format(self.base_url, endpoint)
        response = self.session.get(url)
        return response.content


class Page(object):
    """page of a site"""

    def __init__(self, url, content):
        """Page init"""
        # URL to serve as static information about this page's location
        self.url = url
        # the HTML content of the page
        self.content = content
        self._links = None

    class LinksHTMLParser(HTMLParser):
        """HTMLParser subclass to get hrefs from anchors"""

        def __init__(self):
            """LinksHTMLParser init"""
            HTMLParser.__init__(self)
            self._parsed_links = []

        def handle_starttag(self, tag, attrs):
            """look for anchors and store their href attribute"""
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href':
                        self._parsed_links.append(attr[1])

        def close(self):
            HTMLParser.close(self)
            return self._parsed_links

    def _remove_hashnavs(self, links):
        """only return URLs - not hash navs"""


        # TODO
        clean = []

        hashnav_pattern = r'$#'

        for l in self.links:
            match = re.search()


                clean.append(l)

        return clean

    def _fully_qualify_links(self, links):
        """determine if a link is fully qualified with
        the correct protocol/scheme and domain name,
        if not then prepend with the base URL
        """
        
        import ipdb
        ipdb.set_trace()

        links_to_keep = []
        parse_page_url = urlparse.urlparse(self.url)

        for l in links:
            parse_link = urlparse.urlparse(l)
            scheme = parse_link.scheme
            hostname = parse_link.hostname

            # must be a hypertext protocol, we are dealing with HTML
            # removes 'tel', 'mailto', etc
            if scheme in ('', 'http', 'https'):
                if scheme == '':
                    # if the protocol was left off in the link
                    # we use the protocol of the base URL
                    scheme = parse_page_url.scheme

                if hostname is None:
                    # fully qualify relative URIs
                    hostname = parse_page_url.hostname

                parse_link = urlparse.urlparse('%s://%s/%s' % (scheme, hostname, parse_link.path))
                
                if parse_link.hostname == parse_page_url.hostname:
                    # "Note that this means that all URLs listed in the Sitemap must use the same protocol...
                    # and reside on the same host as the Sitemap." - http://www.sitemaps.org/protocol.html
                    links_to_keep.append(parse_link.geturl())

        import ipdb
        ipdb.set_trace()
        
        return links_to_keep

    def _parse_links(self):
        """use LinksHTMLParser to extract hrefs on page"""
        html = self.content
        self._links = []
        parser = self.LinksHTMLParser()
        parser.feed(html)
        parsed_links = parser.close()
        return parsed_links

    @property
    def links(self):
        """anchors on the current page content"""
        if self._links is None:
            links = self._parse_links()
            links = self._remove_hashnavs(links)
            links = self._fully_qualify_links(links)
            self._links = links

        return self._links
