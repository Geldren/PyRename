import os
import glob
import re
import sys

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

#Dictionary of how many extra arguments go with each cmd option
OPTIONARGS = {'-t': 1,
              '-r': 2,
              '-n': 1,
              '-D': 1,
              '-T': 1,
              '-l': 0,
              '-u': 0,
              '-h': 0,
              '-v': 0,
              '-p': 0,
              '-i': 0,
              '-d': 0,
              '-dt':0}

def main(argv):
    options = [];
    files = [];

    i=1
    while i < len(argv):
        #normalize options
        arg = getArgAlias(argv[i]);

        #if known option, get extra argument options
        if arg in OPTIONARGS:
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
            files.append(arg)

        #increment i
        i=i+1

    print("Arguments: ", options)
    print("Files: ", files)

def getArgAlias(arg):
    for a in ARGALIAS:
        if arg in a:
            return a[0]
    return arg




#Program Entry Point
main(sys.argv)