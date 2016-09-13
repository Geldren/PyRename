import os
import time

from datetime import datetime
from datetime import date

def deleteFile(f):
    os.remove(f)

def renameFile(f, new):
    os.rename(f, new)
    
def touchFile(f):
    os.utime(f)

def setDate(dateString, f):
    if len(dateString) != 8:
        raise Exception("Invalid date string; use the format DDMMYYYY")
        return

    #Get the original time created and modified
    creation = datetime.fromtimestamp(os.path.getctime(f))
    modification = datetime.fromtimestamp(os.path.getmtime(f))

    #Pull the day, month, and year out of the input
    day = int(dateString[0:2])
    month = int(dateString[2:4])
    year = int(dateString[4:8])

    #Create new timestamps by merging the original times with the new date
    newCreation = datetime(year, month, day, \
                           creation.hour, creation.minute, creation.second)

    newModification = datetime(year, month, day, \
                               modification.hour, modification.minute, modification.second)

    os.utime(f, (time.mktime(newCreation.timetuple()),\
                 time.mktime(newModification.timetuple())))

def setTime(timeString, f):
    if len(timeString) != 6:
        raise Exception("Invalid time string; use the format HHMMSS")
        return

    #Get the original time created and modified
    creation = datetime.fromtimestamp(os.path.getctime(f))
    modification = datetime.fromtimestamp(os.path.getmtime(f))

    #Pull the day, month, and year out of the input
    hour = int(timeString[0:2])
    minute = int(timeString[2:4])
    second = int(timeString[4:6])

    #Create new timestamps by merging the original times with the new date
    newCreation = datetime(creation.year, creation.month, creation.day, \
                           hour, minute, second)

    newModification = datetime(modification.year,  modification.month,  modification.day, \
                               hour, minute, second)

    os.utime(f, (time.mktime(newCreation.timetuple()),\
                 time.mktime(newModification.timetuple())))