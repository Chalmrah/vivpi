import src.energenie as energenie
import src.logging as log
import src.action as action
import src.config as config
from datetime import datetime 
from time import sleep

settings = config.load()

currentHour = datetime.now().hour

isDay = action.isDuringDay(settings['time']['dayStart'],settings['time']['nightStart'],currentHour)

if isDay:
    energenie.lightOn()
else:
    energenie.lightOff()