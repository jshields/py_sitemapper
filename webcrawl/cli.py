"""Command Line Interface for web crawler and sitemap generator"""
import argparse
from crawl import Session
from sitemap import Sitemap

# driver functions and Command Line Interface routines
def crawl_routine():
	pass

def commandline_args_setup():
    parser = argparse.ArgumentParser(description='CLI web crawler that gathers links and optionally outputs a sitemap.')
    #parser.add_argument('--sitemap', action='',
    #               help='Option to store sitemap file')
    args = parser.parse_args()
    return args
    
    

def main():
	"""main driver, providing Command Line Interface to the application"""
	args = commandline_args_setup()

	#raw_input('What is the URL of the site you would like to crawl? e.g. http://www.example.com')
	base_url = 'http://jshields.github.io'


	#if args.sitemap:
	#print('sitemap file will be generated at: %s' % args.sitemap)
	yorn = raw_input('Continue with the program? Y/N\n').lower()

	if yorn in ('yes', 'y'):
    	crawl_routine()
    elif yorn in ('no', 'n'):
        print('Stopping')
        exit()
    else:
        print('Sorry, I didn\'t recognize your answer')
        #prompt()


if __name__ == '__main__':
	main()
