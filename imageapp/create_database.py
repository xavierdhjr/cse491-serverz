import database

import sqlite3 as sqlite
from database import Database
import os
	
db = Database('imageapp.db')

conn = db.connect()
c = conn.cursor()

c.execute('''
	CREATE TABLE images
	(Id integer PRIMARY KEY AUTOINCREMENT, Data blob, Title text, Description text, Type text, DTSInserted text)
''')
c.execute('''
	CREATE TABLE comments
	(Id integer PRIMARY KEY AUTOINCREMENT, ImageId integer, Username text, Comment text, DTSInserted text)
''')

conn.commit()
conn.close()
