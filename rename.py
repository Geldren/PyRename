'''
Module author: Andrew Stelter

Assignment: Program 1 - File rename utility in python

Authors: Andrew Stelter, Leif Torgersen

Due: 9/22/16

Professor: Dr. John Weiss

Course: Programming Languages - 11:00 AM

Location: McLaury 205

Program description: This program has the ability to perform a number of operations
                     (including renaming with regEx) to a list of files. The user may
                     specify which operations to perform, and which files to perform
                     them on by calling rename.py with a variety of command line options.
                     All arguments for non-name-related operations (-D, -T, -d, -dt) will
                     be performed in the relative order they are entered, followed by all
                     name-related operations(-l, -u, -t, -r, -n) in the relative order that
                     they are entered. Command line arguments which are not an option or 
                     option parameters will be treated as a glob string to match file names.

Usage: rename.py [-h] [-t N] [-r find replace] [-n countstring] [-D DDMMYYYY]
                 [-T HHMMSS] [-l] [-u] [-dt] [-v] [-p] [-i] [-d] [-wd dir]
                 glob pattern [glob pattern ...]


positional arguments:
  glob pattern          A list of glob strings to match files with

optional arguments:
  -h, --help            Show this help message and exit
  -t N, --trim N        Removes 'n' characters from a string. If n is
                        positive, they will be removed from the front. If n is
                        negative, they will be removed from the end
  -r find replace, --replace find replace
                        Searches filenames for 'find' and where it is found
                        it is replaced with 'replace' Supports regEx capture
                        groups
  -n countstring, --number countstring
                        Renames files in sequence using 'countstring' All
                        files will be named whatever 'countstring' is, but any
                        groups of # characters in countstring will be replaced
                        by numbers. Example: rename.py -n text## Files will be
                        named 'text01' 'text02'...
  -D DDMMYYYY, --date DDMMYYYY
                        Updates file datestamps to the given one
  -T HHMMSS, --time HHMMSS
                        Updates file timestamps to the given one
  -l, --lower           Changes filenames to be all lower-case
  -u, --upper           Changes filenames to be all upper-case
  -dt, --touch          Updates file date/timestamps to the current date/time
  -v, --verbose         Outputs filenames before and after renaming
  -p, --print           Does not actually rename files; outputs what filenames
                        would be before and after renaming
  -i, --interactive     This program will query the user as to whether it
                        should process each file
  -d, --delete          Deletes all files matched
  -wd dir, --workingdir dir
                        Changes the working directory - Use to specify where
                        the files to rename are. Can be relative or absolute
                        path

Known Bugs:
Todo:
Progress Timeline:
Date    Modification
------  -----------------------------------------------------------
9/1/16  Wrote general main skeleton and simple command line parsing
        Named functions to be used for modifying filenames
        Paired command line arguments to functions
        Began writing renaming functions
        First working draft of main to run the functions associated
            the inputted command line parameters
        Added some exceptions raised in renaming functions
        Added custom exception type RenameException
9/2/16  Wrote custom argument parser because argparse documention is
            incredibly complicated and seems like overkill
        Wrote usage/help dialogue
9/5/16  More work on functions which actually modify filenames
9/6/16  Finished renaming functions except for -n and -r
9/8/16  Started working on -D, -T, and -dt functions
        Switched to argparse because it was discussed in class and 
            understood
        Added deletion functionality
        Switched renaming functions to take actual parameters instead
            of a list object (Learned about *list operator in class)
9/13/16 Finished -n function
        Fixed bug where using certain parameters first caused exceptions
9/14/16 Improvements to main() and processAllFilenames(), both are pretty
            short now
9/16/16 Lots of comments and docstrings added
'''

import os
import glob
import sys
import argparse

#module containing the functions to actual work on files
import renameFuncs as of
import input
import files

