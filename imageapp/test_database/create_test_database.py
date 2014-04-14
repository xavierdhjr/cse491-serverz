import sqlite3 as sqlite
from database import Database
import os

def rel_name(filename):
	dir = os.path.dirname(__file__)
	return os.path.join(dir,filename)

def insert_image(cursor, filename, date):
	if filename is not None:
		try:
			fp = open(filename,'rb')
			data = fp.read()
			cursor.execute('''
				INSERT INTO images (Name, Data, DTSInserted)
				VALUES (?, ?,?)
			''',(filename,sqlite.Binary(data),date))
		except IOError:
			cursor.execute('''
				INSERT INTO images (Name, Data, DTSInserted)
				VALUES (?, ?,?)
			''',(filename,sqlite.Binary(filename),date))
	else:
		cursor.execute('''
			INSERT INTO images (Name, Data, DTSInserted)
			VALUES (?, ?,?)
		''',(filename,"",date))
	id = cursor.lastrowid
	
	print "Inserted image ",id,filename
	
	return id
	
db = Database('test_imageapp.db')

conn = db.connect()
conn.text_factory = bytes

c = conn.cursor()

c.execute('''
	CREATE TABLE images
	(Id integer PRIMARY KEY AUTOINCREMENT, Data blob, Name text, DTSInserted text)
''')

conn.commit()

insert_image(c, rel_name("tux.png"),"2014-4-09 12:00:00.000")
insert_image(c, rel_name("dice.png"),"2014-4-09 12:00:01.000")
insert_image(c, rel_name("quack.png"),"2014-4-09 12:00:03.000")
insert_image(c, rel_name("zig.png"),"2014-4-09 12:00:04.000")
insert_image(c, rel_name("time.jpg"),"2014-4-09 12:00:05.000")
insert_image(c, rel_name("kitten.jpg"),"2014-4-09 12:00:06.000")
insert_image(c, rel_name("trip.jpg"),"2014-4-09 12:00:07.000")
insert_image(c, rel_name("unce.gif"),"2014-4-09 12:00:08.000")
insert_image(c, rel_name("morty.gif"),"2014-4-09 12:00:09.000")
insert_image(c, rel_name("beans.jpg"),"2014-4-09 12:00:10.000")
insert_image(c, None,"2014-4-09 12:00:12.000")
insert_image(c, "Invalid","2014-4-09 12:00:12.000")
insert_image(c, rel_name("goku.png"),"2014-4-09 12:00:11.000")
insert_image(c, rel_name("sonic.gif"),"2014-4-09 12:00:09.000")
insert_image(c, rel_name("ironman.jpg"),"invalid time")
insert_image(c, rel_name("titus.jpg"),"2014-4-10 12:00:13.000")
insert_image(c, rel_name("xavier.jpg"),"1991-12-21 03:00:20.000")
insert_image(c, rel_name("xavier.jpg"),"1991-12-21 03:00:21.000")
insert_image(c, rel_name("xavier.jpg"),"1991-12-21 03:00:22.000")
insert_image(c, rel_name("xavier.jpg"),"1991-12-21 03:00:23.000")

conn.commit()
conn.close()
