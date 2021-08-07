import src.config as config
import src.energenie as energenie
import src.logging as log
from datetime import datetime 

settings = config.load()
currentHour = datetime.now().hour


def isDuringDay(dayStart, nightStart, currentTime):
    # If check time is not given, default to current UTC time
    if dayStart < nightStart:
        return currentTime >= dayStart and currentTime < nightStart
    else: # crosses midnight
        return currentTime >= dayStart or currentTime <= nightStart

def verifyTemperature(data):
    temp = float(data['warmTemperature'])
    maxTempDay = float(settings['temperatures']['maxDayTemp'])
    maxTempNight = float(settings['temperatures']['maxNightTemp'])
    minTempDay = float(settings['temperatures']['minDayTemp'])
    minTempNight = float(settings['temperatures']['minNightTemp'])
    isDay = isDuringDay(settings['time']['dayStart'],settings['time']['nightStart'],currentHour)
    # Default to nothing 
    action = None
    if isDay:
        log.logDebug("Is day")

        if temp > maxTempDay:
            log.logDebug("Temperature too high, turn off")
            action = False

        if temp < minTempDay:
            log.logDebug("Temperature too low, turn on")
            action = True
    else:
        log.logDebug("Is night")

        if temp > maxTempNight:
            log.logDebug("Temperature too high, turn off")
            action = False

        if temp < minTempNight:
            log.logDebug("Temperature too low, turn on")
            action = True

    return action

def verifyHumidity(data):
    if settings['humidity']['useColdHumidity'] is True:
        hum = float(data['coldHumidity'])
    else:
        hum = float(data['warmHumidity'])
    minHum = float(settings['humidity']['minHumidity'])
    maxHum = float(settings['humidity']['maxHumidity'])
    # Default to do nothing
    action = None
    if hum > maxHum:
        log.logDebug("Humidity too high, turn off")
        action = False

    if hum < minHum:
        log.logDebug("Humidity too low, turn on")
        action = True

    return action

def verifyMisterOrFogger():
    isDay = isDuringDay(settings['time']['dayStart'],settings['time']['nightStart'],currentHour)
    if isDay:
        switchNumber = settings['switches']['misterSwitch']
    else:
        switchNumber = settings['switches']['foggerSwitch']
    return switchNumber