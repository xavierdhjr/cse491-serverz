import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
from quixote.http_request import parse_query
import os.path

from . import html, image

import json

class RootDirectory(Directory):
	_q_exports = []
	
	@export(name='')                    # this makes it public.
	def index(self):
		return html.render('index.html')

	@export(name='jquery')
	def jquery(self):
		dirname = os.path.dirname(__file__)
		dirname = os.path.join(dirname,"")
		jquery_path = os.path.join(dirname,'jquery-1.3.2.min.js')
		print jquery_path
		return open(jquery_path).read()

	@export(name='upload')
	def upload(self):
		return html.render('upload.html')

	@export(name='browse')
	def browse(self):
		return html.render('browse.html')
		
	@export(name='upload_receive')
	def upload_receive(self):
		print "upload receive start"
		request = quixote.get_request()
		print "got request"
		print request.form.keys()

		the_file = request.form['file']
		print "File FP:",the_file.fp
		print "dir",dir(the_file)
		print 'received file with name:', the_file.base_filename
		data = the_file.fp.read()

		image.add_image(data)
		the_file.close()
		return quixote.redirect('./')
		
	@export(name='upload2')
	def upload2(self):
		return html.render('upload2.html')

	@export(name='upload2_receive')
	def upload2_receive(self):
		request = quixote.get_request()
		print request.form.keys()

		the_file = request.form['file']
		print dir(the_file)
		print 'received file with name:', the_file.base_filename
		data = the_file.read(int(1e9))

		image.add_image(data)

		return html.render('upload2_received.html')

	@export(name='upload_ajax')
	def upload_ajax(self):
		return html.render('upload_ajax.html')

	@export(name='upload_ajax_receive')
	def upload_ajax_receive(self):
		request = quixote.get_request()
		print request.form.keys()

		the_file = request.form['file']
		print dir(the_file)
		print 'received file with name:', the_file.base_filename
		data = the_file.fp.read()

		image.add_image(data)

		response = quixote.get_response()
		response.set_content_type('image/png')
		return image.get_latest_image()

	@export(name='image')
	def image(self):
		request = quixote.get_request()
		query = request.get_query()
		fields = parse_query(query, quixote.DEFAULT_CHARSET)
		
		if "id" in fields:
			image_id = int(fields["id"])
		else:
			id, data, name, date = image.get_latest_image()
			image_id = id
			
		comments = []
		for comment_raw in image.get_comments_for_image(image_id):
			comments.append({"Username":comment_raw[2], "Comment":comment_raw[3], "Date":comment_raw[4]})
			
		image_data = image.get_image(image_id)
		if image_data is None or len(image_data) <= 0:
			return html.render('error.html')
		
		print "Comments",comments
		
		return html.render('image.html',{"comment_count":len(comments),"imageId":image_id,"comments":comments, "message":"OK"})
	
	@export(name='add_comment')
	def add_comment(self):
		request = quixote.get_request()
		imageId = request.form['imageId']
		username = request.form['username']
		comment = request.form['comment']

		image.add_comment_to_image(imageId, username, comment)
		
		return quixote.redirect('./image?id=' + imageId)
		
	@export(name='image_raw')
	def image_raw(self):
		response = quixote.get_response()
		response.set_content_type('image/png')
		id, data, name, date = image.get_latest_image()
		return data
		
	@export(name='get_image')
	def get_image(self):
		request = quixote.get_request()
		query = request.get_query()
		fields = parse_query(query, quixote.DEFAULT_CHARSET)
		
		response = quixote.get_response()
		response.set_content_type('image/png')
		
		if(len(fields) > 0 and "id" in fields):
			image_id = int(fields["id"])
			return image.get_image(image_id)
			
		return image.get_latest_image()

	@export(name='get_stat')
	def get_stat(self):
		request = quixote.get_request()
		query = request.get_query()
		fields = parse_query(query, quixote.DEFAULT_CHARSET)
		
		response = quixote.get_response()
		response.set_content_type('application/json')
		
		stats = {}
		
		def json_encode(data):
			return json.dumps(data)

		if("stat" in fields):
			stat_field = fields["stat"]
			
			if((str)(stat_field) == "basic"):
				stats['image_count'] = image.get_image_count()

		return json_encode(stats)
		