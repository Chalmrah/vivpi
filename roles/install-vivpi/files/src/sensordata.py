
import src.config as config
import src.logging as log
import src.telegram as telegram
import requests # http requests
import json
from time import sleep # wait
#import re #regex parser
#import lxml # XML parder
#from bs4 import BeautifulSoup as bs # html parser
#
#
#def read():
#    webpage = getContent()
#    data = returnData(webpage)
#    return data
#
#def getContent():
#    try:
#        req = requests.get('http://'+ settings['data']['sensorIpAddress'])
#    except:
#        log.logError("Failure getting web data. Sleeping 10 seconds before trying again.")
#        sleep(10)
#        getContent()
#    # If it gets past the stage of curling the webpage.
#    if req.status_code == 200:
#        return req.content
#    else:
#        log.logWarn("Non 200 http response. Trying again")
#        sleep(1)
#        getContent()
#
#def returnData(webContent):
#    regex = re.compile(r'[^\d.]+')
#    soup = bs(webContent, 'lxml')
#    # get all data out of the webpage
#    warmTemperature = float(regex.sub('',(soup.find('span', attrs={'class':'warmTemperature'}).text)))
#    warmPressure    = float(regex.sub('',(soup.find('span', attrs={'class':'warmPressure'}).text)))
#    warmHumidity    = float(regex.sub('',(soup.find('span', attrs={'class':'warmHumidity'}).text)))
#    coldTemperature = float(regex.sub('',(soup.find('span', attrs={'class':'coldTemperature'}).text)))
#    coldPressure    = float(regex.sub('',(soup.find('span', attrs={'class':'coldPressure'}).text)))
#    coldHumidity    = float(regex.sub('',(soup.find('span', attrs={'class':'coldHumidity'}).text)))
#    return (warmTemperature,warmPressure,warmHumidity,coldTemperature,coldPressure,coldHumidity)

settings = config.load()

def read():
    webpage = getContent()
    data = json.loads(webpage)
    return data

#def getContent():
#    try:
#        req = requests.get('http://'+ settings['data']['sensorIpAddress'] + '/data.json')
#    except:
#        log.logError("Failure getting web data. Sleeping 10 seconds before trying again.")
#        sleep(10)
#        getContent()
#    # If it gets past the stage of curling the webpage.
#    if req.status_code == 200:
#        return req.content
#    else:
#        log.logWarn("Non 200 http response. Trying again")
#        sleep(1)
#        getContent()


# Write timeout counter to fail and alert after 3 tries saying it cant run again. Telegram message?
# Write status to file to check if heater is already on to prevent it constantly trying to turn on or off a device?

def getContent():
    for i in range(1,3):
        try:
            req = requests.get('http://'+ settings['data']['sensorIpAddress'] + '/data.json')
            if req.status_code == 200:
                return req.content
        except:
            log.logError("Failure getting web data attempt %s. Sleeping 10 seconds before trying again." % i)
            sleep(10)
    if i == 3:
        log.logError("Final attempt has failed. Alerting...")
        telegram.sendAlert("Collecting sensor data has failed! Check sensor health!")
