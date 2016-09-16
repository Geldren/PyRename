'''
Module author: Leif Torgersen
'''

import re
import string
import files

def option_lower(fileName):
    '''Make stuff lowercase'''

    #Returns a lowercase version of name
    return fileName.lower()

def option_upper(fileName):
    '''Make stuff uppercase'''

    #Returns a uppercase version of name
    return fileName.upper()

def option_trim(n, fileName):
    '''Trim characters from front or back'''

    if n < 0:
        return fileName[0:n]
    else:
        return fileName[n:len(fileName)]

def option_rename(find, replace, fileName):
    '''Replaces a section of the name'''

    #Finds the start and end of the substring to be replaced
    n = fileName.find(find)
    n2 = n + len(find)
    end = len(fileName)
    #Cuts out old substring and reassembles the name around new one
    fileName = fileName[0:n] + replace + fileName[n2:end]

    return fileName

def option_number(countString, fileName):
    '''Numbers the fileName with given countstring'''
    try: option_number.counter += 1
    except: option_number.counter = 1

    poundLocations = []
    poundLocations = re.finditer('#+', countString)

    for loc in poundLocations:
        length = loc[1]-loc[0]
        replacement = '{:0>{1}}'.format(option_number.counter, length)
        countString[loc[0]:loc[1]] = replacement

    return fileName

def option_touch(fileName):
    '''sets date and time to now'''

    #Sets date/time accessed and modified to current time
    files.touchFile(fileName)
    return fileName

def option_date(dateInput, fileName):
    '''Set datestamp'''

    files.setDate(dateInput, fileName)
    return fileName

def option_time(timeInput, fileName):
    '''Set timestamp'''

    files.setTime(timeInput, fileName)
    return fileName
