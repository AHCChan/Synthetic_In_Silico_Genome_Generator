"""
COMMAND LINE PARSER
(version 1.0)
by Angelo Chan

This is a library of functions useful for parsing command line inputs and
verifying them.
"""



# Configurations ###############################################################

# Minor Configurations #########################################################

# Defaults #####################################################################

# Imported Modules #############################################################

import sys
import os



# Enums ########################################################################

# Strings ######################################################################

STR__no_inputs = "\nERROR: No inputs were given."
STR__insufficient_inputs = "\nERROR: Not enough inputs were given."

STR__IO_error_read = "\nERROR: Input file does not exist or could not be "\
        "opened."

STR__IO_error_write_folder_nonexistent = """
ERROR: You specified an output folder which does not exist and cannot be
created. Please specify a different output folder."""
STR__IO_error_write_folder_cannot = """
ERROR: You specified an output folder which you do not have the authorization
to write into. Please specify a different output folder."""
STR__IO_error_write_folder_forbid = """
ERROR: You specified an output folder which already exists and the administrator
for this program has forbidden all overwrites. Please specify a different
output folder, move the currently existing folder, or configure the default
options in Generate_Random_Chromosomes.py."""
STR__IO_error_write_unexpected = """
ERROR: An unexpected error occured with the specified output path. Contact the
developers because this error should never be triggered from normal usage of
this software."""

STR__overwrite_confirm = "\nFile already exists in:\n\t{f}\nDo you wish to "\
        "overwrite it? (y/n): "

STR__overwrite_accept = "\nWARNING: Existing files will be overwritten."
STR__overwrite_decline = "\nThe user has opted not to overwrite existing "\
        "files.\nThe program will now terminate."

STR__invalid_width = """
ERROR: Invalid width: {s}
Please specify a positive integer.
"""

STR__parsing_args = "\nParsing arguments..."



# Lists ########################################################################

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]



# Dictionaries #################################################################

# Communications and Metrics ###################################################

def Pad_Str(string, size, char=" ", side=0):
    """
    Return a padded version of a string.
    Return the original string if the desired string length is smaller than the
    length of the original string.
    
    @string
            (str)
            The string to be padded.
    @size
            (int)
            The length of the final string.
    @char   
            (str)
            The character used to pad the string.
            (DEFAULT: whitespace)
    @side
            (int)
            An integer indicating which side the padding is to be added.
            0 for the padding to be added to the left.
            Any other integer for the padding to be added to the right.
            (DEFAULT: left)
    
    Pad_Str(str, int, str, int) -> str
    """
    length = len(string)
    difference = size - length
    if difference < 0: return string
    padding = difference * char
    if side == 0: return padding+string
    return string+padding

def Trim_Percentage_Str(string, max_decimal_places):
    """
    Return a trimmed version of a string containing a percentage.
    
    @string
            (str)
            The string to be trimmed.
    @max_decimal_places
            (int)
            The maximum number of decimal places the resulting string will
            contain.
    
    Trim_Percentage_Str(str, int) -> str
    """
    string = string + max_decimal_places * "0"
    index = string.index(".") + max_decimal_places + 1
    string = string[:index]
    return string



# Command Line Parsing #########################################################

def Validate_Read_Path(filepath):
    """
    Validates the filepath of the input file.
    Return 0 if the filepath is valid.
    Return 1 otherwise.
    
    Validate_Read_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
        return 0
    except:
        return 1



def Generate_Default_Output_Folder_Path(path_in):
    """
    Generate output folder path based on the provided input filepaths.

    Generate_Default_Output_Paths(str) -> str
    """
    index = Find_Period_Index(path_in)
    if index == -1: return path_in
    else: return path_in[:index]

def Find_Period_Index(filepath):
    """
    Return the index of a filepath's file extension string. (The index of the
    period.)
    
    Return -1 if the file name has no file extension.
    
    Find_Period_Index(str) -> int
    """
    # Find period
    index_period = filepath.rfind(".")
    if index_period == -1: return -1 # No period
    # Slash and backslash
    index_slash = filepath.rfind("/")
    index_bslash = filepath.rfind("\\")
    if index_slash == index_bslash == -1: return index_period # Simple path
    # Complex path
    right_most = max(index_slash, index_bslash)
    if right_most > index_period: return -1 # Period in folder name only
    return index_period

def Get_Extension(filepath):
    """
    Return the file extension for the file specified by [filepath].
    
    Return an empty string if the file has no extension.
    
    Assumes [filepath] is the filepath for a file. If a directory path is
    supplied, an empty string will also be returned.
    
    Get_Extension(str) -> str
    """
    index_period = Find_Period_Index(filepath)
    if index_period == -1: return ""
    return filepath[index_period+1:]


def Validate_Int_Positive(string):
    """
    Validates and returns the positive integer specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a positive integer.
        
    Validate_Column_Number(str) -> int
    """
    try:
        n = int(string)
    except:
        return -1
    if n < 1: return -1
    return n



def Strip_Non_Inputs(list1, name):
    """
    Remove the runtime environment variable and program name from the inputs.
    Assumes this module was called and the name of this module is in the list of
    command line inputs.

    @list1
        (list<str>)
        The raw inputs from the command line. (sys.argv)

    @name
        (str)
        The name of the main Python file. Ex. if the name of the program is:
            
            Test.py
        
        ..., and the program was called in Command Line using:
            
            C:\Python27\python.exe Test.py
        
        ..., then @name should be "Test" or "Test.py".
    
    Strip_Non_Inputs(list<str>) -> list<str>
    """
    if name in list1[0]: return list1[1:]
    return list1[2:]