def addOperationAction(function):
    '''Create a custom action for argparser. This custom action is similar to const_append; however, it appends tuple which contains a constant function and the command line parameters for the argument.
    Parameters:
        function - The constant function to associate with the argument's parameters
    Returns:
        OperationAction type object'''
    class OperationAction(argparse.Action):
        '''Custom action class for argparser. Appends a tuple (function, values) to the list contained in dest as defined by argparse'''
        def __call__(self, parser, namespace, values, option_string=None):
            '''Call operator. Used by argparse to trigger the action having happend due to it's associated command line argument.
            If namespace does not have an attribute with a name matching self.dest, then that attibute is added.
            In either case, the tuple (function, values) is appended to the list contained in that attribute.
            Parameters:
                self - Self object
                parser - The argumentParser calling the action
                namespace - The eventual output of argumentparser.parse_args
                values - The parameters associated with the command line argument that triggered this action
                option_string - The optional string used to invoke the action. Will not be present if the command line argument is positional
            '''
            try:
                currattr = getattr(namespace, self.dest)
                currattr.append((function, values))
                setattr(namespace, self.dest, currattr)
            except:
                setattr(namespace, self.dest, [(function, values)])

    return OperationAction

#Function to add all command line arguments to the a parser and return it
def buildParser():
    '''Create an argparse.argumentParser for the rename.py program. The arguments are added such that each will be associated with a function and
    sorted depending upon the type of action it performs.
    Returns:
        argparse.ArgumentParser type object'''
    p = argparse.ArgumentParser(description="rename.py is a file renaming utility program which can be used to batch-rename files in a directory.\n\
    \n\tUSAGE: rename.py [options] file1 file2...\n\
    Below is a list of all supported options, what they do, and their parameters. Any command line arguments which are not options or option parameters will be interpreted as glob-style format strings to match file names\n\
    All other command line options which may modify files will be executed for each file in the order entered")

    p.add_argument("-t", "--trim", dest="nameops", metavar="N", type=int, nargs=1, action=addOperationAction(of.option_trim),
    help="Removes 'n'' characters from a string. If n is positive, they will be removed from the front. If n is negative, they will be removed from the end")
    
    p.add_argument("-r", "--replace", dest="nameops", metavar=("find","replace"), type=str, nargs=2, action=addOperationAction(of.option_rename),
    help="Searches filenames for 'pattern' and where it is found it is replaced with 'replace'. Supports regEx capture groups")
    
    p.add_argument("-n", "--number", dest="nameops", metavar="countstring", type=str, nargs=1, action=addOperationAction(of.option_number),
    help="Renames files in sequence using 'countstring'. All files will be named whatever 'countstring' is, but any groups of # characters in countstring will be replaced by numbers. Example:. \trename.py -n text##. Files will be named 'text01' 'text02'...")
    
    p.add_argument("-D", "--date", dest="otherops", metavar="DDMMYYYY", type=str, nargs=1, action=addOperationAction(of.option_date),
    help="Updates file datestamps to the given one")
    
    p.add_argument("-T", "--time", dest="otherops", metavar="HHMMSS", type=str, nargs=1, action=addOperationAction(of.option_time),
    help="Updates file timestamps to the given one")
    
    p.add_argument("-l", "--lower", dest="nameops", action="append_const", const=(of.option_lower,),       
    help="Changes filenames to be all lower-case")
    
    p.add_argument("-u", "--upper", dest="nameops", action="append_const", const=(of.option_upper,),       
    help="Changes filenames to be all upper-case")
    
    p.add_argument("-dt", "--touch", dest="otherops", action="append_const", const=(of.option_touch,),       
    help="Updates file date/timestamps to the current date/time")
    
    p.add_argument("-v", "--verbose", dest="verbose", action="store_true",                              
    help="Outputs filenames before and after renaming")
    
    p.add_argument("-p", "--print", dest="print", action="store_true",                                
    help="Does not actually rename files; outputs what filenames would be before and after renaming")
    
    p.add_argument("-i", "--interactive", dest="interact", action="store_true",                          
    help="This program will query the user as to whether it should process each file")
    
    p.add_argument("-d", "--delete", dest="delete", action="store_true",                                
    help="Deletes all files matched")
    
    p.add_argument("-wd", "--workingdir", dest="workingdir", metavar="dir", type=str, nargs=1, 
    help="Changes the working directory - Use to specify where the files to rename are. Can be relative or absolute path")
    
    p.add_argument("globs", nargs="+", metavar="glob pattern", type=str,
    help="A list of glob strings to match files with")
    return p

