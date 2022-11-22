import datetime
from datetime import datetime


def get_date():
    current_dt = datetime.now().strftime("%d.%m")
    c_date = current_dt.split()
    msg = f"{c_date}".partition("'")[2].partition("'")[0]
    return msg

def get_time():
    current_dt = datetime.now().strftime("%H:%M")
    c_time = current_dt.split()
    msg = f"{c_time}".partition("'")[2].partition("'")[0]
    return msg


def numberdef(num):
    if num[0:1]=='8':
        if len(num)==11:
            return True
    elif num[0:2]=='+7':
        if len(num)==12:
            return True
    elif num[0:1] == '7':
        if len(num)==11:
            n='+'+num
            return True


def num(ph):
    if ph[0:1]=='8':
        p=str(ph).replace('8', '+7', 1)
    elif ph[0:2]=='+7':
        p=ph
    elif ph[0:1] == '7':
        p ='+'+ph
    return p


def phoneReplace(num):
    if num[0:1]=='8':
        phone=num.replace('8','+7',1)
        return phone
    elif num[0:2]=='+7':
        return num
    elif num[0:1] == '7':
        if len(num)==11:
            n='+'+num
            return n


def isAge(string):
    if string.isdigit:
        if int(string)<100:
            return True

