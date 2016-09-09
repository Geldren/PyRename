import os

from datetime import datetime
from datetime import time
from datetime import date

def deleteFile(f):
    os.remove(f)

def renameFile(f, new):
    os.rename(f, new)
    
def touchFile(f):
    os.utime(f)

def setDate(dateString, f):
    #Converts date into timestamp value
    dateString = date(dateString[4:], dateString[2:4], dateString[:2])
    time.mktime(dateInput.timetuple())

    #Creates tuple for utime
    dateInput = (dateString, dateString)
    os.utime(f, dateInput)

def setTime(timeString, f):
    #Converts time into timestamp value
    timeString = time(timeString[:2], timeString[2:4], timeString[4:])
    time.mktime(timeString.timetuple())

    #Creates tuple for utime
    timeInput = (timeString, timeString)
    os.utime(f, timeInput)