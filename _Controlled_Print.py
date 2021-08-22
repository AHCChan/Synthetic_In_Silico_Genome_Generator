HELP_DOC = """
CONTROLLED PRINT
(version 1.0)
by Angelo Chan

This is a library of print functions, the behaviour of which is controlled by
Global variables in the importing module.



REQUIRED GLOBALS:

PRINT_ERRORS (boolean)
PRINT_PROGRESS (boolean)
PRINT_METRICS (boolean)



EXAMPLE USAGE:

First, define the necessary global variables:
    
    PRINT_ERRORS = True
    PRINT_PROGRESS = True
    PRINT_METRICS = True

Then, import this module:
    
    import _Controlled_Print as PRINT

Then, apply those global variables to this module:
    
    PRINT.PRINT_ERRORS = PRINT_ERRORS
    PRINT.PRINT_PROGRESS = PRINT_PROGRESS
    PRINT.PRINT_METRICS = PRINT_METRICS
"""



# Functions ####################################################################

def printE(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing error messages.
    It can be controlled by a global variable.
    """
    if PRINT_ERRORS: print(string)

def printP(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing progress messages.
    It can be controlled by a global variable.
    """
    if PRINT_PROGRESS: print(string)

def printM(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing file metrics.
    It can be controlled by a global variable.
    """
    if PRINT_METRICS: print(string)


