"""cli module: Command Line Interface for sitemap generator"""
import sys
import argparse
import logging

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
    verbose_opt = args.verbose
    if verbose_opt:
        # set the root logger to show info messages
        logging.getLogger('').setLevel(logging.INFO)
        # setup a logging handler for the command line
        console = logging.StreamHandler()  # stream=sys.stdout
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(funcName)s: %(message)s')
        console.setFormatter(formatter)
        # add the handler to the verbose logger
        verbose = logging.getLogger('verbose')
        verbose.addHandler(console)
        verbose.info('Running verbose.')

    import ipdb
    ipdb.set_trace()

    base_url = args.base_url

    session = parse.Session(base_url)
    html = session.try_get_html(base_url)
    page = parse.Page(base_url, html)

    #logging.getLogger('verbose').info()
    verbose.info(page.content)

    links = page.links

    verbose.info(links)

    # store the file if opted
    sm = Sitemap(links)
    sm_arg = args.sitemap
    if sm_arg:
        sm.export(sm_arg)

if __name__ == '__main__':
    main()
