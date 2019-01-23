# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:

	def __init__(self, database):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def select_all(self):
		with self.connection:
			return self.cursor.execute('SELECT * FROM Users').fetchall()

	

	# def select_single(self, rownum):
	# 	with self.connection:
	# 		return self.cursor.execute('SELECT * FROM users WHERE id = ?', (rownum,)).fetchall()[0]

	# def count_rows(self):
	# 	with self.connection:
	# 		result = self.cursor.execute('SELECT * FROM users').fetchall()
	# 		return len(result)

	def insert_id(self,user_id):
		with self.connection:
			self.cursor.execute('INSERT INTO Users(user_id) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Users WHERE user_id = ?)',(user_id,user_id,))
			self.connection.commit()

	def update_album_num(self,user_id,album_num):
		with self.connection:
			self.cursor.execute('UPDATE Users SET album_num = ? WHERE user_id = ?',(album_num,user_id,))
			self.connection.commit()
				
	def select_current_state(self,user_id):
		with self.connection:
			result = self.cursor.execute('SELECT current_state FROM Users WHERE user_id = ?',(user_id,)).fetchall()[0]
			return result[0]
						

	def update_state(self,user_id,value):
		with self.connection:
			self.cursor.execute('UPDATE Users SET current_state = ? WHERE user_id = ?',(value,user_id,))
			self.connection.commit()

	def update_chat_id(self,user_id,chat_id):
		with self.connection:
			self.cursor.execute('UPDATE Users SET chat_id = ? WHERE user_id = ?',(chat_id,user_id,))
			self.connection.commit()		


	def update_vk_id(self,user_id,vk_id):
		with self.connection:
			self.cursor.execute('UPDATE Users SET vk_id = ? WHERE user_id = ?',(vk_id,user_id,))
			self.connection.commit()

	def close(self):
		self.connection.close()							