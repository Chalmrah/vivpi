import src.config as config
import src.logging as log
import src.telegram as telegram
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
    isDay = isDuringDay(settings['time']['dayStart'],settings['time']['nightStart'],currentHour)
    # Default to nothing 
    action = None
    if isDay:
        maxTemp = float(settings['temperatures']['maxDayTemp'])
        minTemp = float(settings['temperatures']['minDayTemp'])
    else:
        maxTemp = float(settings['temperatures']['maxNightTemp'])
        minTemp = float(settings['temperatures']['minNightTemp'])
    
    alertTemp = minTemp - float(settings['temperatures']['alertThresholdTemp'])
    log.logDebug("Using daytime thresholds of maxTemp: {}, minTemp: {}, and alertTemp: {}".format(maxTemp, minTemp, alertTemp))
        
    if temp > maxTemp:
        log.logDebug("Temperature too high, turn off")
        action = False

    if temp < minTemp:
        log.logDebug("Temperature too low, turn on")
        action = True
    
    if temp < alertTemp:
        telegram.sendAlert("Temperature Alert!\nCurrent temp: {}C\nAlert threshold: {}C\nCheck vivarium and heater are working!".format(temp, alertTemp))

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