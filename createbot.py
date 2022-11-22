from  aiogram import Bot
from  aiogram.dispatcher import  Dispatcher
from help import stri
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

bot=Bot(token=stri.TOKEN)
dp=Dispatcher(bot, storage=storage)