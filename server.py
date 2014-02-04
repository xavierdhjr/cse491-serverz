#!/usr/bin/env python
import random
import socket
import time
import os
import urlparse
from urlparse import urlparse
from urlparse import parse_qs

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
	request = conn.recv(1000)
	
	request_components = request.split(' ')
	request_type = 'text/html'
	path = '/'

	if len(request_components) > 0:
		request_type = request.split(' ')[0]
	if len(request_components) > 1:
		path = request.split(' ')[1]

	headers_start = request.index('\r\n')

	parsed_path = urlparse(path)
	print "Request Information ----------"
	print "Path: " + path
	print "Type: " + request_type
	print "Params: " + parsed_path.params
	print "Query: " + parsed_path.query
	
	if request_type == "POST":
		request_payload = request.split('\r\n\r\n')[1]
		handle_post_request(path, request_type, request_payload, conn)
	elif request_type == "GET":
		handle_get_request(path, parsed_path, conn)
	
		
	conn.close()

def handle_post_request(path, type, payload, conn):

	if(path == '/submit'):
		form_data = parse_qs(payload)
		form_handle_submit(form_data["ccn"][0],form_data["ssn"][0],conn)
	else:
		conn.send(http_404_header())
		conn.send("bad form")
	
#didn't refactor the main function into many page functions
#because I felt like this was cooler
#I did however do it for the GET form
def handle_get_request(path, parsed_path, conn):

	if(path.split('?')[0] == "/submit"):
		form_data = parse_qs(parsed_path.query)
		form_handle_submit(form_data["ccn"][0],form_data["ssn"][0],conn)
		return
		
		
	if path[len(path) - 1] == '/':
		path = path + "index.html"
	if path[0] == '/':
		path = path[1:]
		
	dirname, filename = os.path.split(os.path.abspath(__file__))
	dirname = dirname + "\\"
	
	path = dirname + path
	
	try:
		with open(path, "r") as myfile:
			data = myfile.read()
			conn.send(http_header())
			conn.send(data)
	except IOError:
		with open(dirname + "404.html", "r") as myfile:
			data = myfile.read()
			conn.send(http_404_header()) # Could not find file to serve
			conn.send(data)
		
	print 'request handled'

#spits back out a response for a form submission
def form_handle_submit(ccn,ssn,conn):
	conn.send(http_header())

	response = "<html><body>Thanks. You have won. Your information: " + \
				"<br/>CC:{ccn} <br/>SSN:{ssn} " +  \
				"<br/><img src='http://bhpmss.org/yahoo_site_admin/assets/images/money.135143522.jpg'/>" + \
				"</body></html>"
	response = response.replace("{ccn}", ccn)
	response = response.replace("{ssn}", ssn)
	conn.send(response)

	return
	
def http_header():
	return 'HTTP/1.0 200 OK\r\n' + \
			'Content-type: text/html\r\n' + \
			'\r\n'
def http_404_header():
	return 'HTTP/1.0 404 Not found\r\n' + \
					'Content-type: text/html\r\n' + \
					'Connection: close\r\n' + \
					'\r\n'
	
if __name__ == '__main__':
   main()
