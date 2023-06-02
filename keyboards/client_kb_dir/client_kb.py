from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Стаж')
b2 = KeyboardButton('ЗП')
b3 = KeyboardButton('Премия')
b4 = KeyboardButton('Моё Оборудование')
b5 = KeyboardButton('Назад')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.insert(b1).insert(b2).insert(b3).add(b4).add(b5)

# kb_client.add(b1, b2, b3).row(b4).insert(b5).insert(b6)
