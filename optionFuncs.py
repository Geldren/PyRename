import renameException
import re

def option_lower(parameters, fileName):
    '''Make stuff lowercase'''

    return fileName.lower()

def option_upper(parameters, fileName):
    '''Make stuff uppercase'''

    return fileName.upper()

def option_trim(parameters, fileName):
    '''Trim characters from front or back'''

    #Try to interpret param as number; if fail, raise exception with single error message string to be handled in main
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

def option_rename(parameters, fileName):
    '''Replaces the whole name'''
    return parameters[0]

def option_number(parameters, fileName):
    '''Numbers the fileName with given countstring'''
    return fileName

def option_touch(parameters, fileName):
    '''sets date and time to now'''

def option_date(parameters, fileName):
    '''Set datestamp'''

def option_time(parameters, fileName):
    '''Set timestamp'''
