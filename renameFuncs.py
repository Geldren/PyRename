'''
Module author: Leif Torgersen

Module containing functions for completing the operations associated with command line arguments in the rename.py program
'''

import re
import string
import files

def option_lower(fileName):
    '''Make a string all lowercase'''

    #Returns a lowercase version of name
    return fileName.lower()

def option_upper(fileName):
    '''Make a string all uppercase'''

    #Returns a uppercase version of name
    return fileName.upper()

def option_trim(n, fileName):
    '''Remove n characters from a string. If n is negative, they are removed from the end; if positive, the beginning.'''

    if n < 0:
        return fileName[0:n]
    else:
        return fileName[n:len(fileName)]

def option_rename(find, replace, fileName):
    '''Replace a section of a filename using regular expressions'''

    #takes in a string to modify, the substring to look for
    #the first place the substring is found, it is removed
    #and replaced with the specified replacement string
    fileName = re.sub(find, replace, fileName)

    return fileName

def option_number(countString, fileName):
    '''Change filenames to a specific name containing a number. Every call to the function will increase the number inserted by 1'''
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
    '''Set file date and time to current date and time'''

    #Sets date/time accessed and modified to current time
    files.touchFile(fileName)
    return fileName

def option_date(dateInput, fileName):
    '''Set file datestamp to requested datestamp'''

    files.setDate(dateInput, fileName)
    return fileName

def option_time(timeInput, fileName):
    '''Set file timestamp to requested timestamp'''

    files.setTime(timeInput, fileName)
    return fileName
