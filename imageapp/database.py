import sqlite3 as sqlite
import os

class Database(object):
	def __init__(self,database_file,working_dir=os.path.dirname(__file__)):
		self.file = database_file
		self.dir = working_dir
		
	def connect(self):
		dirname = self.dir
		database_path = os.path.join(dirname, self.file)
		conn = sqlite.connect(database_path)
		return conn
	
	def create_response(self,success = True, message = "", data = None):
		return {'success': success, 'data': data, 'message': message}

	def add_comment(self, imageId, username, comment):
		conn = self.connect()
		c = conn.cursor()
		
		c.execute('''
			INSERT INTO comments (ImageId, Username, Comment, DTSInserted)
			VALUES (?,?,?,DateTime('now'))
		''', (imageId, username, comment))
		conn.commit()
		conn.close()
			
		return self.create_response(True, "Success")
	
	def get_comments_for_image(self, imageId):
		conn = self.connect()
		c = conn.cursor()
		
		conn = self.connect()
		
		c = conn.cursor()
		c.execute('''
			SELECT * FROM comments WHERE ImageId = ?
		''', (imageId,))
		
		results = c.fetchall()
		
		conn.close()
		
		return results
		
	def add_db_image(self,data):
		conn = self.connect()
		conn.text_factory = bytes
		c = conn.cursor()
		
		c.execute('''
			INSERT INTO images (Data, DTSInserted)
			VALUES (?,DateTime('now'))
		''', (sqlite.Binary(data),))
		conn.commit()
		
		c.execute('''
			SELECT Data FROM images
			WHERE Id = ?
		''', (c.lastrowid,))
		
		retrieved_data, = c.fetchone()
		conn.close()
		
		return self.create_response(True, "")

	def get_db_image(self,id):
		conn = self.connect()
		
		conn.text_factory = bytes
		
		c = conn.cursor()
		c.execute('''
			SELECT * FROM images
			WHERE Id = ?
		''', (id,))
		
		result = c.fetchone()
		
		conn.commit()
		conn.close()
		
		if(result is None):
			return self.create_response(success=False,message="Could not fetch image id" + str(id))
		
		return self.create_response(data=result)

	def get_num_images(self):
		conn = self.connect()
		conn.text_factory = bytes
		
		c = conn.cursor()
		c.execute('''
			SELECT * FROM images
		''')
		
		results = c.fetchall()
		
		conn.close()
		
		return len(results)
		
	def get_recent_image(self):
		conn = self.connect()
		
		conn.text_factory = bytes

		c = conn.cursor()
		c.execute('''
			SELECT * FROM images
			ORDER BY Id DESC
		''')
		
		result = c.fetchone()
		
		return result

	