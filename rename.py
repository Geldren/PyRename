import os
import glob
import re
import sys

#modules containing the functions to actual work on files
import renaming_options as ro
import other_options as oo

#List of groups of cmd options that mean the same thing
ARGALIAS = [['-t', '--trim'],
            ['-r', '--replace'],
            ['-n', '--number'],
            ['-D', '--date'],
            ['-T', '--time'],
            ['-l', '--lower'],
            ['-u', '--upper'],
            ['-h', '--help'],
            ['-v', '--verbose'],
            ['-p', '--print'],
            ['-i', '--interactive'],
            ['-d', '--delete'],
            ['-dt', '--touch']]

#Dictionary of how many extra parameters go with each cmd option
OPTIONARGS = {'-t': 1,'-r': 2,'-n': 1,'-D': 1,'-T': 1,
              '-l': 0,'-u': 0,'-h': 0,'-v': 0,'-p': 0,
              '-i': 0,'-d': 0,'-dt':0}

OPTIONFUNCTIONS = {'-t': ro.option_trim, '-r': ro.option_replace, '-n': ro.option_number, '-D': oo.option_date,
                   '-T': oo.option_time, '-l': ro.option_lower, '-u': ro.option_upper,
                   '-d': oo.option_date, '-dt': oo.option_touch}

OPTIONORDER = ['d', '-l', '-u', '-t', '-r', '-n', '-t', '-D', '-T']

def main(argv):
    '''Main execution function for renaming program'''
    options = []
    fileGlobs = []
    files = []

    interactive = printonly = verbose = False;

    i=1
    while i < len(argv):
        #normalize options
        arg = getArgAlias(argv[i]);

        #check for special case options
        if arg == '-i':
            interactive = True
        elif arg == '-p':
            printonly = True
        elif arg == '-v':
            verbose = True
        elif arg == '-h':
            usage()
            return
        #if known option, get extra argument options
        elif arg in OPTIONARGS:
            argList = [arg]

            #read n arguments
            for j in range(OPTIONARGS[arg]):
                #increment i to skip parameters
                i += 1
                argList.append(argv[i])

            #add arg and parameters to options list
            options.append(argList)
        else:
            #otherwise, assume filename
            fileGlobs.append(arg)

        #increment i
        i=i+1

    print("Arguments: ", options)
    print("Files Globs: ", fileGlobs)

    #Assume each file name is a glob format and expand it to an actual file list
    for f in fileGlobs:
        file += glob.glob(f)

    print("Files: ", files)

def getArgAlias(arg):
    '''Checks if an argument is an alias and returns the most simple form if so; returns the argument if not'''
    for a in ARGALIAS:
        if arg in a:
            return a[0]
    return arg

def usage():
    '''Prints a help menu for rename.py'''
    print("Usage: ")


#Program Entry Point
main(sys.argv)