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
			sql = 'CREATE INDEX IF NOT EXISTS animal_names_idx ON animals(name)'
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot create table. Raised exception {}.'.format(e))
			return False

	def getAnimalId(self, name):
		try:
			sql = """SELECT id FROM animals WHERE name GLOB '{}' LIMIT 1""".format(name)
			self.cursor.execute(sql)
			rows = self.cursor.fetchone()
			if rows != None:
				return rows[0]
			return 0
		except Exception as e:
			log.error('Cannot get animal with name: {}. Raised exception {}.'.format(name, e))
			return 0

	def getAnimalSuperheroNames(self, animalId):
		try:
			sql = """SELECT superhero_names FROM animals WHERE id = '{}' LIMIT 1""".format(animalId)
			self.cursor.execute(sql)
			rows = self.cursor.fetchone()
			if rows != None:
				return rows[0]
			return ""
		except Exception as e:
			log.error('Cannot get animal superhero names with id: {}. Raised exception {}.'.format(animalId, e))
			return ""

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

	def updateAnimal(self, animalId, superheroNames):
		try:
			sql = """UPDATE animals SET superhero_names = '{}',
			hits = hits + 1,
			updated = current_timestamp
			WHERE id = {}""".format(superheroNames, animalId)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot update animal with id: {}. Raised exception {}.'.format(animalId, e))
			return False

	def updateAnimalHit(self, animalId):
		try:
			sql = """UPDATE animals SET hits = hits + 1,
			updated = current_timestamp
			WHERE id = {}""".format(animalId)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot update animal hit with id: {}. Raised exception {}.'.format(animalId, e))
			return False

	# for debugging
	def showRecent(self, rowLimit):
		try:
			sql = """SELECT * FROM animals ORDER BY updated DESC LIMIT {}""".format(rowLimit)
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			return rows
		except Exception as e:
			log.error('Cannot show all. Raised exception {}.'.format(name, e))
			return False