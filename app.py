# from http://docs.python.org/2/library/wsgiref.html
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

from wsgiref.util import setup_testing_defaults

class ConnectionContent(object):
	
	def __init__(self):
		self.content = ""
		
	def send(self, data):
		self.content += data
		
	def get(self):
		return self.content

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
	setup_testing_defaults(environ)
	
	request_type = environ["REQUEST_METHOD"]
	path = environ["PATH_INFO"]
	querystring = environ["QUERY_STRING"]
	content_type = environ["CONTENT_TYPE"]
	content_length = environ["CONTENT_LENGTH"]
	wsgi_input = environ["wsgi.input"]
	
	print "Request Method",request_type
	print "Path",path
		
	parsed_path = urlparse(path)
	conn = ConnectionContent()
	
	if request_type == "POST":
		if("application/x-www-form-urlencoded" == content_type):
			handle_post_request(path, wsgi_input, conn)
		elif("multipart/form-data"  == content_type):
			fs_environ = {"REQUEST_METHOD":"POST"};
			fieldstorage_payload = cgi.FieldStorage(fp=StringIO.StringIO(wsgi_input), headers=headers_dict, environ=fs_environ)
			handle_multipart_post_request(path, fieldstorage_payload, conn)
		else:
			handle_get_request("2929239849284.html","",conn)
			#@comment should refactor to a send 404 method
			
	elif request_type == "GET":
		handle_get_request(path, parsed_path, conn)
	else:
		handle_get_request("2929239849284.html","",conn)
		#@comment should refactor to a send 404 method
		
	status = '200 OK'
	headers = [('Content-type', 'text/plain')]

	start_response(status, headers)

	ret = ["%s: %s\n" % (key, value) for key, value in environ.iteritems()]
	ret.insert(0, "This is your environ.  Hello, world!\n\n")
	
	return conn.get()

def handle_multipart_post_request(path, payload, conn):
	if(path == '/submit'):
		form_handle_submit(payload.getvalue("'ccn'"),payload.getvalue("'ssn'"),conn)
	else:
		conn.send(http_404_header())
		conn.send("bad form")
	
	
def handle_post_request(path, payload, conn):

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
	
	#path = dirname + path
	
	loader = jinja2.FileSystemLoader(dirname + "templates")
	env = jinja2.Environment(loader=loader,autoescape=True)
	
	print "Path:",path
	
	try:
		template = env.get_template(path)
		html = template.render()
		conn.send(http_header())
		conn.send(html)
	except:
		template = env.get_template("404.html")
		conn.send(http_404_header()) # Could not find file to serve
		conn.send(template.render())
		
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
	
def make_app():
    return simple_app
