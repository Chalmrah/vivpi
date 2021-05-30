
import src.config as config
import src.logging as log
import requests # http requests
import json
#import re #regex parser
#import lxml # XML parder
#from bs4 import BeautifulSoup as bs # html parser
#from time import sleep # wait
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

def getContent():
    try:
        req = requests.get('http://'+ settings['data']['sensorIpAddress'] + '/data.json')
    except:
        log.logError("Failure getting web data. Sleeping 10 seconds before trying again.")
        sleep(10)
        getContent()
    # If it gets past the stage of curling the webpage.
    if req.status_code == 200:
        return req.content
    else:
        log.logWarn("Non 200 http response. Trying again")
        sleep(1)
        getContent()
