import sqlite3
import logging

log = logging.getLogger(__name__)

class Database(object):

	def __init__(self, db_file):
		self.db_file = db_file
		self.connectToDb()

	def __del__(self):
		self.cursor.close()
		self.connection.close()

	def connectToDb(self):
		try:
			self.connection = sqlite3.connect(self.db_file)
			self.cursor = self.connection.cursor()
			return True
		except Exception as e:
			log.error('Cannot connect to database {}, raised exception {}.'.format(self.db_file, e))
			return False

	def createAnimalTableIfNotExists(self):
		try:
			sql = 'CREATE TABLE IF NOT EXISTS animals (Id INTEGER PRIMARY KEY, Name TEXT NOT NULL UNIQUE, Names BLOB)'
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot create table. Raised exception {}.'.format(e))
			return False