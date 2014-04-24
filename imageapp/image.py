# image handling API
import database

	
class ImageRepository(object):
	def __init__(self, database_module = database.Database('imageapp.db')):
		self.db_module = database_module

	#returns the newest row in the table
	def get_latest(self):
		return self.db_module.get_recent_image()
	
	#returns a response obj
	# {success, message, data}
	def get_image(self, id):
		return self.db_module.get_db_image(id)
		
	def get_image_meta(self, id):
		return self.db_module.get_db_image_meta(id)
	
	#returns a response obj
	# {success, message, data}
	def add_image(self, data, title, description,type):
		return self.db_module.add_db_image(data, title, description,type)
	
	#returns a number
	def count_images(self):
		return self.db_module.get_num_images()
	
	def get_comments_for_image(self, imageId):
		return self.db_module.get_comments_for_image(imageId)

	def add_comment_to_image(self, imageId, username, comment):
		return self.db_module.add_comment(imageId, username, comment)

images = ()
repository = ImageRepository()

def get_image_meta(imageId):
	return repository.get_image_meta(imageId)

def add_comment_to_image(imageId, usersname, comment):
	response = repository.add_comment_to_image(imageId, usersname, comment)
	if response["success"]:
		print "Successfully added comment."
	else:
		print response["message"]
		return -1

def get_comments_for_image(imageId):
	return repository.get_comments_for_image(imageId)

def add_image(data, title, description, type):

	response = repository.add_image(data, title, description, type)
	if response["success"]:
		print "Successfully added image"
	else:
		print response["message"]
		return -1

def get_image_count():
	return repository.count_images()

def get_image(num):
	response = repository.get_image(num)
	if(response["success"]):
		print "Successfully retrieved image ", num
		id, data, name, desc, type, date = response["data"]
		return data
	else:
		print "Failed to retrieve image ", num
		return None

def get_latest_image():
	#id, data, name, date = repository.get_latest()
	#print "Latest image id: ", id 
	return repository.get_latest()