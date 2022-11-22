import time

import mysql
from  aiogram import types
from aiogram import Dispatcher

from help import kb, database, stri, Actions
from createbot import bot



#машина состояний
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMDraw(StatesGroup):
    prize1=State()
    prize2=State()
    prize3=State()
    start=State()

class FSMAct(StatesGroup):
    startAc=State()
    finishAc=State()

class FSMDel(StatesGroup):
    deleteAc=State()

class FSMSend(StatesGroup):
    send=State()

class FSMdb(StatesGroup):
    delete=State()

class FSMevent(StatesGroup):
    newEv=State()

class FSMinf(StatesGroup):
    ev=State()


#РОЗЫГРЫШ
async def newDraw(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        await FSMDraw.prize1.set()
        await msg.reply("Приз за Первое место!")
    else:
        await msg.answer("Вы не администратор!")

async def draw1(msg: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['1'] = msg.text
    await FSMDraw.next()
    await msg.reply("Приз за Второе место!")

async def draw2(msg: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['2'] = msg.text
    await FSMDraw.next()
    await msg.reply("Приз за Третье место!")

async def draw3(msg: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['3'] = msg.text
    await msg.answer("1- "+data['1'])
    await msg.answer("2- "+data['2'])
    await msg.answer("3- "+data['3'])
    await FSMDraw.next()
    await msg.reply("Всё верно?", reply_markup=kb.check)

async def start(msg: types.Message, state:FSMContext):
    if msg.text=='Да':
        async with state.proxy() as data:
            p1=data['1']
            p2=data['2']
            p3=data['3']
        pr=database.draw()
        name1 = f'<a href="tg://user?id={pr[0]}">{database.getName(pr[0])}</a>'
        name2 = f'<a href="tg://user?id={pr[1]}">{database.getName(pr[1])}</a>'
        name3 = f'<a href="tg://user?id={pr[2]}">{database.getName(pr[2])}</a>'
        text="Итоги розыгрыша!\n\n" \
             "Первое место: "+name1+"\nПриз: "+data['1']+\
             "\n\nВторое место: "+name2+"\nПриз: "+data['2']+\
             "\n\nТретье место: "+name3+"\nПриз: "+data['3']+\
             "\n\nПоздравляем победителей и ждём следующих розыгрышей!"
        for i in database.sender():
            await bot.send_message(i, text, parse_mode="HTML")
        await bot.send_message(pr[0], "Поздравляем Вас!\nВаш приз: "+data['1']+"\nЖдём в Дайте TIME!")
        await bot.send_message(pr[1], "Поздравляем Вас!\nВаш приз: "+data['2']+"\nЖдём в Дайте TIME!")
        await bot.send_message(pr[2], "Поздравляем Вас!\nВаш приз: "+data['3']+"\nЖдём в Дайте TIME!")
        await state.finish()
        await msg.answer("Успешно!", reply_markup=kb.main_kb)
    else:
        await state.finish()
        await msg.answer("Отмена розыгрыша", reply_markup=kb.main_kb)



#АКЦИЯ
async def newAct(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        await FSMAct.startAc.set()
        await msg.reply("Отправь фотку или текст для новой акции!")
    else:
        await msg.answer("Вы не администратор!")

async def actmsg(msg:types.Message, state:FSMContext):
    if msg.text==None:
        async with state.proxy() as data:
            data['text']=msg.caption
            data['ph']=msg.photo[-1].file_id
        await FSMAct.next()
        await msg.answer("Проверьте правильность данных. Всё верно?", reply_markup=kb.check)
    else:
        async with state.proxy() as data:
            data['text']=msg.text
            data['ph']=None
        await FSMAct.next()
        await msg.answer("Проверьте правильность данных. Всё верно?", reply_markup=kb.check)

async def actfinish(msg:types.Message, state:FSMContext):
    if msg.text=='Да':
        async with state.proxy() as data:
            text=str(data['ph'])+'caption:'+str(data['text'])
            await msg.answer(Actions.adAction(text), reply_markup=kb.main_kb)
        await state.finish()
    else:
        await msg.answer("Акция отменена", reply_markup=kb.main_kb)
        await state.finish()


#РАССЫЛКА
def mar(chatid):
    button_url = "tg://openmessage?user_id=" + str(chatid)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Написать', url=button_url))
    return markup


async def sender(message: types.Message):
    if database.isAdmin(message.from_user.id):
        await FSMSend.send.set()
        await message.answer("Отправьте сообщение для рассылки!", reply_markup=kb.cancel)

    else:
        await message.answer("Вы не администратор!", reply_markup=kb.main_kb)


async def sendMsg(msg: types.Message, state:FSMContext):
    if msg.text=='Отмена':
        await state.finish()
        await msg.answer("Отмена рассылки", reply_markup=kb.main_kb)
    else:
        if msg.content_type=='photo':
            for i in database.sender():
                msg.from_user.id = i
                await bot.send_photo(i, msg.photo[-1].file_id, msg.caption)
                time.sleep(1)
        elif msg.content_type=='voice':
            for i in database.sender():
                await bot.send_voice(i, voice=msg.voice.file_id)
                time.sleep(1)
        elif msg.content_type=='video':
            for i in database.sender():
                await bot.send_video(i, video=msg.video.file_id, caption=msg.caption)
                time.sleep(1)
        elif msg.content_type=='video_note':
            for i in database.sender():
                await bot.send_video_note(i, msg.video_note.file_id)
                time.sleep(1)
        elif msg.content_type=='sticker':
            for i in database.sender():
                await bot.send_sticker(i, msg.sticker.file_id)
                time.sleep(1)
        elif msg.content_type=='text':
            for i in database.sender():
                await bot.send_message(i, msg.text)
                time.sleep(1)


async def adminSender(id, msg: types.Message):
    for i in database.adminList:
        await bot.send_message(i, msg, reply_markup=mar(id))


async def delAct(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        if msg.text.partition('/delete ')[2].isdigit():
            await msg.answer(Actions.delWeek(msg.text.partition('/delete ')[2]))
        else:
            await FSMDel.deleteAc.set()
            for i in Actions.admText():
                print(i)
                id=str(i).partition('(')[2].partition(',')[0]
                text=str(i).partition("'")[2].partition("'")[0]
                await msg.answer(str(id)+"\n"+text)
            for i in Actions.admPhoto():
                print(Actions.actPhoto())
                id=str(i).partition('(')[2].partition(',')[0]
                text=str(i).partition("'")[2].partition("'")[0]
                if text!='None':
                    await bot.send_photo(msg.from_user.id, text, caption=id)
            for i in Actions.txtEvents():
                id = str(i).partition("(")[2].partition(", '")[0]
                tex = str(i).partition(id + ", '")[2].partition("', '")[0]
                ph = str(i).partition(tex + "', '")[2].partition("')")[0]
                if ph == 'None':
                    s = str(id + "\n\n" + tex).replace(r'\n', '\n')
                    await msg.answer(s)
                else:
                    s = str(tex + "\n\n\n" + id).replace(r'\n', '\n')
                    await bot.send_photo(msg.from_user.id, photo=ph, caption=s)
            await msg.answer("Введи номер акции, которую хочешь удалить!", reply_markup=kb.cancel)
    else:
        await msg.answer("Вы не администратор!", reply_markup=kb.main_kb)

async def delFinAct(msg: types.Message, state:FSMContext):
    if msg.text=='Отмена':
        await msg.answer("Удаление окончено!", reply_markup=kb.main_kb)
        await state.finish()

    elif msg.text.isdigit():
        await msg.answer(Actions.delAction(msg.text), reply_markup=kb.cancel)
    else:
        await msg.answer("Введи номер акции, которую хочешь удалить!")


async def delBook(msg: types.Message, state:FSMContext):
    if database.isAdmin(msg.from_user.id):
        await FSMdb.delete.set()
        for i in database.books():
            id=str(i).partition('(')[2].partition(',')[0]
            date=str(i).partition("'")[2].partition("'")[0]
            time=str(i).partition(date+"', '")[2].partition("',")[0]
            user=str(i).partition(time+"', '")[2].partition("')")[0]
            await msg.answer(str(id)+"\n"+date+"\n"+time+"\n@"+user)
        await msg.answer("Введи номер брони, которую хочешь удалить!", reply_markup=kb.cancel)
    else:
        await msg.answer("Вы не администратор!", reply_markup=kb.main_kb)


async def delFinBook(msg: types.Message, state:FSMContext):
    if msg.text=='Отмена':
        await msg.answer("Удаление окончено!", reply_markup=kb.main_kb)
        await state.finish()
    elif msg.text.isdigit():
        await msg.answer(database.delbook(msg.text), reply_markup=kb.cancel)
    else:
        await msg.answer("Введи номер брони, которую хочешь удалить!")


async def book(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        if len(database.showbooks())==0:
            await msg.answer("Актуальных броней нет!")
        for i in database.showbooks():
            await msg.answer(i[0]+"  "+i[1]+"\n@"+i[2]+" \n"+i[5]+" лет\n+"+i[4]+"\nКол-во чел.: "+i[3])
    else:
        await msg.answer("Вы не администратор!", reply_markup=kb.main_kb)


async def newEvent(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        await FSMevent.newEv.set()
        await msg.answer("Отправьте фото/видео/текст для нового мероприятия!", reply_markup=kb.cancel)
    else:
        await msg.answer("Вы не администратор!")




async def addNewEvent(msg: types.Message, state: FSMContext):
    if msg.text=='Отмена':
        await state.finish()
        await msg.answer("Отмена мероприятия!")
    else:
        if msg.caption==None:
            msg.caption='None'
        if msg.content_type=='photo':
            mes=msg.photo[-1].file_id+"caption:"+msg.caption
        elif msg.content_type=='video':
            mes=msg.video.file_id+"caption:"+msg.caption
        elif msg.content_type=='text':
            mes="Nonecaption:"+msg.text
        await msg.answer(Actions.addEvent(mes), reply_markup=kb.main_kb)
        await state.finish()


async def eventInfo(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        if len(Actions.txtEvents())==0:
            await msg.answer("Мероприятий нет")
        else:
            for i in Actions.txtEvents():
                print(i)
                id = str(i).partition("(")[2].partition(", '")[0]
                tex = str(i).partition(id + ", '")[2].partition("', '")[0]
                ph = str(i).partition(tex + "', '")[2].partition("')")[0]
                if ph == 'None':
                    s = str(id + "\n\n" + tex).replace(r'\n', '\n')
                    await msg.answer(s)
                else:
                    s = str(tex + "\n\n\n" + id).replace(r'\n', '\n')
                    await bot.send_photo(msg.from_user.id, photo=ph, caption=s)
            await FSMinf.ev.set()
    else:
        await msg.answer("Вы не администратор!", reply_markup=kb.main_kb)

async def evInf(msg: types.Message, state:FSMContext):
    await msg.answer(Actions.eventPeople(msg.text))
    await state.finish()


async def adminhelp(msg: types.Message):
    if database.isAdmin(msg.from_user.id):
        await msg.answer(stri.admin)
    else:
        await msg.answer("Вы не администратор!", reply_markup=kb.main_kb)


async def count(msg: types.Message):
    try:
        connection = database.con()
        mySql_insert_query = "SELECT COUNT(*) FROM users;"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        photos = cursor.fetchone()
        await msg.answer("Колличество пользователей: "+str(photos[-1]))

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))




def dp_admin(dp:Dispatcher):
    dp.register_message_handler(sender, commands=['send'], state=None)
    dp.register_message_handler(sendMsg, content_types=['photo', 'video', 'text', 'voice', 'video_note', 'sticker'], state=FSMSend.send)
    dp.register_message_handler(newDraw, commands=['raffle'], state=None)
    dp.register_message_handler(draw1, state=FSMDraw.prize1)
    dp.register_message_handler(draw2, state=FSMDraw.prize2)
    dp.register_message_handler(draw3, state=FSMDraw.prize3)
    dp.register_message_handler(start, state=FSMDraw.start)
    dp.register_message_handler(newAct, commands=['newaction'], state=None)
    dp.register_message_handler(actmsg, content_types=['photo', 'text'], state=FSMAct.startAc)
    dp.register_message_handler(actfinish, state=FSMAct.finishAc)
    dp.register_message_handler(delAct, commands=['delete'], state=None)
    dp.register_message_handler(delFinAct, state=FSMDel.deleteAc)
    dp.register_message_handler(delBook, commands=['delbook'], state=None)
    dp.register_message_handler(delFinBook, state=FSMdb.delete)
    dp.register_message_handler(newEvent, commands=['newevent'], state=None)
    dp.register_message_handler(addNewEvent, content_types=['photo', 'video', 'text'], state=FSMevent.newEv)
    dp.register_message_handler(eventInfo, commands=['event'], state=None)
    dp.register_message_handler(evInf, state=FSMinf.ev)
    dp.register_message_handler(adminhelp, commands=['admin', 'a', ''])
    dp.register_message_handler(book, commands=['book'])
    dp.register_message_handler(count, commands=['count'])


