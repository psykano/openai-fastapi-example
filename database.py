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

	# Create prompts table and add index for prompt input
	def createTableIfNotExists(self):
		try:
			sql = """CREATE TABLE IF NOT EXISTS prompts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				input TEXT NOT NULL UNIQUE,
				result TEXT NOT NULL,
				hits INTEGER DEFAULT 1,
				created datetime default current_timestamp,
				updated datetime default current_timestamp)"""
			self.cursor.execute(sql)
			self.connection.commit()
			sql = 'CREATE INDEX IF NOT EXISTS prompt_input_idx ON prompts(name)'
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot create table. Raised exception {}.'.format(e))
			return False

	# Get prompt ID by input using GLOB to make use of the index table
	def getPromptId(self, promptInput):
		try:
			sql = """SELECT id FROM prompts WHERE input GLOB '{}' LIMIT 1""".format(promptInput)
			self.cursor.execute(sql)
			rows = self.cursor.fetchone()
			if rows != None:
				return rows[0]
			return 0
		except Exception as e:
			log.error('Cannot get prompt with input: {}. Raised exception {}.'.format(promptInput, e))
			return 0

	def getPromptResultsFromId(self, promptId):
		try:
			sql = """SELECT result FROM prompts WHERE id = '{}' LIMIT 1""".format(promptId)
			self.cursor.execute(sql)
			rows = self.cursor.fetchone()
			if rows != None:
				return rows[0]
			return ""
		except Exception as e:
			log.error('Cannot get prompt results with id: {}. Raised exception {}.'.format(promptId, e))
			return ""

	def insertPrompt(self, promptInput, promptResult):
		try:
			sql = """INSERT INTO prompts (input,result) VALUES (
				'{}',
				'{}')""".format(promptInput, promptResult)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot insert prompt {}. Raised exception {}.'.format(promptInput, e))
			return False

	def updatePrompt(self, promptId, promptResult):
		try:
			sql = """UPDATE prompts SET result = '{}',
			hits = hits + 1,
			updated = current_timestamp
			WHERE id = {}""".format(promptResult, promptId)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot update prompt with id: {}. Raised exception {}.'.format(promptId, e))
			return False

	def updatePromptHit(self, promptId):
		try:
			sql = """UPDATE prompts SET hits = hits + 1,
			updated = current_timestamp
			WHERE id = {}""".format(promptId)
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			log.error('Cannot update prompt hit with id: {}. Raised exception {}.'.format(promptId, e))
			return False

	def showRecent(self, rowLimit):
		try:
			sql = """SELECT * FROM prompts ORDER BY updated DESC LIMIT {}""".format(rowLimit)
			self.cursor.execute(sql)
			rows = self.cursor.fetchall()
			return rows
		except Exception as e:
			log.error('Cannot show all. Raised exception {}.'.format(e))
			return False