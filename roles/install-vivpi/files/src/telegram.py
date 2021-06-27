import src.config as config
from datetime import datetime 
import telegram

settings = config.load()

bot = telegram.Bot(token=settings['telegram']['botToken'])

def listener():
    return ""

def sendAlert(message):
    for user in settings['telegram']['users']:
        bot.sendMessage(chat_id=user,text=message)

def sendMessage(message):
    for user in settings['telegram']['users']:
        bot.sendMessage(chat_id=user,text=message)