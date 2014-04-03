# __init__.py is the top level file in a Python package.

from apps import QuotesApp

def make():
	quotes_app = QuotesApp('./quotes/quotes.txt', './quotes/html')
	return quotes_app

