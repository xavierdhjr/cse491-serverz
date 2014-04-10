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
		
	#returns a response obj
	# {success, message, data}
	def add_image(self, data):
		return self.db_module.add_db_image(data)
	
	#returns a number
	def count_images(self):
		return self.db_module.get_num_images()
	

images = ()
repository = ImageRepository()

def add_image(data):

	response = repository.add_image(data)
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
		id,data,date = response["data"]
		return data
	else:
		print "Failed to retrieve image ", num
		return None

def get_latest_image():
	id, data, date = repository.get_latest()
	return data