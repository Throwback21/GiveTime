import random
import sqlite3

from aiogram import types

import mysql
from mysql.connector import connect
from help import stri


adminList=[732391814, 909527339, 741340808]


def isAdmin(id):
    if id in adminList:
        return True


def sss():
    try:
        connection = con()

        mySql_insert_query = "SELECT chatid FROM users"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        users = []
        for row in cursor.fetchone():
            s = str(row)
            aaa = s.partition(',')[0]
            zzz = aaa.partition('(')[2]
            if int(zzz) not in adminList:
                users.append(zzz)
        cursor.close()
        return users

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def draw():
    return random.sample(sss(), 3)


def con():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        return sqlite_connection

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def add(userid, username, age,  chatId, phone):
        try:
            sqliteConnection = con()
            if userid==None:
                mySql_insert_query = "INSERT INTO users ( name, age, chatid, phone) VALUES ('" \
                                     +username + "', " + str(age) + ", " + str(chatId) + ", " + str(phone) + ");"
            else:
                mySql_insert_query = "INSERT INTO users (userId, name, age, chatid, phone) VALUES ('"\
            + userid +"', '" + username + "', "+str(age)+", "+str(chatId)+", "+str(phone)+");"

            cursor = sqliteConnection.cursor()
            cursor.execute(mySql_insert_query)
            sqliteConnection.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            cursor.close()
            return stri.compreg

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
            return stri.failreg


def isreg(chatid):
    try:
        connection = con()

        mySql_insert_query = "SELECT COUNT(*) FROM users WHERE chatId="+str(chatid)

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        result=cursor.fetchone()
        if result[-1]==1:
            return False
        elif result[-1]==0:
            return True
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def сount():
    try:
        connection = con()

        mySql_insert_query = "SELECT COUNT(*) FROM users"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        return cursor.fetchone()

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def getAge(chatid):
    try:
        connection = con()

        mySql_insert_query = "SELECT age FROM users WHERE chatid="+str(chatid)

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        return cursor.fetchone()

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def getName(chatid):
    try:
        connection = con()

        mySql_insert_query = "SELECT name FROM users WHERE chatid="+str(chatid)

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        s=str(cursor.fetchone())
        ss=s.partition("'")[2]
        sss=ss.partition("'")[0]

        return sss

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def getPhone(chatid):
    try:
        connection = con()

        mySql_insert_query = "SELECT phone FROM users WHERE chatid="+str(chatid)

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        return cursor.fetchone()

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def newbook(date, time, userid, age, phone, chatId, count):
    try:
        connection = con()
        if userid == None:
            mySql_insert_query = "INSERT INTO book ( date, time, age, chatid, phone, count) VALUES ('" \
                                 + date + "', '" + time + "', " + age + ", '" + str(chatId) + "', '" + str(phone) + "', "+str(count)+");"

        else:
            mySql_insert_query = "INSERT INTO book ( date, time, age, chatid, phone, userid, count) VALUES ('" \
                                 +date+"', '"+time+"', "+ age + ", '" + str(chatId) + "', '" + str(phone) + "', '"+str(userid)+"', "+str(count)+");"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return stri.bcomplete

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return stri.bfail


def books():
    try:
        connection = con()

        mySql_insert_query = "SELECT id, date, time, userid FROM book;"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        res=cursor.fetchall()
        return res

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def showbooks():
    try:
        connection = con()

        mySql_insert_query = "SELECT date, time, userid, count, phone, age FROM book;"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        res=cursor.fetchall()
        return res

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))



def delbook(id):
    try:
        connection = con()

        mySql_insert_query = "DELETE FROM book WHERE id="+id
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        return "Бронь удалена!"

        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

def sender():
    try:
        connection = con()

        mySql_insert_query = "SELECT chatid FROM users"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        users=[]
        for row in cursor.fetchall():
            s=str(row)
            aaa=s.partition(',')[0]
            zzz=aaa.partition('(')[2]
            users.append(zzz)
        cursor.close()
        return users
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def deleteAll(id):
    try:
        connection = con()
        mySql_insert_query = "DELETE FROM users WHERE chatid=" + str(id)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()
        return stri.delete

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return "Ошибка!"


