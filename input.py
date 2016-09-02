def getBoolInput(prompt):
    '''Get an input and attempt to interpret it as a boolean; defaults to false'''
    given = input(prompt).lower()
    
    if given == 'y' or given == 'yes' or given == '1' or given == 'true':
        return True
    return False  