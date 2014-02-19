import app
import urllib
from StringIO import StringIO

#heavy inspiration from github.com/leflerja
#need to write more tests

def test_error():
    environ = {}
    environ['PATH_INFO'] = '/error'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.Application()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Error') != -1, text
    assert status == '404 Not Found'
    assert ('Content-type', 'text/html') in headers

def test_index():
    environ = {}
    environ['PATH_INFO'] = '/'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
		print "Headers", h

    test_app = app.Application()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Hello') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_get_querystring():
	environ = {}
	environ['PATH_INFO'] = '/submit'
	environ['REQUEST_METHOD'] = 'GET'
	environ['QUERY_STRING'] = 'ssn=999&ccn=888'
	environ['CONTENT_TYPE'] = 'text/html'

	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
		print "Headers", h

	test_app = app.Application()
	results = test_app(environ, test_start_response)

	text = "".join(results)
	status, headers = d['status'], d['headers']
    
	assert text.find('Your CCN') != -1, text
	assert text.find('999') != -1, text
	assert text.find('Your SSN') != -1, text
	assert text.find('888') != -1, text
	assert status == '200 OK'
	assert ('Content-type', 'text/html') in headers
	
def test_get_file():	
	environ = {}
	environ['PATH_INFO'] = '/file'
	environ['REQUEST_METHOD'] = 'GET'
	environ['CONTENT_TYPE'] = 'text/html'

	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
		print "Headers", h

	test_app = app.Application()
	results = test_app(environ, test_start_response)

	text = "".join(results)
	print "Results:",text
	status, headers = d['status'], d['headers']

	assert text.find("hello world") != -1, text
	assert status == '200 OK'
	assert ('Content-type', 'text/plain') in headers

def test_get_image():	
	environ = {}
	environ['PATH_INFO'] = '/image'
	environ['REQUEST_METHOD'] = 'GET'
	environ['CONTENT_TYPE'] = 'text/html'

	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
		print "Headers", h

	test_app = app.Application()
	results = test_app(environ, test_start_response)
	
	text = "".join(results)
	status, headers = d['status'], d['headers']

	assert status == '200 OK'
	assert ('Content-type', 'image/jpeg') in headers
	pass