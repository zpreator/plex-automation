import numpy as np
import datetime
import re

def GetPreviousTime():
    previous_time = np.loadtxt("C:\\Repos\\plex-automation\\youtubeLog.txt", dtype=str)
    previous_datetime = datetime.datetime.fromisoformat(str(previous_time))
    return previous_datetime

def GetCurrentTime(date):
    time = re.findall("[\d]{1,2} [ADFJMNOS]\w* [\d]{4} [0-9][0-9]:[0-9][0-9]:[0-9][0-9]", date)[0]
    datetime_ = datetime.datetime.strptime(time, '%d %b %Y %H:%M:%S')
    return datetime_

def SetCurrentTime(date):
    iso = GetCurrentTime(date).isoformat() # Gets most recent url
    np.savetxt("C:\\Repos\\plex-automation\\youtubeLog.txt", np.array([iso]), fmt='%s') # Saves most recent url date