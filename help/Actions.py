import mysql
from mysql.connector import connect
from datetime import datetime

from help import stri, database

class Act:
    photo: str
    text: str
    desc: str

def thisday():
    return datetime.isoweekday(datetime.now())


def con():
    return database.con()

def adAction(text):
    try:
        sqliteConnection = con()
        photo=str(text).partition('caption:')[0]
        text=str(text).partition('caption:')[2]
        if photo == 'None':
            mySql_insert_query = "INSERT INTO actions (text, photo, description) VALUES ('"+text+"', 'None', 'None');"
        elif text.isdigit():
            mySql_insert_query = "DELETE FROM actions WHERE description="+text
            cursor = sqliteConnection.cursor()
            cursor.execute(mySql_insert_query)
            sqliteConnection.commit()
            mySql_insert_query = "INSERT INTO actions (description, photo, text) VALUES ('" + text + "', '" + photo + "', 'None');"
        else:
            mySql_insert_query = "INSERT INTO actions (text, photo, description) VALUES ('"+text+"', '"+photo+"', 'None');"
        cursor = sqliteConnection.cursor()
        cursor.execute(mySql_insert_query)
        sqliteConnection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return stri.actcomplete
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return stri.actfail


def actPhoto():
    try:
        connection = con()
        mySql_insert_query = "SELECT COUNT(*) FROM actions WHERE description='None'"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        countres=cursor.fetchone()
        if countres[-1]==0:
            return None
        else:
            mySql_insert_query = "SELECT photo FROM actions WHERE description='None'"
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            photos = cursor.fetchall()
            return photos

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def actText():
    try:
        connection = con()
        mySql_insert_query = "SELECT COUNT(*) FROM actions WHERE description='None'"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        countres=cursor.fetchone()
        if countres[-1]==0:
            return stri.actnone
        else:
            msg="Наши акции:\n\n"
            mySql_insert_query = "SELECT text FROM actions WHERE photo='None'"
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            texts = cursor.fetchone()
            print(texts)
            if texts!=None:
                for i in texts:
                    if i != 'None' and i != '':
                        msg += str(i) + "\n\n"

                return msg
            else:
                return stri.actnone

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

def weekAct():
    try:
        id=thisday()
        connection = con()
        mySql_insert_query = "SELECT COUNT(*) FROM actions WHERE description=" + str(id)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        countres = cursor.fetchone()
        if countres[-1] == 0:
            return None
        else:
            media = []
            mySql_insert_query = "SELECT photo FROM actions WHERE description=" + str(id)
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            photos = cursor.fetchone()
            return photos

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def admText():
    try:
        connection = con()

        mySql_insert_query = "SELECT id, text FROM actions WHERE description='None' AND text!='None' AND photo='None';"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        photos = cursor.fetchall()
        return photos

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def admPhoto():
    try:
        connection = con()
        mySql_insert_query = "SELECT id, photo FROM actions WHERE description='None';"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        photos = cursor.fetchall()
        return photos

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))



def delAction(id):
    try:
        connection = con()
        mySql_insert_query = "DELETE FROM actions WHERE id="+id
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return "Акция удалена!"
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return stri.actfail

def delWeek(id):
    try:
        connection = con()
        mySql_insert_query = "DELETE FROM actions WHERE description="+id
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return "Акция удалена!"
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return stri.actfail


def showEvents():
    try:
        connection = con()
        mySql_insert_query = "SELECT * FROM actions WHERE description='event';"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        event = cursor.fetchall()
        return event

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

def txtEvents():
    try:
        connection = con()
        mySql_insert_query = "SELECT id, text, photo FROM actions WHERE description='event';"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        event = cursor.fetchall()


        return event

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

def txtAct():
    try:
        connection = con()
        mySql_insert_query = "SELECT id, text, photo FROM actions WHERE description='None';"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        event = cursor.fetchone()


        return event

        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def addEvent(text):
    try:
        connection = con()
        photo=str(text).partition('caption:')[0]
        text=str(text).partition('caption:')[2]
        if photo == 'None':
            mySql_insert_query = "INSERT INTO actions (text, photo, description) VALUES ('"+text+"', 'None', 'event');"
        else:
            mySql_insert_query = "INSERT INTO actions (text, photo, description) VALUES ('"+text+"', '"+photo+"', 'event');"
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return stri.evcomp
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return stri.evfail



def regEvent(id, user):
    try:
        connection = con()
        mySql_insert_query = "SELECT people FROM actions WHERE id="+id
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        ev = cursor.fetchone()
        peps = []
        peo = str(ev[-1])
        if str(user) in peo:
            return "Вы уже зарегистрированы на данное мероприятие!"
        else:
            print(peo)
            if peo=='None':
                peo = str(user) + "n"
            else:
                peo = peo+str(user)+"n"
            print(peo)
            cursor = connection.cursor()
            cursor.execute('update actions set people=? where id=?', [peo, id])
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.close()
            return stri.regevc
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return "Ошибка"

def eventPeople(id):
    try:
        connection = con()
        mySql_insert_query = "SELECT people FROM actions WHERE id=" + id
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        peo = cursor.fetchone()
        peps=[]
        evPeo="Участники:\n"

        if peo!='None':
            peo = str(peo[-1])

            while "n" in peo:
                p1 = peo.partition('n')[0]
                peps.append(p1)
                peo = peo.replace(p1 + 'n', '')
            for i in peps:
                mySql_insert_query = "SELECT userid, phone FROM users WHERE chatid=" + i
                cursor = connection.cursor()
                cursor.execute(mySql_insert_query)
                user = cursor.fetchall()
                phone = '+' + str(user[-1][-1])

                name = '@' + str(user[-1][-2])
                evPeo += phone + "\n" + name + "\n\n"
        else:
            evPeo=evPeo+"\nУчастников нет!"
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return evPeo
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))



