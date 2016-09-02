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
TYPE_SPECIAL = 'spec'

def main(argv):
    '''Main execution function for renaming program'''
    workingdir = os.getcwd()

    parser = buildParser()
    parser.parseArgs(argv)

    specs = parser.getArgType(TYPE_SPECIAL)
    if '-h' in specs:
        usage(parser)
        return
    
    actions = parser.getArgType(TYPE_ACTION)
    for a in actions:
        try:
            a.trigger()
        except RenameException as e:
            print("Error:",e.message)

    globs = parser.getArgType(Argument.TYPE_DEFAULT)
    fileNames = []
    for g in globs:
        fileNames += glob.glob(g)

    ops = parser.getArgType(TYPE_OPERATION)
    opts = parser.getArgType(TYPE_OPTION)

    options = []
    for o in opts:
        options.append(o.defaultAlias())

    processAllFilenames(ops, fileNames, options)

    os.chdir(workingdir)

def usage(parser):
    '''Prints a help menu for rename.py'''
    print("Usage: ")

def buildParser():
    p = arguments.ArgumentParser()
    p.addArgument(Argument(["-t", "--trim"],        TYPE_OPERATION, 1, [of.option_trim]))
    p.addArgument(Argument(["-r", "--replace"],     TYPE_OPERATION, 2, [of.option_rename]))
    p.addArgument(Argument(["-n", "--number"],      TYPE_OPERATION, 1, [of.option_number]))
    p.addArgument(Argument(["-D", "--date"],        TYPE_OPERATION, 1, [of.option_date]))
    p.addArgument(Argument(["-T", "--time"],        TYPE_OPERATION, 1, [of.option_time]))
    p.addArgument(Argument(["-l", "--lower"],       TYPE_OPERATION, 1, [of.option_lower]))
    p.addArgument(Argument(["-u", "--upper"],       TYPE_OPERATION, 1, [of.option_upper]))
    p.addArgument(Argument(["-dt", "--touch"],      TYPE_OPERATION, 0, [of.option_touch]))
    p.addArgument(Argument(["-h", "--help"],        TYPE_SPECIAL))
    p.addArgument(Argument(["-v", "--verbose"],     TYPE_OPTION))
    p.addArgument(Argument(["-p", "--print"],       TYPE_OPTION))
    p.addArgument(Argument(["-i", "--interactive"], TYPE_OPTION))
    p.addArgument(Argument(["-d", "--delete"],      TYPE_OPTION))
    p.addArgument(Argument(["-wd", "--workingdir"], TYPE_ACTION,    1, [of.option_workingDir]))
    return p

def processAllFilenames(ops, fileNames, options):
    for f in fileNames:
        run = True

        #if interactive prompt user for each file
        if "-i" in options:
            run = input.getBoolInput("Process file" + f + "? (y/n)\n>")
        if run:
            #special case delete
            if "-d" in options:
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
            if "-v" in options or "-p" in options:
                print(f, "-->", newName, "\n")
            #if not printonly, actually apply the name change
            if "-p" not in options:
                files.renameFile(f, newName)
                f = newName
        else:
            print("Skipping",f,"...\n")


#Program Entry Point
main(sys.argv)