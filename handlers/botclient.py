from datetime import datetime

from  aiogram import types
from aiogram import Dispatcher
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.json import json

from help import kb, stri, database
from help.testbot import numberdef, num
from handlers import botadmin
from help import Actions
from createbot import bot

#машина состояний
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMReg(StatesGroup):
    cont=State()
    age=State()
    check=State()

class FSMBook(StatesGroup):
    dt=State()
    tm=State()
    cn=State()
    ch=State()

class Num:
    number=None


#START/HELP

async def command_help(message: types.Message):
    if database.isreg(message.from_user.id):
        await message.answer(stri.needreg, reply_markup=kb.main_kb)
    else:
        await message.answer(stri.help, reply_markup=kb.main_kb)



#РЕГИСТРАЦИЯ


async def command_reg(message: types.Message):
    if database.isreg(message.from_user.id):
        await FSMReg.cont.set()
        await message.reply(stri.reg, reply_markup=kb.contact_kb)
    else:
        await message.answer(stri.notreg, reply_markup=kb.main_kb)


async def msg_cont(message: types.Message, state:FSMContext):
    if message.text==None:
        async with state.proxy() as data:
            data['reg']=message.contact.phone_number
            await FSMReg.next()
            await message.answer(stri.age, reply_markup=kb.main_kb)
    elif numberdef(message.text):
        async with state.proxy() as data:
            data['reg']=num(message.text)
        await FSMReg.next()
        await message.answer(stri.age, reply_markup=kb.main_kb)
    else:
        await message.answer(stri.contacterror, reply_markup=kb.contact_kb)

