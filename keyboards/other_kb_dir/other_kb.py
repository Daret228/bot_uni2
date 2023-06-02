from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Админ')
b2 = KeyboardButton('Пользователь')

kb_other = ReplyKeyboardMarkup(resize_keyboard=True)

kb_other.insert(b1).insert(b2)