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