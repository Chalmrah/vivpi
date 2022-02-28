import src.config as config
import requests
#import energenie

settings = config.load()

thingspeakKey = settings['data']['thingspeakKey']

# function here that takes all the data and posts it to thingspeak

def postData(sensorData):
    data = {
        'api_key':thingspeakKey, 
        'field1':sensorData['warmTemperature'], 
        'field2':sensorData['warmPressure'], 
        'field3':sensorData['warmHumidity'], 
        'field4':sensorData['coldTemperature'], 
        'field5':sensorData['coldPressure'], 
        'field6':sensorData['coldHumidity'],
        'field7':sensorData['heaterStatus'],
        'field8':sensorData['humidityStatus']
        }

    req = requests.post('https://api.thingspeak.com/update.json', data = data)