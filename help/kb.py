from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1 = KeyboardButton('💵')
button2 = KeyboardButton('📆')
button6 = KeyboardButton('🎟')
button5 = KeyboardButton('☘')
button4 = KeyboardButton('🌏')
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(button1, button2, button5, button6, button4)

contact_kb=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
contact_kb.add(KeyboardButton('📱Отправить номер', request_contact=True))

b1 = KeyboardButton('Да')
b2 = KeyboardButton('Нет')
check = ReplyKeyboardMarkup(resize_keyboard=True)
check.row(b1, b2)

bb = KeyboardButton('Отмена')
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.row(bb)

maps_kb = InlineKeyboardMarkup()
maps_kb.add(InlineKeyboardButton('Посмотреть на картах', url='https://yandex.ru/maps/org/dayte_time/220217265394'))



