import os
import glob
import sys

#module containing the functions to actual work on files
import renameFuncs as of
import input
import files
import renameException
from renameException import RenameException
import arguments
from arguments import Argument

TYPE_OPERATION = 'oper'
TYPE_OPTION = 'opt'
TYPE_ACTION = 'act'
TYPE_HELP = 'spec'

#Function to add all command line arguments to the a parser and return it
def buildParser():
    p = arguments.ArgumentParser()
    p.addArgument(Argument(["-t", "--trim"],        TYPE_OPERATION, 1, [of.option_trim],        argNames=["n"], desc=["Removes 'n'' characters from a string","If n is positive, they will be removed from the front","If n is negative, they will be removed from the end"]))
    p.addArgument(Argument(["-r", "--replace"],     TYPE_OPERATION, 2, [of.option_rename],      argNames=["pattern","replace"], desc=["Searches filenames for 'pattern' and where it is found it is replaced with 'replace'","Supports regEx capture groups"]))
    p.addArgument(Argument(["-n", "--number"],      TYPE_OPERATION, 1, [of.option_number],      argNames=["countstring"], desc=["Renames files in sequence using 'countstring'","All files will be named whatever 'countstring' is, but any groups of # characters in countstring will be replaced by numbers","Example:","\trename.py -n text##","Files will be named 'text01' 'text02'..."]))
    p.addArgument(Argument(["-D", "--date"],        TYPE_OPERATION, 1, [of.option_date],        argNames=["DDMMYYYY"], desc=["Updates file datestamps to the given one"]))
    p.addArgument(Argument(["-T", "--time"],        TYPE_OPERATION, 1, [of.option_time],        argNames=["HHMMSS"], desc=["Updates file timestamps to the given one"]))
    p.addArgument(Argument(["-l", "--lower"],       TYPE_OPERATION, 0, [of.option_lower],       desc=["Changes filenames to be all lower-case"]))
    p.addArgument(Argument(["-u", "--upper"],       TYPE_OPERATION, 0, [of.option_upper],       desc=["Changes filenames to be all upper-case"]))
    p.addArgument(Argument(["-dt", "--touch"],      TYPE_OPERATION, 0, [of.option_touch],       desc=["Updates file date/timestamps to the current date/time"]))
    p.addArgument(Argument(["-h", "--help"],        TYPE_HELP,                                  desc=["Displays this help screen"]))
    p.addArgument(Argument(["-v", "--verbose"],     TYPE_OPTION,                                desc=["Outputs filenames before and after renaming"]))
    p.addArgument(Argument(["-p", "--print"],       TYPE_OPTION,                                desc=["Does not actually rename files; outputs what filenames would be before and after renaming"]))
    p.addArgument(Argument(["-i", "--interactive"], TYPE_OPTION,                                desc=["rename.py will query the user as to whether it should process each file"]))
    p.addArgument(Argument(["-d", "--delete"],      TYPE_OPTION,                                desc=["Deletes all files matched"]))
    p.addArgument(Argument(["-wd", "--workingdir"], TYPE_ACTION,    1, [of.option_workingDir],  argNames=["dir"], desc=["Changes the working directory - Use to specify where the files to rename are\nCan be relative or absolute path"]))
    return p

#main entry point to program
def main(argv):
    '''Main execution function for renaming program'''

    #store working dir to move back later
    workingdir = os.getcwd()

    #build parser and parse args
    parser = buildParser()
    parser.parseArgs(argv)

    #check for -h argument
    help = parser.getArgType(TYPE_HELP)
    if len(help) > 0:
        usage(parser)
        return
    
    #do any immediate action arguments (-wd)
    actions = parser.getArgType(TYPE_ACTION)
    for a in actions:
        try:
            a.trigger()
        except RenameException as e:
            print("Error:",e.message)
        except Exception as e:
            print("Unknown Exception:",e)

    #convert blob shorthands to full file list
    globs = parser.getArgType(Argument.TYPE_DEFAULT)
    fileNames = []
    for g in globs:
        fileNames += glob.glob(g)

    #get option and operation arguments
    ops = parser.getArgType(TYPE_OPERATION)
    opts = parser.getArgType(TYPE_OPTION)

    #translate option arguments to just string aliases
    options = []
    for o in opts:
        options.append(o.defaultAlias())

    #process ALLLL the files
    processAllFilenames(ops, fileNames, options)

    #move back to original directory
    os.chdir(workingdir)

def usage(parser):
    '''Prints a help menu for rename.py'''
    print("-"*20,"rename.py -- Help","-"*20, sep="|")
    print("rename.py is a file renaming utility program which can be used to batch-rename files in a directory.")
    print("\n\tUSAGE:", "rename.py [options] file1 file2...\n")
    print("Below is a list of all supported options, what they do, and their parameters. Any command line arguments which are not options or option parameters will be interpreted as glob-style format strings to match file names","\n")
    print("All other command line options which may modify files will be executed for each file in the order entered")
    print(parser.generateHelp());    

def processAllFilenames(ops, fileNames, options):
    '''Goes through the file list, optionally querying user per file, and applies
    all operations specified in the command line arguments in the order they were given'''
    delete = '-d' in options
    interactive = '-i' in options
    printonly = '-p' in options
    verbose = '-v' in options
    for f in fileNames:
        run = True

        #if interactive prompt user for each file
        if interactive:
            run = input.getBoolInput("Process file" + f + "? (y/n)\n>")
        if run:
            #special case delete
            if delete:
                files.deleteFile(f)
                continue

            #apply all rename functions in order specified
            newName = f
            for o in ops:
                try:
                    newName = (o.trigger([newName])[0])
                except RenameException as e:
                    print("Error:", e.message)
                except Exception as e:
                    print("Unknown exception:", e)

            #print before/after names if requested
            if verbose or printonly:
                print(f, "-->", newName, "\n")
            #if not printonly, actually apply the name change
            if not printonly:
                files.renameFile(f, newName)
                f = newName
        else:
            print("Skipping",f,"...\n")


#Program Entry Point
main(sys.argv)