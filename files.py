import os

def deleteFile(f):
    os.remove(f)

def renameFile(f, new):
    os.rename(f, new)
    
