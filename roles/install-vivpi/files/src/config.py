import json
import os
from jsonschema import validate, ValidationError, SchemaError
import src.logging as log


def validateConfig(settings):
    schema = {
        "type" : "object",
        "data": {
            "type": "object",
            "properties" : {
                "sensorIpAddress" : {"type" : "string"},
                "thingspeakKey" : {"type" : "string",},
                "thingspeakEnabled" : {"type" : "boolean"}
            },
            "required": ["sensorIpAddress","thingspeakEnabled"]
        },
        "temperatures": {
            "type": "object",
            "properties" : {
                "maxDayTemp" : {"type" : "number",},
                "maxNightTemp" : {"type" : "number",},
                "minDayTemp" : {"type" : "number",},
                "minNightTemp" : {"type" : "number",}
            },
            "required": ["dayTemp","nightTemp"]
        },
        "humidity": {
            "type": "object",
            "properties" : {
                "maxHumidity" : {"type" : "number",},
                "minHumidity" : {"type" : "number",},
                "useColdHumidity" : {"type" : "boolean"},
                "useTimedMister" : {"type" : "boolean"},
                "timedMisterSeconds" : {"type" : "number"},
            },
            "required": ["humidityMax","humidityMin"]
        },
        "time": {
            "type": "object",
            "properties" : {
                "dayStart" : {"type" : "number",},
                "nightStart" : {"type" : "number",}
            },
            "required": ["dayStart","nightStart"]
        },
        "switches": {
            "type": "object",
            "properties" : {
                "tempSwitch" : {"type" : "number",},
                "humSwitch" : {"type" : "number",},
                "lightSwitch" : {"type" : "number",}
            },
            "required": ["tempSwitch","humSwitch"]
        },
        "logging": {
            "type": "object",
            "properties" : {}
        },
        "required": ["data","temperatures","humidity","time","switches"]
    }
    try:
        validate(settings, schema)
    except SchemaError as e:
        log.logInfo("There is an error with the schema")
        return False
    except ValidationError as e:
        log.logEmerg(e)
        log.logEmerg(e.absolute_path)
        return False
    return True

def load():
    dir = os.path.dirname(__file__)

    with open(os.path.join(dir, '..', 'config.json'), mode='r', encoding='utf-8') as f:
        return json.load(f)

def write(settings):
    dir = os.path.dirname(__file__)

    with open(os.path.join(dir, '..', 'config.json'),'w') as f:
        json.dump(settings, f, indent=4)
    return "Settings updated"
