import syslog

programName = "vivpi"

syslog.openlog(ident=programName,logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)
#syslog.syslog('VivPi logging started...')


def logError(message):
    syslog.syslog(syslog.LOG_ERR, message)

def logInfo(message):
    syslog.syslog(syslog.LOG_INFO, message)

def logWarn(message):
    syslog.syslog(syslog.LOG_WARNING, message)

def logDebug(message):
    syslog.syslog(syslog.LOG_DEBUG, message)

def logEmerg(message):
    syslog.syslog(syslog.LOG_EMERG, message)

def closeLogging():
    syslog.syslog(syslog.LOG_INFO, "Stopping logging")
    syslog.closelog()
