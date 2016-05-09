"""parse module: parse web content"""
import requests  # pip dependency
import logging
import re
import urlparse
from HTMLParser import HTMLParser
#from requests.auth import HTTPBasicAuth
#from getpass import getpass


class Session(object):
    """requests Session wrapper"""

    @staticmethod
    def status_by_code(code):
        """find request status by code"""
        orig = vars(requests.codes)
        flipped = dict(zip(orig.values(), orig.keys()))
        code = int(code)
        return flipped[code].upper()

    def __init__(self):
        """init parse Session with desired headers"""
        self.session = requests.Session()
        headers = {
                    'Accept': 'text/html'
                  }
        self.session.headers.update(headers)

    def html_at_url(self, url):
        """
        get the HTML content at a url
        """
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


    class LinksHTMLParser(HTMLParser):
        """HTMLParser subclass to get hrefs from anchors"""

        def __init__(self):
            """LinksHTMLParser init"""
            HTMLParser.__init__(self)
            self._parsed_links = []

        def handle_starttag(self, tag, attrs):
            """look for anchors and store their href attribute"""
            # anchor tag
            if tag == 'a':
                for attr in attrs:
                    # attr name
                    if attr[0] == 'href':
                        # attr value
                        self._parsed_links.append(attr[1])

        def close(self):
            """done parsing"""
            HTMLParser.close(self)
            return self._parsed_links

    def _remove_hashnavs(self, links):
        """only return URLs - not hash navs"""
        # TODO verify results
        hashnav_pattern = r'(^#)'

        for li in links:
            match = re.match(hashnav_pattern, li)
            if match:
                links.remove(li)

        return links

    def _fully_qualify_links(self, links):
        """determine if a link is fully qualified with
        the correct protocol/scheme and domain name,
        if not then prepend with the base URL
        """
        print('initial links:', links)

        links_to_keep = []
        parse_page_url = urlparse.urlparse(self.url)

        for link_url in links:
            parse_url = urlparse.urlparse(link_url)
            scheme = parse_url.scheme
            hostname = parse_url.hostname

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

                # reconstruct the fully qualified url from:
                # scheme, netloc (host / domain), path, params, query, fragment)
                parse_url = urlparse.urlunparse((scheme, hostname, parse_url.path, '', '', ''))

                if parse_url.scheme == parse_page_url.scheme and parse_url.hostname == parse_page_url.hostname:
                    # "Note that this means that all URLs listed in the Sitemap must use the same protocol...
                    # and reside on the same host as the Sitemap." - http://www.sitemaps.org/protocol.html
                    links_to_keep.append(parse_url.geturl())

        print('keep: %s' % links)
        return links

    def _parse_links(self):
        """use LinksHTMLParser to extract hrefs from page"""
        html = self.content
        parser = self.LinksHTMLParser()
        parser.feed(html)
        parsed_links = parser.close()
        return parsed_links

    def _warn_404s(self, links):
        """
        TODO
        warn the consumer about 404 Not Found pages
        note: does not remove the link
        """
        _session = Session()

        for link_url in links:
            response = _session.get(link_url)
            status_code = response.status_code

            if status_code == requests.codes.NOT_FOUND:
                status_by_code(status_code)
                #logging.getLogger('verbose').warn()

    @property
    def links(self):
        """anchors in the current page content"""
        links = self._parse_links()

        # TODO refactor to avoid multiple loops?
        #links = self._warn_404s(links)
        links = self._remove_hashnavs(links)
        links = self._fully_qualify_links(links)

        return links
