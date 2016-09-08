import renameException
from renameException import RenameException
import re
import os
from datetime import datetime
from datetime import time
from datetime import date

def option_lower(parameters):
    '''Make stuff lowercase'''
    fileName = parameters[0]
    #Returns a lowercase version of name
    return fileName.lower()

def option_upper(parameters):
    '''Make stuff uppercase'''
    fileName = parameters[0]
    #Returns a uppercase version of name
    return fileName.upper()

def option_trim(parameters):
    '''Trim characters from front or back'''
    if len(parameters) < 2:
        raise RenameException("Invalid number of trim arguments: " + str(parameters))
        return

    #Try to interpret param as number; if fail, raise exception with single error message string to be handled in main
    fileName = parameters[1]
    n = 0
    try:
        n = int(parameters[0])
    except:
        raise RenameException("Invalid trim option: " + str(n))
        return

    if n < 0:
        return fileName[0:n]
    else:
        return fileName[n:len(fileName)]

def option_rename(parameters):
    '''Replaces a section of the name'''
    fileName = parameters[2]
    #Finds the start and end of the substring to be replaced
    n = fileName.find(parameters[0])
    n2 = n + len(parameters[0])
    end = len(fileName)
    #Cuts out old substring and reassembles the name around new one
    fileName = fileName[0:n] + parameters[1] + fileName[n2:end]

    return fileName

def option_number(parameters):
    '''Numbers the fileName with given countstring'''
    fileName = parameters[0]
    counts = []

    for i in fileName
        if i == '#'
            counts += [i]

    for j in count

    return fileName

def option_touch(parameters):
    '''sets date and time to now'''
    fileName = parameters[0]
    #Sets date/time accessed and modified to current time
    os.utime(fileName)
    return fileName

def option_date(parameters):
    '''Set datestamp'''
    fileName = parameters[1]
    dateInput = parameters[0]

    #Converts date into timestamp value
    dateInput = date(dateInput[4:], dateInput[2:4], dateInput[:2])
    time.mktime(dateInput.timetuple())

    #Creates tuple for utime
    dateInput = (dateInput, dateInput)
    os.utime(fileName, dateInput)
    return fileName

def option_time(parameters):
    '''Set timestamp'''
    fileName = parameters[1]
    timeInput = parameters[0]

    #Converts time into timestamp value
    timeInput = time(timeInput[:2], timeInput[2:4], timeInput[4:])
    time.mktime(timeInput.timetuple())

    #Creates tuple for utime
    timeInput = (timeInput, timeInput)
    os.utime(fileName, time)
    return fileName

def option_workingDir(parameters):
    '''Change directories'''
    if len(parameters) < 1:
        raise RenameException("Invalid number of workingDir arguments: " + str(parameters))
        return;

    os.chdir(parameters[0])
