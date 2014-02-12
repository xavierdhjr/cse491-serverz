#!/usr/bin/env python
import cgitb
import cgi
import random
import socket
import time
import os
import jinja2
import sys
import urlparse
import StringIO
from urlparse import urlparse
from urlparse import parse_qs
from mimetools import Message

from app import make_app

def main():
	s = socket.socket()         # Create a socket object
	host = 'localhost'#socket.getfqdn() # Get local machine name
	port = random.randint(8000, 25000)
	s.bind((host, port))        # Bind to the port

	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)

	s.listen(5)                 # Now wait for client connection.

	print 'Entering infinite loop; hit CTRL-C to exit'
	while True:
		# Establish connection with client.    
		c, (client_host, client_port) = s.accept()
		print 'Got connection from', client_host, client_port
		handle_connection(c)
		
def handle_connection(conn):

	print "Handling connection"
	partial_request = conn.recv(1)
	bytes_read = 0
	request = partial_request
	
	while '\r\n\r\n' not in request:
		bytes_read += 1
		partial_request = conn.recv(1)
		request = request + partial_request
	
		
	request_line, headers_alone = request.split('\r\n', 1)
	headers = Message(StringIO.StringIO(headers_alone))

	headers_dict = { "content-type" : "text/plain", "content-length":0 }
	for key in headers.keys(): #copy values into our own dict
		headers_dict[key] = headers[key];
		
	#print "headers",headers_dict
	
	print "Request:",request
	
	request_line = request.split(' ')
	request_type = request.split(' ')[0]
	path = request.split(' ')[1]
	#Note: write a test where the request line is empty?
	parsed_path = urlparse(path)
	wsgi_environ = {
		"PATH_INFO" : path,
		"REQUEST_METHOD" : request_type,
		"QUERY_STRING" : parsed_path.query,
		"CONTENT_TYPE" : headers_dict["content-type"],
		"CONTENT_LENGTH" : headers_dict["content-length"],
		"wsgi.input" : request.split('\r\n\r\n',1)[1]
	}
	
	the_wsgi_app = make_app()
	print "Created the WSGI app"

	def start_response(app_status, app_headers):
		print "App Headers", app_headers
		print "App Status", app_status
	
	conn.send(the_wsgi_app(wsgi_environ, start_response))

	conn.close()

if __name__ == '__main__':
   main()
