'''
Module author: Andrew Stelter

The input module contains functions for getting input from the user.
Currently only contains the function getBoolInput, but could easily
be extended.
'''
def getBoolInput(prompt):
    '''Prompt the user for input and then read a value, attempting to interpret it as a boolean value. If interpretation fails, the default is False
    Values which are evaluated to true: 'y', 'yes', '1', 'true'
    Parameters:
        prompt - The string to print as a prompt to the user before recieving input
    Returns:
        boolean - Whether the value entered was a representation of true or false'''
    given = input(prompt).lower()
    
    if given == 'y' or given == 'yes' or given == '1' or given == 'true':
        return True
    return False  