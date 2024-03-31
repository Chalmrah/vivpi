import src.config as config
import requests
#import energenie

settings = config.load()

checkId = settings["data"]["nodepingCheckId"]
checkToken = settings["data"]["nodepingCheckToken"]

def postHeartbeat():
  data = {'status': 200}
  url = "https://push.nodeping.com/v1?id=%s&checktoken=%s" % checkId,checkToken
  requests.post(url,data)
  