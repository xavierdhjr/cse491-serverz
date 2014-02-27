#!/usr/bin/env python

#This is directly ripped from github.com/MaxwellGBrown

import random
import socket
import time
from urlparse import urlparse, parse_qs

## for the new POST request handling
from StringIO import StringIO
import cgi

## for the templates
import jinja2
import os

## for the wsgi app
from app import make_app## other apps#import quixote
#from quixote.demo.altdemo import create_publisher #login demo#import imageapp #image application
from wsgiref.validate import validator
_quixote_app = Nonedef make_quixote_app():	global _quixote_app		if(_quixote_app is None):		p = create_publisher()		_quixote_app = quixote.get_wsgi_app()			return _quixote_app	_image_app = Nonedef make_image_app():	global _image_app			if(_image_app is None):		imageapp.setup()		p = imageapp.create_publisher()		_image_app = quixote.get_wsgi_app()			return _image_app	
##
## HANDLE CONNECTION DEFINITION
##
def handle_connection(conn, environ):

	# Start reading in data from the connection
	read = conn.recv(1)
	while read[-4:] != '\r\n\r\n':
		read += conn.recv(1)

	# Parse headers
	request, data = read.split('\r\n',1)

	headers = {}
	for line in data.split('\r\n')[:-2]:
		k, v = line.split(': ',1)
		headers[k.lower()] = v

	# parse path and query string as urlparse object
	# parsed_url[2] = path, parsed_url[4] = query string
	parsed_url = urlparse(request.split(' ', )[1])

	environ['PATH_INFO'] = parsed_url[2]
	environ['QUERY_STRING'] = parsed_url[4]

	# Handle reading of POST data
	content = ''
	if request.startswith('POST '):
		environ['REQUEST_METHOD'] = 'POST'
		environ['CONTENT_LENGTH'] = headers['content-length']
		environ['CONTENT_TYPE'] = headers['content-type']
		# read the remaining data from http request to construct wsgi.input
		while len(content) < int(headers['content-length']):
			content += conn.recv(1)
	else:
		environ['REQUEST_METHOD'] = 'GET'
		environ['CONTENT_LENGTH'] = 0	if('cookie' in headers):		environ['HTTP_COOKIE'] = headers['cookie']

	#this is required by WSGI standards				  
	environ['CONTENT_LENGTH'] = str(environ['CONTENT_LENGTH']) 

	environ['wsgi.input'] = StringIO(content)



	def start_response(status, response_headers):
		conn.send('HTTP/1.0 %s\r\n' % status)
		for header in response_headers:
			conn.send('%s: %s\r\n' % header)
		conn.send('\r\n')

	# make the app	application = make_app()	
	response_html = application(environ, start_response)
	for html in response_html:
		conn.send(html)

	# close the connection
	conn.close()


def get_server_environ(port = 9999):
	environ = {}
	
	environ['SERVER_NAME'] = "localhost"
	environ['SERVER_PORT'] = str(port)
	environ['wsgi.version'] = (1,0)
	environ['wsgi.errors'] = StringIO()
	environ['wsgi.multithread'] = False
	environ['wsgi.multiprocess'] = False
	environ['wsgi.run_once'] = False
	environ['wsgi.url_scheme'] = 'http'
	environ['SCRIPT_NAME'] = ""
	
	return environ


##
## MAIN FUNCTION DEFINITION
##

def main(socket_module = socket):
	s = socket_module.socket()         # Create a socket object
	host = "localhost" # Changed to localhost because my machine throws exceptions at getfqdn for some reason
	port = random.randint(8000, 9999)
	s.bind((host, port))        # Bind to the port
	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)
	s.listen(5)                 # Now wait for client connection.
	print 'Entering infinite loop; hit CTRL-C to exit'
	
	# Some initial information about the server
	
	environ = get_server_environ(port)
	
	while True:
		# Establish connection with client.
		c, (client_host, client_port) = s.accept()
		print 'Got connection from', client_host, client_port
		# handle connection to serve page
		handle_connection(c, environ)


##
## RUN MAIN
##

if __name__ == '__main__':
    main()