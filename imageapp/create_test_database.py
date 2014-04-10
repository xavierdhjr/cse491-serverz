import sqlite3 as sqlite
from database import Database
import os

def rel_name(filename):
	dir = os.path.dirname(__file__)
	return os.path.join(dir,filename)

def insert_image(cursor, filename, date):
	fp = open(filename,'rb')
	data = fp.read()
	
	cursor.execute('''
		INSERT INTO images (Data, DTSInserted)
		VALUES (?,?)
	''',(sqlite.Binary(data),date))

	id = cursor.lastrowid
	
	print "Inserted image ",id,filename
	
	return id
	
db = Database('test_imageapp.db')

conn = db.connect()
conn.text_factory = bytes

c = conn.cursor()

c.execute('''
	CREATE TABLE images
	(Id integer PRIMARY KEY AUTOINCREMENT, Data blob, DTSInserted text)
''')
c.execute('''
	CREATE TABLE image_comments
	(Id integer PRIMARY KEY AUTOINCREMENT, ImageId integer, Content text, DTSInserted text)
''')

conn.commit()

insert_image(c, rel_name("tux.png"),"2013-10-07 08:23:19.120")
insert_image(c, rel_name("dice.png"),"2013-10-07 08:23:19.120")

conn.commit()
conn.close()
