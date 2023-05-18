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
			log.error('Cannot connect to database {}. Raised exception {}.'.format(self.db_file, e))
			return False

	def createAnimalTableIfNotExists(self):
		try:
			sql = """CREATE TABLE IF NOT EXISTS animals (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL UNIQUE,
				superhero_names TEXT NOT NULL,
				hits INTEGER DEFAULT 1,
				created datetime default current_timestamp,
				updated datetime default current_timestamp)"""
			self.cursor.execute(sql)
			self.connection.commit()
			sql = 'CREATE INDEX animal_names_idx ON animals(name)'
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot create table. Raised exception {}.'.format(e))
			return False

	def checkIfAnimalExists(self, name):
		try:
			sql = """SELECT 1 FROM animals WHERE name GLOB '{}'""".format(name)
			self.cursor.execute(sql)
			data = self.cursor.fetchone()
			if data != None:
				return True
			return False
		except Exception as e:
			log.error('Cannot check if animal exists. Raised exception {}.'.format(e))
			return False

	def insertAnimal(self, name, superheroNames):
		try:
			sql = """INSERT INTO animals (name,superhero_names) VALUES (
				'{}',
				'{}')""".format(name, superheroNames)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot insert animal {}. Raised exception {}.'.format(name, e))
			return False