# py_sitemapper
Simple hypertext and hyperlink web crawler that outputs a `sitemap.xml` file.

URL parameters, query string, and document fragment identifier (hash navigation) do not currently carry to the output sitemap file.

Compatibility: Python 2.7+

Requires `requests` module: `pip install requests`

Example: `python cli.py http://jshields.github.io/showcase/sitemapper_target/home.htm`

## How it Works:
 - Make a request to a URL to get its markup.
 - Search the HTML for anchor tags and retrieve their hypertext references / link URLs.
 - Appropriately filter and save those links in sitemap file format.
 - Future enhancements: warn users about 404 Not Found links picked up by the crawler.

#### Resources:
- [http://www.sitemaps.org/protocol.html](http://www.sitemaps.org/protocol.html)
- [https://support.google.com/webmasters/answer/183668#sitemapformat](https://support.google.com/webmasters/answer/183668#sitemapformat)
