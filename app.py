#! /usr/bin/env python
#heavy inspiration (some code direclty) from github.com/leflerja

import cgi
import os
import jinja2
import sys
import urllib
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from wsgiref.simple_server import make_server

class Application(object):
	def __call__(self, environ, start_response):
	
		if(environ["PATH_INFO"] == "/file"):
			return self.temp_serve_file(environ, start_response)
		elif(environ["PATH_INFO"] == "/image"):
			return self.temp_serve_image(environ, start_response)
	
		if(environ["REQUEST_METHOD"] == "POST"):
			return self.handle_post(environ, start_response)
		elif(environ["REQUEST_METHOD"] == "GET"):
			return self.handle_get(environ, start_response)
		else:
			return self.handle_get(environ, start_response)
			
	def temp_serve_image(self, environ, start_response):
		dirname, filename = os.path.split(os.path.abspath(__file__))
		dirname = dirname + "\\"
		
		fp = open(dirname + "doge.jpg", "rb")
		data = fp.read()

		fp.close()
	
		start_response("200 OK", [('Content-type', "image/jpeg")])
		return [data]
		
	def temp_serve_file(self, environ, start_response):
		dirname, filename = os.path.split(os.path.abspath(__file__))
		dirname = dirname + "\\"
		
		fp = open(dirname + "hello_world.txt", "r")
		data = fp.read()
		fp.close()
		
		start_response("200 OK", [('Content-type', "text/plain")])
		return [data]

	def handle_get(self, environ, start_response):
		params = parse_qs(environ['QUERY_STRING'])
		
		result = self.render_page(environ["PATH_INFO"], params)
		
		start_response(result["status"], [('Content-type', result["content-type"])])
		return [result["page"]]
		
	def handle_post(self, environ, start_response):
		headers = {}
		params = {} 
		for k, v in environ.iteritems():
			headers['content-type'] = environ['CONTENT_TYPE']
			headers['content-length'] = environ['CONTENT_LENGTH']
			fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
								headers=headers, environ=environ)
			params.update({x: [fs[x].value] for x in fs.keys()})
		result = self.render_page(environ["PATH_INFO"], params)
		start_response(result["status"], [('Content-type', result["content-type"])])
		
		return [result["page"]]
		
	def render_page(self, path, params):
		rendered_page = ""
		status = "200 OK"
		content_type = "text/html"
		path = path[1:].split("?")[0]
		
		if(path == ""):
			path = "index"
		
		print "Path:",path
		
		dirname, filename = os.path.split(os.path.abspath(__file__))
		dirname = dirname + "\\"
			
		loader = jinja2.FileSystemLoader(dirname + "templates")
		env = jinja2.Environment(loader=loader,autoescape=True)
		
		try:
			template = env.get_template(path + ".html")
			html = template.render(params)
			rendered_page += html
		except jinja2.TemplateNotFound:
			template = env.get_template("404.html")
			rendered_page += template.render(params)
			status = "404 Not Found"
		except jinja2.TemplateSyntaxError:
			template = env.get_template("500.html")
			rendered_page += template.render(params)
			status = "500 Internal Server Error"
			print "Syntax Error on", path
		
			
		return { 
			"page" : str(rendered_page)
			, "status": status
			, "content-type": content_type 
			}
	
def make_app():
    return Application()
	