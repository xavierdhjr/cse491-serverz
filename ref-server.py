#! /usr/bin/env python
import socket
import random
from wsgiref.simple_server import make_server

#from app import make_app

## other apps
import quixote
#from quixote.demo.altdemo import create_publisher #login demo
import imageapp #image application

#testing quixote

_the_app = None
def make_app():
	global _the_app
	
	if _the_app is None:
		imageapp.setup()
		p = imageapp.create_publisher()
		p.is_thread_safe = True
		_the_app = quixote.get_wsgi_app()
		
	return _the_app


the_wsgi_app = make_app()

host = "localhost" #socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
httpd = make_server('', port, the_wsgi_app)
print "Serving at http://%s:%d/..." % (host, port,)
httpd.serve_forever()
