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
    if isDay:
        maxTemp = float(settings['temperatures']['maxDayTemp'])
        minTemp = float(settings['temperatures']['minDayTemp'])
    else:
        maxTemp = float(settings['temperatures']['maxNightTemp'])
        minTemp = float(settings['temperatures']['minNightTemp'])
    
    # Validating alerts
    validateTemperatureAlerts(temp,minTemp,maxTemp)

    # Default to nothing 
    action = None
    if temp > maxTemp:
        log.logDebug("Temperature too high, turn off")
        action = False

    if temp < minTemp:
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

    # Validating alerts
    validateHumidityAlerts(hum,minHum,maxHum)
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

def validateTemperatureAlerts(temp,minTemp,maxTemp):
    alertTemp = minTemp - float(settings['temperatures']['alertThresholdTemp'])
    log.logDebug("Using thresholds of maxTemp: {}, minTemp: {}, and alertTemp: {}".format(maxTemp, minTemp, alertTemp))
    # Giving a 10 minute breather after the day switch before alerting for temperature
    breathingTime = 10
    currentMinute = datetime.now().minute
    if settings['time']['dayStart'] == currentHour and currentMinute < breathingTime:
        pass
    else:
        if temp < alertTemp:
            telegram.sendAlert("Temperature Alert!\nCurrent temp: {}C\nAlert threshold: {}C\nCheck vivarium and heater are working!".format(temp, alertTemp))

def validateHumidityAlerts(hum,minHum,maxHum):
    if maxHum+15 > 100:
        maxAlertHum = 97
    else:
        maxAlertHum = maxHum+15
    minAlertHum = minHum-20
    if hum > maxAlertHum:
        telegram.sendAlert("Humidity Alert!\nCurrent level: {}%\nAlert threshold: Above {}%\nCheck vivarium and mister are working!".format(hum, maxAlertHum))
    if hum < minAlertHum:
        telegram.sendAlert("Humidity Alert!\nCurrent level: {}%\nAlert threshold: Below {}%\nCheck vivarium and mister are working!".format(hum, minAlertHum))