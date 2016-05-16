# py_sitemapper
Work In Progress. Simple hypertext and hyperlink web crawler that outputs a sitemap file.

URL parameters, query string, and document fragment identifier (hash navigation) do not currently carry to the output sitemap file.

Compatibility: Python 2.7+

Example: `python cli.py --base-url http://jshields.github.io/showcase/sitemapper_target/home.htm`

##Agenda:
 - Make a request to a URL
 - Search HTML for anchor tags and retrieve their hypertext references
 - Index references that are internal to the domain of the requested site

####Resources:
- [http://www.sitemaps.org/protocol.html](http://www.sitemaps.org/protocol.html)
- [https://support.google.com/webmasters/answer/183668#sitemapformat](https://support.google.com/webmasters/answer/183668#sitemapformat)
