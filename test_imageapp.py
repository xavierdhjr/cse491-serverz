import imageapp
import quixote
import imageapp.image
import imageapp.database
import os
import sys
import json

def test_imageapp_API_getstat_basic():
	environ = create_environ(path="/get_stat",qs="stat=basic")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert ('Content-Type','application/json') in headers, headers
	decoded_json = json.loads(html)
	assert "image_count" in decoded_json.keys() 
	
def test_imageapp_index():
	environ = create_environ(path="/")
	
	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h

	app = make_imageapp()
	response = app(environ, test_start_response)
	html = get_response_html(response)
	
	status, headers = d['status'], d['headers']
	
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert "Most Recent Image:" in html, "Didn't find 'Most Recent Image' text"

def test_imageapp_image_raw():
	environ = create_environ(path="/image_raw",qs="")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert ('Content-Type','image/png') in headers, headers
	assert len(html) > 50, "length wasnt greater than 50. Got length: %s" % len(html)
	
def test_imageapp_get_image_noparams():
	#should get latest image
	environ = create_environ(path="/get_image",qs="")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert ('Content-Type','image/png') in headers, headers
	assert len(html) > 50, "length wasnt greater than 50"
	
def test_imageapp_get_image():
	environ = create_environ(path="/get_image",qs="id=48")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert ('Content-Type','image/png') in headers, headers
	assert len(html) > 50, "length wasnt greater than 50"
		
def test_imageapp_get_image_invalid():
	environ = create_environ(path="/get_image",qs="id=-20")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert ('Content-Type','image/png') in headers, headers
	assert len(html) == 0, "Got content for allegedly invalid id? Content: %s" % html
	
def test_imageapp_upload():
	environ = create_environ(path="/upload_ajax")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	
def test_imageapp_upload():
	environ = create_environ(path="/upload")
	html, status, headers = webpage_setup(environ)
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	
def test_imageapp_image():
	environ = create_environ(path="/image")
	html, status, headers = webpage_setup(environ)
	
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert "Here is your image" in html, "'Here is your image' wasn't in the html."

def test_imageapp_browse():
	environ = create_environ(path="/browse")
	
	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h


	app = make_imageapp()
	response = app(environ, test_start_response)
	html = get_response_html(response)
	
	status, headers = d['status'], d['headers']
	
	assert "200 OK" == status, "Status wasnt 200 OK. Was %s" % status
	assert "All Images" in html, "Didn't find 'All Images'"
	
	
def test_repository_count_images():
	db_module = get_test_db()
	repository = imageapp.image.ImageRepository(db_module)
	
	images = repository.count_images()
	
	assert images == 2, "image count was %s" % images
	
def test_repository_get_latest():
	db_module = get_test_db()
	repository = imageapp.image.ImageRepository(db_module)
	
	id, data, date = repository.get_latest()
	
	#assumes 2 images in the test database
	assert id == 2, "ID was not 2. Was, %s" % id
	
def test_repository_get_image():
	db_module = get_test_db()
	repository = imageapp.image.ImageRepository(db_module)
	
	response = repository.get_image(1)
	
	assert response["success"] == True, "Get Image failed"
	id, data, dtsInserted = response["data"]
	assert id == 1, "Asked for ID 1, got ID %s" % id
	assert len(data) > 50, "Returned data: %s" % (str)(data)
		
	response = repository.get_image(2)
	
	assert response["success"] == True, "Get Image failed"
	id, data, dtsInserted = response["data"]
	assert id == 2, "Asked for ID 2, got ID %s" % id
	assert len(data) > 50, "Returned data: %s" % (str)(data)


## HELPERS ##

def webpage_setup(environ):
	d = {}
	def test_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h

	app = make_imageapp()
	response = app(environ, test_start_response)
	html = get_response_html(response)
	
	return (html, d['status'], d['headers'])
	
def create_environ(path="/",method="GET",qs=""):
	environ = {}
	environ['SERVER_NAME'] = "localhost"
	environ['SERVER_PORT'] = 9999
	environ['wsgi.version'] = (1,0)
	environ['wsgi.errors'] = sys.stderr
	environ['wsgi.multithread'] = False
	environ['wsgi.multiprocess'] = False
	environ['wsgi.run_once'] = False
	environ['wsgi.url_scheme'] = 'http'
	environ['SCRIPT_NAME'] = ""
	environ['wsgi.input'] = ""
	environ['PATH_INFO'] = path
	environ['REQUEST_METHOD'] = method
	environ['QUERY_STRING'] = qs
	
	return environ

_setup_complete = False
def make_imageapp():
	global _setup_complete
	if not _setup_complete:
		imageapp.setup()
		p = imageapp.create_publisher()
		_setup_complete = True
	return quixote.get_wsgi_app()
	
def get_test_db():
	return imageapp.database.Database("test_imageapp.db")

def get_response_html(response):
	content = ""
	for html in response:
		content += html
	return content