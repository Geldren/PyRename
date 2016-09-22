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

    #takes in a string to modify, the substring to look for
    #the first place the substring is found, it is removed
    #and replaced with the specified replacement string
    fileName = re.sub(find, replace, fileName)

    return fileName

def option_number(countString, fileName):
    '''Numbers the fileName with given countstring'''
    if(countString.find('#') < 0):
        raise Exception("countString does not contain any # symbols")
        return
    try: option_number.counter += 1
    except: option_number.counter = 1
    #Finds all # signs in countstring
    poundLocations = []
    poundLocations = re.finditer('(#+)', countString)
    #For each # string, it creates a string with the counter and a fill character of 0
    for loc in poundLocations:
        inds = loc.span()
        length = inds[1]-inds[0]
        replacement = '{0:{fill}>{width}}'.format(option_number.counter, width=length, fill='0')
        countString = countString[0:inds[0]]+replacement+countString[inds[1]:]
    return countString

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