async def age(msg: types.Message, state:FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['age']=msg.text
        await msg.answer("Ваш номер: " + data['reg'])
        await msg.answer('Ваш возраст: ' + data['age'])
        await FSMReg.next()
        await msg.answer('Всё верно?', reply_markup=kb.check)
    else:
        await msg.answer('Укажите свой возраст:')

async def reg(msg: types.Message, state:FSMContext):
    if msg.text=='Да':
        async with state.proxy() as data:
            await msg.answer(database.add(msg.from_user.username, msg.from_user.first_name,
                                          data['age'], msg.from_user.id, data['reg']), reply_markup=kb.main_kb)
            await state.finish()
    elif msg.text=='Нет':
        await FSMReg.first()
        await command_reg(msg)





#БРОНИРОВАНИЕ
async def newbook(msg: types.Message,):
    if database.isreg(msg.from_user.id):
        await  msg.answer(stri.needreg)
    else:
        await FSMBook.dt.set()
        await msg.answer(stri.date, reply_markup=kb.cancel)

async def bookdate(msg:types.Message, state:FSMContext):
    if msg.text=='Отмена':
        await state.finish()
        await msg.answer("Бронь отменена.", reply_markup=kb.main_kb)
    else:
        msg.text = msg.text.replace(' ', '.')
        msg.text = msg.text.replace('-', '.')
        if str(msg.text.partition('.')[0]).isdigit() and str(msg.text.partition('.')[2]).isdigit():
            if int(msg.text.partition('.')[0])<32 and int(msg.text.partition('.')[0])>0:
                if int(msg.text.partition('.')[2])<13 and int(msg.text.partition('.')[2])>0:
                    async with state.proxy() as data:
                        data['dt'] = msg.text
                        await FSMBook.next()
                        await msg.answer(stri.time)
                else:
                    await msg.answer("Вы указали недоступную дату! Попробуйте снова.")
            else:
                await msg.answer("Вы указали недоступную дату! Попробуйте снова.")
        else:
            await msg.answer("Вы указали недоступную дату! Попробуйте снова.")

async def booktime(msg:types.Message, state:FSMContext):
    msg.text=msg.text.replace(' ', ':')
    msg.text=msg.text.replace('.', ':')
    if str(msg.text.partition(':')[0]).isdigit() and str(msg.text.partition(':')[2]).isdigit():
        if int(msg.text.partition(':')[0])<19 and int(msg.text.partition(':')[0])>9:
            if int(msg.text.partition(':')[2])<60 and int(msg.text.partition(':')[2])>=0:
                if int(msg.text.partition(':')[0]) >=18 and int(msg.text.partition(':')[2]) > 0:
                    await msg.answer("Вы указали недоступное время! Попробуйте снова.")
                else:
                    async with state.proxy() as data:
                        data['tm'] = msg.text
                        await FSMBook.next()
                        await msg.answer(stri.count)
            else:
                await msg.answer("Вы указали недоступное время! Попробуйте снова.")
        else:
            await msg.answer("Вы указали недоступное время! Попробуйте снова.")
    else:
        await msg.answer("Вы указали недоступное время! Попробуйте снова.")

async def bookcount(msg:types.Message, state:FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['count'] = msg.text
            await msg.answer("Дата брони: " + data['dt'] +
                             "\nВремя брони: " + data['tm']+
                             "\nКолличество: "+data['count'])
            await FSMBook.next()
            await msg.answer(stri.checkbook, reply_markup=kb.check)
    else:
        await msg.answer(stri.count)

async def bookcheck(msg:types.Message, state:FSMContext):
    if msg.text=='Да':
        s = str(database.getAge(msg.from_user.id))
        aaa = s.partition(',')[0]
        age = aaa.partition('(')[2]
        ss = str(database.getPhone(msg.from_user.id))
        aa = ss.partition("'")[2]
        phone = aa.partition("'")[0]
        if msg.from_user.username==None:
            name='None'
        else:
            name=msg.from_user.username

        async with state.proxy() as data:
            await msg.answer(database.newbook(data['dt'],data['tm'], name, age,
                                              phone, msg.from_user.id, data['count']), reply_markup=kb.main_kb)
            await botadmin.adminSender(msg.from_user.id, "Новая бронь!\nДата- "+str(data['dt'])+
                        "\nВремя- "+str(data['tm'])+
                        "\nВозраст- "+str(age)+
                        "\nАккаунт- @"+name+
                        "\nНомер- +"+str(phone)+
                        "\nКол-во чел.: "+str(data['count']))
            await state.finish()
    elif msg.text=='Нет':
        await FSMBook.first()
        await newbook(msg)



async def actions(msg:types.Message):
    if Actions.actText()==stri.actnone and Actions.actPhoto()==None and Actions.weekAct() == None:
        await msg.answer(stri.actnone)
    else:
        await msg.answer("Наши акции:")
        if Actions.actText() != stri.actnone:
            await bot.send_message(msg.from_user.id, Actions.actText())
        media = []
        print(Actions.actPhoto())
        if Actions.actPhoto() != None:
            for i in Actions.actPhoto():
                s = str(i).partition("'")[2].partition("'")[0]
                if s != 'None':
                    media.append(types.InputMediaPhoto(s))
            if len(media) > 1:
                await bot.send_media_group(msg.from_user.id, media=media)
            elif len(media) == 1:
                await bot.send_photo(msg.from_user.id, s)
        if Actions.weekAct() != None:
            for s in Actions.weekAct():
                if s != 'None':
                    await bot.send_photo(msg.from_user.id, s, caption="Еженедельная акция!!!")



async def events(msg: types.Message):
    if database.isreg(msg.from_user.id):
        await msg.answer(stri.needreg)
    elif len(Actions.showEvents())!=0:
        await msg.answer("Ближайшие мероприятия:")
        for i in Actions.showEvents():
            idev=str(i).partition('(')[2].partition(',')[0]
            text=str(i).partition("'")[2].partition("', ")[0]
            photo=str(i).partition(text+"', '")[2].partition("', ")[0]
            text=text.replace(r'\n', '\n')

            ikm = InlineKeyboardMarkup()
            ikm.add(InlineKeyboardButton('Записаться', callback_data=str(idev)))
            if text=='None':
                await bot.send_photo(msg.from_user.id, photo=photo, parse_mode="HTML", reply_markup=ikm)
            elif photo!='None':
                await bot.send_photo(msg.from_user.id, photo=photo, caption=text, parse_mode="HTML", reply_markup=ikm)
            else:
                await bot.send_message(msg.from_user.id, text, parse_mode="HTML", reply_markup=ikm)
    else:
        await msg.answer(stri.ev)

async def callEv(msg:types.CallbackQuery):
    await bot.send_message(msg.from_user.id, Actions.regEvent(msg.data, msg.from_user.id))



async def echo_message(msg: types.Message):
        if msg.text== '💵':
            if database.isreg(msg.from_user.id):
                await msg.answer(stri.needreg, reply_markup=kb.main_kb)
            else:
                await msg.answer(stri.price, reply_markup=kb.main_kb)
        elif msg.text== '📆':
            if database.isreg(msg.from_user.id):
                await msg.answer(stri.needreg, reply_markup=kb.main_kb)
            else:
                await msg.answer(stri.book)
                await newbook(msg, FSMBook)
        elif msg.text== '☘':
            if database.isreg(msg.from_user.id):
                await msg.answer(stri.needreg, reply_markup=kb.main_kb)
            else:
                await msg.answer(stri.action)
        elif msg.text== '🌏':
            if database.isreg(msg.from_user.id):
                await msg.answer(stri.needreg, reply_markup=kb.main_kb)
            else:
                await msg.answer(stri.connect)
                await msg.answer(stri.maps, reply_markup=kb.maps_kb)
        else:
            msg.text = "Я тебя не понимаю."
            await msg.answer(msg.text, reply_markup=kb.main_kb)

async def stop(msg: types.Message):
    await msg.answer(database.deleteAll(msg.from_user.id))



def dp_client(dp:Dispatcher):
    dp.register_message_handler(command_help, commands=['start','help'])
    dp.register_message_handler(stop, commands=['stop'])
    dp.register_message_handler(command_reg, commands=['reg'], state=None)
    dp.register_message_handler(msg_cont, content_types=['contact', 'text'], state=FSMReg.cont)
    dp.register_message_handler(age, state=FSMReg.age)
    dp.register_message_handler(reg, state=FSMReg.check)
    dp.register_message_handler(actions,filters.Text(contains='☘', ignore_case=True))
    dp.register_message_handler(events,filters.Text(contains='🎟', ignore_case=True))
    dp.register_message_handler(newbook,filters.Text(contains='📆', ignore_case=True), state=None)
    dp.register_message_handler(bookdate, state=FSMBook.dt)
    dp.register_message_handler(booktime, state=FSMBook.tm)
    dp.register_message_handler(bookcount, state=FSMBook.cn)
    dp.register_message_handler(bookcheck, state=FSMBook.ch)
    dp.register_callback_query_handler(callEv)
    dp.register_message_handler(echo_message)