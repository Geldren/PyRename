def option_lower(parameters, files):
    print("Make stuff lowercase")

    return files.lower()

def option_upper(parameters, files):
    print("Make stuff uppercase")

    return files.upper()

def option_trim(parameters, files):
    print("Trim characters from front or back")

    n = 0

    #Try to interpret param as number; if fail, raise exception with single error message string to be handled in main
    try:
        n = int(parameters[0])
    except:
        raise Exception("Invalid trim option: " + str(n))
        return

    if n < 0:
        return( files[0:(len(files)-n)])
    else:
        return( files[(n+1):(len(files)-1)])

def option_rename(parameters, files):
    print("Replaces the whole name")

def option_number(parameters, files):
    print("Numbers the files with given countstring")
def option_touch(parameters, files):
    print("sets date and time to now")
def option_date(parameters, files):
    print("Set datestamp")
def option_time(parameters, files):
    print("Set timestamp")