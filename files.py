'''
Module author: Andrew Stelter and Leif Torgersen

The files module contains a number of useful functions
abstracting the os calls required to work with files.
'''

import os
import time

from datetime import datetime
from datetime import date

def deleteFile(f):
    '''Delete a file
    Parameters: 
        f - The name of the file to delete'''
    os.remove(f)

def renameFile(f, new):
    '''Change the name of a file to a different name
    Parameters: 
        f - The name of the file to rename
        new - The name to change the filename to'''
    os.rename(f, new)
    
def touchFile(f):
    '''Update the modification time of a file to the current time
    Parameters: 
        f - The name of the file to update'''
    os.utime(f)

def setDate(dateString, f):
    '''Change the dates of creation and modification of a file without changing the times of creation and modification
    Parameters:
        dateString - String encoding of the date to change to. Should be of the form DDMMYYYY
        f - The name of the file to update'''
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
    '''Change the times of creation and modification of a file without changing the dates of creation and modification
    Parameters:
        timeString - String encoding of the date to change to. Should be of the form HHMMSS
        f - The name of the file to update'''
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