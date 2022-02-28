import src.config as config
import src.logging as log
from energenie import switch_on,switch_off
from time import sleep

settings = config.load()

tempSwitch = settings['switches']['tempSwitch']
foggerSwitch = settings['switches']['foggerSwitch']
misterSwitch = settings['switches']['misterSwitch']
lightSwitch = settings['switches']['lightSwitch']

# Energenie actions based on socket positions
def foggerOn():
    log.logInfo("Switching on fogger")
    switch_on(foggerSwitch)

def foggerOff():
    log.logInfo("Switching off fogger")
    switch_off(foggerSwitch)

def misterOn():
    log.logInfo("Switching on mister")
    switch_on(misterSwitch)

def misterOff():
    log.logInfo("Switching off mister")
    switch_off(misterSwitch)

def temperatureOn():
    log.logInfo("Switching on temperature")
    switch_on(tempSwitch)

def temperatureOff():
    log.logInfo("Switching off temperature")
    switch_off(tempSwitch)

def lightOn():
    log.logInfo("Switching on light")
    switch_on(lightSwitch)

def lightOff():
    log.logInfo("Switching off light")
    switch_off(lightSwitch)

def misterOnTimed(seconds):
    log.logInfo("Switching on mister for %s seconds" % seconds)
    switch_on(misterSwitch)
    sleep(seconds)
    switch_off(misterSwitch)