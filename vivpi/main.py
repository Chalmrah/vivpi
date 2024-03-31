
import src.config as config
import src.energenie as energenie
import src.thingspeak as thingspeak
import src.sensordata as sensordata
import src.action as action
import src.telegram as telegram
import src.logging as log
import src.nodeping as nodeping

# Load config
settings = config.load()

# Validate 
if(config.validateConfig(settings) == False):
    telegram.sendAlert("ALERT: Config validation unsuccessful!")
    raise ValueError("Config did not validate successfully! Please check json file!")
    
# Pull data from endpoint
data = sensordata.read()

# Validate data
if data['coldTemperature'] == 0:
    telegram.sendAlert('Cold sensor not responding!')
    if settings['humidity']['useColdHumidity'] is True:
        raise Exception('Cold sensor not responding. Failing to prevent false data processing!')
if data['warmTemperature'] == 0:
    telegram.sendAlert('Warm sensor not responding! Script will halt until this is resolved!')
    raise Exception('Warm sensor not responding. Failing to prevent false data processing!')

# Time to perform actions and verify the temps against the config
tempAction = action.verifyTemperature(data) 
humAction = action.verifyHumidity(data) 

if tempAction is True:
    energenie.temperatureOn()
if tempAction is False:
    energenie.temperatureOff()

if settings['humidity']['ignoreMister'] is True:
    if humAction is True:
        energenie.foggerOn()
    if humAction is False:
        energenie.foggerOff()
else:
    mistOrFog = action.verifyMisterOrFogger()
    if mistOrFog is settings['switches']['misterSwitch']:
        if humAction is True:
            if settings['humidity']['useTimedMister'] is True:
                energenie.misterOnTimed(settings['humidity']['timedMisterSeconds'])
            else:
                energenie.misterOn()
        if humAction is False:
            energenie.misterOff()

    if settings['switches']['foggerSwitch'] != settings['switches']['misterSwitch']:
        if mistOrFog == settings['switches']['foggerSwitch']: 
            if humAction is True:
                energenie.foggerOn()
            if humAction is False:
                energenie.foggerOff()

# Post data to thingspeak
if settings['data']['thingspeakEnabled'] is True:
    # Default status for sensors.
    data['heaterStatus'] = 1
    data['humidityStatus'] = 1
    # Change if action was taken.
    if tempAction is True:
        data['heaterStatus'] = 2
    if tempAction is False:
        data['heaterStatus'] = 0
    if humAction is True:
        data['humidityStatus'] = 2
    if humAction is False:
        data['humidityStatus'] = 0
    thingspeak.postData(data)

if settings['data']['nodepingEnabled'] is True:
    nodeping.postHeartbeat()