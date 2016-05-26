"""parse module: parse web content"""
import logging
import re
import urlparse
from HTMLParser import HTMLParser

import requests


class Session(object):

    """requests Session wrapper"""

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


class Page(object):

    """page of a web site"""

    def __init__(self, url, content):
        """Page init

        Args:
            url (str): URL to serve as static information
                about this page's location.
            content (): the HTML content of the page
        """

        self.url = url
        self.content = content

    def _parse_links(self):
        """use LinksHTMLParser to extract hrefs from page"""
        html = self.content
        parser = LinksHTMLParser()
        parser.feed(html)
        return parser.close()

    def _remove_hashnavs(self, links):
        """only return URLs - not hash navs"""
        hashnav_pattern = r'^#'
        to_remove = []

        for li in links:
            # hashnav as href or at end of path
            match = re.match(hashnav_pattern, li)
            if match or urlparse.urlparse(li).fragment:
                logging.getLogger('verbose').info('Removing {link}'.format(link=li))
                to_remove.append(li)

        # now that we're done looping over the list,
        # we can modify it safely
        for li in to_remove:
            links.remove(li)

        return links

    def _fully_qualify_links(self, links):
        """determine if a link is fully qualified with
        the correct protocol/scheme and domain name,
        if not then prepend with the base URL
        """
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

                # prepend a potentially relative URI with the path
                # of the page from where it is linked
                parse_url_path = urlparse.urljoin(parse_page_url.path, parse_url.path)

                # reconstruct the fully qualified url from:
                # scheme, network location, path, params, query, fragment)
                # cycling an unparsed string back into a ParseResult
                parse_url_update = urlparse.urlparse(
                    urlparse.urlunparse(
                        (scheme,
                         hostname,
                         parse_url_path,
                         '',  # params
                         '',  # query
                         ''   # fragment
                         )
                    )
                )

                if (parse_url_update.scheme == parse_page_url.scheme and
                        parse_url_update.hostname == parse_page_url.hostname):
                    # "Note that this means that all URLs listed in the
                    # Sitemap must use the same protocol...
                    # and reside on the same host as the Sitemap."
                    # - http://www.sitemaps.org/protocol.html
                    links_to_keep.append(parse_url_update.geturl())

        return links_to_keep

    def _remove_duplicates(self, sequence):
        """
        Keeping the order of the sequence,
        while removing duplicates.
        (http://stackoverflow.com/questions/480214/
        how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order)
        """
        seen = set()
        seen_add = seen.add
        return [x for x in sequence if not (x in seen or seen_add(x))]

    @property
    def links(self):
        """anchors in the current page content"""
        links = self._parse_links()
        links = self._remove_hashnavs(links)
        links = self._fully_qualify_links(links)
        links = self._remove_duplicates(links)
        # TODO links = self._warn_404s(links)

        return links
