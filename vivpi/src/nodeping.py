import src.config as config
import requests
import json
#import energenie

settings = config.load()

def postHeartbeat():
  params = {
    'id' : settings["data"]["nodepingCheckId"],
    'checktoken' : settings["data"]["nodepingCheckToken"]
    }
  url = "https://push.nodeping.com/v1"
  requests.post(url,params=params)
  