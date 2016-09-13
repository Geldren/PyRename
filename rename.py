import os
import glob
import sys

#module containing the functions to actual work on files
import renameFuncs as of
import input
import files
import argparse

def addOperationAction(function):
    class OperationAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            try:
                currattr = getattr(namespace, self.dest)
                currattr.append([function, values])
                setattr(namespace, self.dest, currattr)
            except:
                setattr(namespace, self.dest, [[function, values]])

    return OperationAction

#Function to add all command line arguments to the a parser and return it
def buildParser():
    p = argparse.ArgumentParser(description="rename.py is a file renaming utility program which can be used to batch-rename files in a directory.\n\
    \n\tUSAGE: rename.py [options] file1 file2...\n\
    Below is a list of all supported options, what they do, and their parameters. Any command line arguments which are not options or option parameters will be interpreted as glob-style format strings to match file names\n\
    All other command line options which may modify files will be executed for each file in the order entered")

    p.add_argument("-t", "--trim", dest="nameops", metavar="N", type=int, nargs=1, action=addOperationAction(of.option_trim),
    help="Removes 'n'' characters from a string\nIf n is positive, they will be removed from the front\nIf n is negative, they will be removed from the end")
    
    p.add_argument("-r", "--replace", dest="nameops", metavar=("find","replace"), type=str, nargs=2, action=addOperationAction(of.option_rename),
    help="Searches filenames for 'pattern' and where it is found it is replaced with 'replace'\nSupports regEx capture groups")
    
    p.add_argument("-n", "--number", dest="nameops", metavar="countstring", type=str, nargs=1, action=addOperationAction(of.option_number),
    help="Renames files in sequence using 'countstring'\nAll files will be named whatever 'countstring' is, but any groups of # characters in countstring will be replaced by numbers\nExample:\n\trename.py -n text##\nFiles will be named 'text01' 'text02'...")
    
    p.add_argument("-D", "--date", dest="otherops", metavar="DDMMYYYY", type=str, nargs=1, action=addOperationAction(of.option_date),
    help="Updates file datestamps to the given one")
    
    p.add_argument("-T", "--time", dest="otherops", metavar="HHMMSS", type=str, nargs=1, action=addOperationAction(of.option_time),
    help="Updates file timestamps to the given one")
    
    p.add_argument("-l", "--lower", dest="nameops", action="append_const", const=[of.option_lower],       
    help="Changes filenames to be all lower-case")
    
    p.add_argument("-u", "--upper", dest="nameops", action="append_const", const=[of.option_upper],       
    help="Changes filenames to be all upper-case")
    
    p.add_argument("-dt", "--touch", dest="otherops", action="append_const", const=[of.option_touch],       
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
    help="Changes the working directory - Use to specify where the files to rename are\nCan be relative or absolute path")
    
    p.add_argument("globs", nargs="+", metavar="glob pattern", type=str,
    help="A list of glob strings to match files with")
    return p

#main entry point to program
def main(argv):
    '''Main execution function for renaming program'''

    #store working dir to move back later
    workingdir = os.getcwd()

    #build parser and parse args
    parser = buildParser()
    args=parser.parse_args()
    
    if args.workingdir != None:
        try:
            os.chdir(args.workingdir[0])
        except:
            print("Unable to change directory to", args.workingdir[0] + "; staying in", workingdir);
            os.chdir(workingdir);

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
    '''Goes through the file list, optionally querying user per file, and applies
    all operations specified in the command line arguments in the order they were given'''
    delete = args.delete
    interactive = args.interact
    printonly = args.print
    verbose = args.verbose

    for f in fileNames:
        if not os.path.isfile(f):
            if verbose or printonly:
                print(f, "is not a file; skipping...")
            continue

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
            if args.nameops != None:
                for o in args.nameops:
                    try:
                        newName = o[0](*((o[1]+[newName]) if len(o)>1 else [newName]))
                    except Exception as e:
                        print("Error:", e)
                        print("Exiting...")
                        return

            #print before/after names if requested
            if verbose or printonly:
                print(f, "-->", newName, "\n")
            #if not printonly, actually apply the name change
            if not printonly:
                files.renameFile(f, newName)
                f = newName

            #apply all functions which won't change the name
            if args.otherops != None:
                for o in args.otherops:
                    try:
                        o[0](*((o[1]+[f]) if len(o)>1 else [f]))
                    except Exception as e:
                        print("Error:", e)
                        print("Exiting...")
                        return
        else:
            print("Skipping",f,"...\n")


#Program Entry Point
main(sys.argv)