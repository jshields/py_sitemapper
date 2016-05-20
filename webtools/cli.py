"""cli module: Command Line Interface for sitemap generator"""
# external modules
import sys
import argparse
import logging
# project modules
import parse
from sitemap import Sitemap, DEFAULT_SITEMAP_NAME


def commandline_args_setup():
    """prepare the arguments that can be
    input from the command line
    """
    parser = argparse.ArgumentParser(
        description=('CLI webpage parser that gathers links '
                     'and optionally outputs a sitemap.'
                     )
        )
    parser.add_argument('--base-url', '-B', action='store',
                        required=True,
                        help='Base URL to parse.')
    parser.add_argument('--sitemap-dest', '-S', action='store',
                        required=False,
                        default=DEFAULT_SITEMAP_NAME,
                        help=('Option to save sitemap file at '
                              'a different destination. '
                              'A sitemap.xml is saved in the '
                              'current directory by default.'
                              )
                        )
    parser.add_argument('--verbose', '-V', action='store_true',
                        help='Verbose output of runtime information.')
    args = parser.parse_args()
    return args


def _prompt_sitemap_save(site_url, filepath):
    """Specialized prompt for the user to confirm that
    they are going to save a sitemap file.

    Args:
        site_url: The website that the sitemap file is for.

        filepath: The path where the sitemap file will be saved.
    """
    print(
          ('You are about to save a sitemap file for {site},\n'
           'at {path}').format(site=site_url, path=filepath)
          )
    user_resp = raw_input('Continue? Y or N\n').lower()

    if user_resp not in ('y', 'n'):
        print('I didn\'t recognize that response.')
        _prompt_sitemap_save(site_url, filepath)

    if user_resp == 'y':
        print('Saving.')
        return True

    print('Exiting.')  # we could register an exit message instead
    return False


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

    import ipdb
    ipdb.set_trace()

    base_url = args.base_url
    session = parse.Session()
    html = session.html_at_url(base_url)

    # this web page is defined as a URL and some HTML
    page = parse.Page(base_url, html)
    logging.getLogger('verbose').info(page.content)

    links = page.links
    logging.getLogger('verbose').info(links)

    # store the file if opted
    sm_arg = args.sitemap_dest
    to_save = _prompt_sitemap_save(base_url, sm_arg)
    if to_save:
        sm = Sitemap(links)
        sm.export(sm_arg)

# this lets us run from the command line
# without making the module unsafe to import
if __name__ == '__main__':
    main()
