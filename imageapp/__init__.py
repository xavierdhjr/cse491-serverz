# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

import os
import sys

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
	html.init_templates()

	dirname = os.path.dirname(__file__)
	dirname = os.path.join(dirname,"imageapp")
	
	path = os.path.join(dirname,'dice.png')

	some_data = open(path, 'rb').read()
	image.add_image(some_data)
    

def teardown():                         # stuff that should be run once.
    pass
