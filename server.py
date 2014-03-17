#!/usr/bin/env python

import argparse
import sys
import random
import socket
from time import gmtime, strftime
from urlparse import urlparse, parse_qs

## for the new POST request handling
from StringIO import StringIO
import cgi

## for the templates
import jinja2
import os

## for the wsgi app
import app## other appsimport quixote
from quixote.demo.altdemo import create_publisher #login demoimport imageapp
from wsgiref.validate import validator

#### GLOBALS ####
# Setup should only one once in choose_app
_setup_complete = False

# Names of my apps that can be typed in
# to the command line
APP_QUIXOTE_ALTDEMO = "altdemo"
APP_QUIXOTE_IMAGEAPP = "image"
APP_MINE = "myapp"

# This list is used to check if an invalid 
# app was chosen.
APPS = [
	APP_QUIXOTE_ALTDEMO
	,APP_QUIXOTE_IMAGEAPP 
	,APP_MINE
]
#### END GLOBALS ####


parser = argparse.ArgumentParser(description='this is the beans!')
parser.add_argument('-A' \
	, metavar='application' \
	, nargs = '?' \
	, default = APP_MINE
	,help='What application should be run on this server.')
parser.add_argument('-p', metavar='port' \
	, nargs='?'
	, default=random.randint(8000,9999) \
	, type=int
	, help='What port the server should run on')

args = parser.parse_args()


# Accepts one of the above three strings
def choose_app(app_name):
	global _setup_complete 
	
	if(app_name == APP_MINE):
		return app.make_app()
	elif(app_name == APP_QUIXOTE_ALTDEMO):
		if not _setup_complete:
			p = create_publisher()
			_setup_complete = True
		return quixote.get_wsgi_app()
	elif(app_name == APP_QUIXOTE_IMAGEAPP):
		if not _setup_complete:
			imageapp.setup()
			p = imageapp.create_publisher()
			_setup_complete = True
		return quixote.get_wsgi_app()

def print_request_info(environ, conn):
	print "------------------"
	print "[" + environ['SELECTED_APP'] + "]", \
		strftime("%Y-%m-%d %H:%M:%S", gmtime()), \
		conn.getpeername(), \
		environ['REQUEST_METHOD'], \
		"-", \
		environ['PATH_INFO'] 
def print_response_info(status, headers):
	print '\tStatus',status
	print '\tHeaders',headers
	
##
## HANDLE CONNECTION DEFINITION
##
def handle_connection(conn, environ, selected_app = APP_MINE):

	# for print_request
	environ['SELECTED_APP'] = selected_app
	
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
	parsed_url = urlparse(request.split(' ', )[1])

	environ['PATH_INFO'] = parsed_url[2]
	environ['QUERY_STRING'] = parsed_url[4]
	# Handle reading of POST data
	content = ''
	
	if request.startswith('POST '):
		environ['REQUEST_METHOD'] = 'POST'
		environ['CONTENT_LENGTH'] = headers['content-length']
		environ['CONTENT_TYPE'] = headers['content-type']
		contentLength = int(environ['CONTENT_LENGTH'])	
		
		while len(content) < contentLength:
			received_content = conn.recv(contentLength)
			content += received_content
	else:
		environ['REQUEST_METHOD'] = 'GET'
		environ['CONTENT_LENGTH'] = 0	if('cookie' in headers):		environ['HTTP_COOKIE'] = headers['cookie']

	#this is required by WSGI standards				  
	environ['CONTENT_LENGTH'] = str(environ['CONTENT_LENGTH']) 

	environ['wsgi.input'] = StringIO(content)
	
	def start_response(status, response_headers):
		print_response_info(status, response_headers)
		conn.send('HTTP/1.0 %s\r\n' % status)
		for header in response_headers:
			conn.send('%s: %s\r\n' % header)
		conn.send('\r\n')

	print_request_info(environ, conn)
	# make the app	application = choose_app(selected_app)	
	response_html = application(environ, start_response)
	for html in response_html:
		conn.send(html)

	conn.close()

def get_server_environ(port = 9999, server_name = "localhost"):
	environ = {}
	
	environ['SERVER_NAME'] = server_name#"localhost"
	environ['SERVER_PORT'] = str(port)
	environ['wsgi.version'] = (1,0)
	environ['wsgi.errors'] = sys.stderr
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
	host = "localhost"#socket_module.getfqdn() 
	# Changed to localhost because my machine throws 
	# exceptions at getfqdn for some reason
	
	### PROGRAM ARGUMENTS ###
	port = args.p 
	selected_app = args.A
	###
	
	if selected_app not in APPS:
		print "Selected app was not valid:",selected_app
		exit()
	
	s.bind((host, port))        # Bind to the port
	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)
	s.listen(5)                 # Now wait for client connection.
	print 'Entering infinite loop; hit CTRL-C to exit'

	
	print "Using application", selected_app
	
	while True:
		# Some initial information about the server
		environ = get_server_environ(port, host)
		# Establish connection with client.
		c, (client_host, client_port) = s.accept()
		# handle connection to serve page
		handle_connection(c, environ, selected_app)


##
## RUN MAIN
##

if __name__ == '__main__':
    main()