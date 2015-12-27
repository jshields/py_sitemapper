"""Command Line Interface for sitemap generator"""
import sys
import argparse
import logging
import parse # Session, Page
from sitemap import Sitemap

def commandline_args_setup():
    """prepare the options input from the command line args"""
    parser = argparse.ArgumentParser(description='CLI webpage parser that gathers links and optionally outputs a sitemap.')
    parser.add_argument('--base-url', '-B', action='store', required=True,
                  help='Base URL to parse.')
    parser.add_argument('--sitemap', '-S', action='store', default=False,
                       help='Option to store sitemap file.')
    parser.add_argument('--verbose', '-V', action='store_true',
                        help='Verbose output of runtime information.')
    args = parser.parse_args()
    return args

def main():
    """main driver"""
    args = commandline_args_setup()
    verbose = args.verbose

    # handle verbose option
    if verbose:
        # setup a logging handler for the command line
        console = logging.StreamHandler(stream=sys.stdout)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(funcName)s: %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)

    base_url = args.base_url

    session = parse.Session(base_url)
    html = session.try_get_html(base_url)
    page = parse.Page(html)

    logging.info(page.content)

    links = page.links

    #if verbose:
    logging.info(links)

    # store the file if opted
    sm = Sitemap(links)
    sm_arg = args.sitemap
    if sm_arg:
        sm.export(sm_arg)

if __name__ == '__main__':
    main()
