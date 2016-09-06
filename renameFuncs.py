import renameException
from renameException import RenameException
import re
import os

countStringIndex = 0

def option_lower(parameters):
    '''Make stuff lowercase'''
    fileName = parameters[0]

    return fileName.lower()

def option_upper(parameters):
    '''Make stuff uppercase'''
    fileName = parameters[0]

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

    n = fileName.find(parameters[0])
    n2 = n + len(parameters[0])
    end = len(fileName)

    fileName = fileName[0:n] + parameters[1] + fileName[n2:end]

    return fileName

def option_number(parameters):
    '''Numbers the fileName with given countstring'''

    return fileName

def option_touch(parameters):
    '''sets date and time to now'''
    return fileName

def option_date(parameters):
    '''Set datestamp'''
    return fileName

def option_time(parameters):
    '''Set timestamp'''
    return fileName

def option_workingDir(parameters):
    '''Change directories'''
    if len(parameters) < 1:
        raise RenameException("Invalid number of workingDir arguments: " + str(parameters))
        return;

    os.chdir(parameters[0])
