import os
import glob
import sys

#module containing the functions to actual work on files
import optionFuncs as of
import input
import files
import renameException

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
            ['-dt', '--touch'],
            ['-wd', '--workingdir']]

#Dictionary of how many extra parameters go with each cmd option
OPTIONARGS = {'-t': 1,'-r': 2,'-n': 1,'-D': 1,'-T': 1,
              '-l': 0,'-u': 0,'-h': 0,'-v': 0,'-p': 0,
              '-i': 0,'-d': 0,'-dt':0, '-wd':1}

#Dictonary of functions for arguments
OPTIONFUNCTIONS = {'-t': of.option_trim, '-r': of.option_rename, '-n': of.option_number,'-l': of.option_lower, '-u': of.option_upper,
                   '-D': of.option_date, '-T': of.option_time, '-dt': of.option_touch}

RENAMEORDER = ['d', '-l', '-u', '-t', '-r', '-n']
OTHERORDER = ['-t', '-D', '-T']

def main(argv):
    '''Main execution function for renaming program'''
    workingdir = os.getcwd()

    ops, fileNames, options = parseArgs(argv)

    processAllFilenames(ops, fileNames, options)

    os.chdir(workingdir)
    
def getArgAlias(arg):
    '''Checks if an argument is an alias and returns the most simple form if so; returns the argument if not'''
    for a in ARGALIAS:
        if arg in a:
            return a[0]
    return arg

def usage():
    '''Prints a help menu for rename.py'''
    print("Usage: ")

def processAllFilenames(ops, fileNames, options):
    for f in fileNames:
        run = True

        #if interactive prompt user for each file
        if options["interactive"]:
            run = input.getBoolInput("Process file" + f + "? (y/n)")
        if run:
            #special case delete
            if options["delete"]:
                files.deleteFile(f)
                continue

            #apply all rename functions in order
            newName = f
            for o in RENAMEORDER:
                if o in ops:
                    #Try-catch in case something is invalid about the arguments given
                    try:
                        newName = OPTIONFUNCTIONS[o](options[o], newName)
                    except Exception as e:
                        if len(e.args) < 1:
                            print("Unexpected exception:", e)
                    except RenameException as e:
                            print("Exception: ", e.message)

            #print before/after names if requested
            if options["verbose"] or options["printonly"]:
                print(f, "-->", newName)
            #if not printonly, actually apply the name change
            if not options["printonly"]:
                files.renameFile(f, newName)
                f = newName

            #apply all non-rename functions in order
            for o in OTHERORDER:
                if o in ops:
                    #Try-catch in case something is invalid about the arguments given
                    try:
                        OPTIONFUNCTIONS[o](options[o], f)
                    except Exception as e:
                        if len(e.args) < 1:
                            print("Unexpected exception:", e)
                    except RenameException as e:
                            print("Exception: ", e.message)

def parseArgs(argv):
    '''Function to parse the arguments passed in to the program'''
    options = {}
    operations = {}
    fileGlobs = []
    fileNames = []
    
    options['interactive'] = options['printonly'] = options['verbose'] = options['delete'] = False

    i=1
    while i < len(argv):
        #normalize options
        arg = getArgAlias(argv[i]);

        #check for special case options
        if arg == '-i':
            options['interactive'] = True
        elif arg == '-p':
            options['printonly'] = True
        elif arg == '-v':
            options['verbose'] = True
        elif arg == '-h':
            usage()
            return
        elif arg == '-d':
            options['delete'] = True
        elif arg == '-wd':
            i += 1
            try:
                print("Moving to",argv[i])
                os.chdir(argv[i])
            except:
                print("Failed to move to directory", argv[i])
                return;

        #if known option, get extra argument options
        elif arg in OPTIONARGS:
            argList = []

            #read n arguments
            for j in range(OPTIONARGS[arg]):
                #increment i to skip parameters
                i += 1
                argList.append(argv[i])

            #add arg and parameters to options list
            operations[arg] = argList
        else:
            #otherwise, assume filename
            fileGlobs.append(arg)

        #increment i
        i+=1

    #Assume each file name is a glob format and expand it to an actual file list
    for f in fileGlobs:
        fileNames += glob.glob(f)

    return operations, fileNames, options


#Program Entry Point
main(sys.argv)