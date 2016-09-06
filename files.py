import os

def deleteFile(f):
    print("Delete", f)

def renameFile(f, new):
    os.rename(f, new)
    
