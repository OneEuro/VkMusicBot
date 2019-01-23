# -*- coding: utf-8 -*-
import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name
from random import shuffle
from telebot import types
from enum import Enum
import re

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_VKID = "1"
    S_DOWNLOADING = "2"
    # S_SEND_PIC = "3"

def clean(text):
    reg = re.compile(r'[^a-zA-Z ,\d,\w,а-я,А-Я,.]')
    string = reg.sub('', text)
    return string.replace(' ','_')

def set_user_id(user_id):
	db = SQLighter(database_name)
	db.insert_id(user_id)
	db.update_state(user_id,'1')
	db.close()

def set_album_num(user_id,album_num):
	db = SQLighter(database_name)
	db.update_album_num(user_id,album_num)
	db.close()

def get_user_id(user_id,album_num):
	db = SQLighter(database_name)
	db.update_album_num(user_id,album_num)
	db.close()

def get_current_state(user_id):
	db = SQLighter(database_name)
	state = db.select_current_state(user_id)
	db.close()
	return str(state)

def set_state(user_id, value):
	db = SQLighter(database_name)
	db.update_state(user_id,value)
	db.close()

def set_chat_id(user_id, chat_id):
	db = SQLighter(database_name)
	db.update_chat_id(user_id,chat_id)
	db.close()

def set_vk_id(user_id, vk_id):
	db = SQLighter(database_name)
	db.update_vk_id(user_id,vk_id)
	db.close()

# def count_rows():
# 	db = SQLighter(database_name)
# 	rowsnum = db.count_rows()
# 	with shelve.open(shelve_name) as storage:
# 		storage['rows_count'] = rowsnum


# def get_rows_count():
# 	with shelve.open(shelve_name) as storage:
# 		rowsnum = storage['rows_count']
# 	return rowsnum
	

	


# def finish_user_game(chat_id):
# 	with shelve.open(shelve_name) as storage:
# 		del storage[str(chat_id)]


# def get_answer_for_user(chat_id):
# 	with shelve.open(shelve_name) as storage:
# 		try:
# 			answer = storage[str(chat_id)]
# 			return answer
# 		except KeyError:
# 			return None

# def generate_markup(right_answer, wrong_answer):
# 	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
# 	all_answers = '{},{}'.format(right_answer,wrong_answer)
# 	list_items = []
# 	for item in all_answers.split(','):
# 		list_items.append(item)
# 	shuffle(list_items)
# 	for item in list_items:
# 		markup.add(item)
# 	return markup														