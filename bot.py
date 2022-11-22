from aiogram.utils import executor
from createbot import dp

from handlers import botclient, botadmin

botadmin.dp_admin(dp)
botclient.dp_client(dp)


if __name__=='__main__':
    executor.start_polling(dp)