#main entry point to program
def main(argv):
    '''Main execution function for renaming program
    Steps of exection:
        Store current working directory
        Create argumentparser
        Parse arguments
        If a working directory change was requested, attempt to change to the new directory
        Get the list of glob strings to match, and use glob.glob to get a list of matching filenames
        Call the processAllFilenames function to do all work
        Change back to the original working directory'''

    #store working dir to move back later
    workingdir = os.getcwd()

    #build parser and parse args
    parser = buildParser()
    args=parser.parse_args()
    
    #optionally attempt to change directory
    if args.workingdir != None:
        try:
            os.chdir(args.workingdir[0])
        except:
            print("Unable to change directory to", args.workingdir[0] + "; Exiting...")
            return

    #convert blob shorthands to full file list
    globs = args.globs
    fileNames = []
    for g in globs:
        fileNames += glob.glob(g)

    #process ALL the files
    processAllFilenames(args, fileNames)

    #move back to original directory
    os.chdir(workingdir)


def processAllFilenames(args, fileNames):
    '''Go through the file list, optionally querying user per file, and apply
    all operations specified in the command line arguments in the order they were given with 2 exceptions:
        1) If -d was specified, no other operations will occur
        2) The operation which do not change the name of the file (-D, -T, -dt) will occur first, in their respective order'''
    delete = args.delete
    interactive = args.interact
    printonly = args.print
    verbose = args.verbose

    #loop through file names
    for f in fileNames:
        #make sure the name is maps to a file, nothing else
        #optionally output a message to the user
        if not os.path.isfile(f):
            if verbose or printonly:
                print(f, "is not a file; skipping...")
            continue

        run = True

        ops = []
        #Create a list of all operations to run on each file
        #the list will be [[non-renaming operations][renaming operations]]
        #This allows the operations which need the actual filename on disk to occur
        #before the name changes and prevents having to do two separate loops
        if args.otherops != None:
            ops += args.otherops
        if args.nameops != None:
            ops += args.nameops

        #if interactive prompt user for each file
        if interactive:
            run = input.getBoolInput("Process file" + f + "? (y/n)\n>")
        if run:
            #special case delete
            if delete:
                files.deleteFile(f)
                continue

            #apply all operational functions in order specified
            newName = f
            for o in ops:
                try:
                    #for each tuple o in the operations list, attempt to call
                    #o[0] as a function with the arguments being the list of command line argument parameters + the current name of the file
                    #the return value will be what the name of the file should be changed to
                    #All of the functions called here come from renamefuncs.py, and have parameters matching this format
                    newName = o[0](*((o[1]+[newName]) if len(o)>1 else [newName]))
                except Exception as e:
                    #if any exceptions occur, cut program exection after presenting the error to the user
                    print("Error:", e)
                    print("Exiting...")
                    return

            #print before/after names if requested
            if verbose or printonly:
                print(f, "-->", newName)
            #if not printonly, actually apply the name change
            if not printonly:
                try:
                    files.renameFile(f, newName)
                except Exception as ex:
                    print("Unable to rename", "'"+ex.args[0]+"'", "to", "'"+ex.args[1]+"'", "\n")
        else:
            print("Skipping",f,"...\n")


#Pseudo-main function to allow use as standalone program or module
if __name__ == '__main__':
    main(sys.argv)