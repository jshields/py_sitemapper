"""cli module: Command Line Interface for sitemap generator"""
# external modules
import sys
import argparse
import logging
# project modules
import parse
from sitemap import Sitemap


def commandline_args_setup():
    """prepare the options input from the command line args"""
    parser = argparse.ArgumentParser(
        description='CLI webpage parser that gathers links and optionally outputs a sitemap.'
        )
    parser.add_argument('--base-url', '-B', action='store', required=True,
                        help='Base URL to parse.')
    parser.add_argument('--sitemap', '-S', action='store', default=False,
                        help='Option to save sitemap file at a relative path.')
    parser.add_argument('--verbose', '-V', action='store_true',
                        help='Verbose output of runtime information.')
    args = parser.parse_args()
    return args


def main():
    """main driver"""
    args = commandline_args_setup()

    # handle verbose option
    if args.verbose is True:
        # setup a logging handler to the command line
        console = logging.StreamHandler()  # stream=sys.stdout
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('{funcName}: {message}')  # TODO verify
        console.setFormatter(formatter)
        # add the handler to the verbose logger
        verbose = logging.getLogger('verbose')
        verbose.addHandler(console)
        verbose.info('Running verbose.')

    #import ipdb
    #ipdb.set_trace()

    base_url = args.base_url

    session = parse.Session(base_url=base_url)
    html = session.html_at_url(base_url)

    # this web page is defined as a URL and some HTML
    page = parse.Page(base_url, html)
    logging.getLogger('verbose').info(page.content)

    links = page.links
    logging.getLogger('verbose').info(links)

    # store the file if opted
    sm = Sitemap(links)
    sm_arg = args.sitemap
    if sm_arg:
        sm.export(sm_arg)

if __name__ == '__main__':
    main()
