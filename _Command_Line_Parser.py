"""
COMMAND LINE PARSER
(version 1.3)
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

STR__IO_error_read_folder = "\nERROR: Input folder does not exist or could not"\
        " be read."

STR__read_folder_no_substring = "\nERROR: Input folder:\n\t{f}\n...contains "\
        "no files containing the substring:\n\t{s}"

STR__IO_error_write_forbid = """
ERROR: You specified an output file which already exists and the administrator
for this program has forbidden all overwrites. Please specify a different
output file, move the currently existing file, or configure the underlying
File Writer module."""
STR__IO_error_write_unable = """
ERROR: Unable to write to the specified output file."""

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
options in program."""
STR__IO_error_write_unexpected = """
ERROR: An unexpected error occured with the specified output path. Contact the
developers because this error should never be triggered from normal usage of
this software."""

STR__overwrite_confirm = "\nFile already exists:\n\t{f}\nDo you wish to "\
        "overwrite it? (y/n): "

STR__overwrite_accept = "\nWARNING: Existing files will be overwritten."
STR__overwrite_decline = "\nThe user has opted not to overwrite existing "\
        "files.\nThe program will now terminate."

STR__invalid_width = """
ERROR: Invalid width: {s}
Please specify a positive integer.
"""

STR__invalid_bool = """
ERROR: Invalid boolean: {s}
Please specify one of the following:
    Yes
    No
    True
    False"""

STR__invalid_arg_for_flag = "\nERROR: Invalid argument supplied for the flag "\
"\"{s}\"" 



STR__invalid_table_type = "\nERROR: Invalid table type specified:\n\t{s}"



STR__invalid_argument = "\nERROR: Invalid argument: {s}"

STR__parsing_args = "\nParsing arguments..."



# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"]

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]

LIST__all = ["A", "a", "ALL", "All", "all"]

LIST__FASTA = ["FA", "fa", "FASTA", "Fasta", "fasta"] # File extensions
LIST__VCF = ["VCF", "Vcf", "vcf"]
LIST__CSV = ["CSV", "Csv", "csv"]
LIST__TSV = ["TSV", "Tsv", "tsv"]
LIST__TSV_ = ["TSV", "Tsv", "tsv", "TAB", "Tab", "tab"]
LIST__SSV = ["SSV", "Ssv", "ssb"]



# Dictionaries #################################################################

DICT__table_ext_to_delim = {}
DICT__table_ext_to_delim_ = {}

for ext in LIST__CSV: DICT__table_ext_to_delim[ext] = ","
for ext in LIST__TSV: DICT__table_ext_to_delim[ext] = "\t"
for ext in LIST__SSV: DICT__table_ext_to_delim[ext] = " "

DICT__table_ext_to_delim_ = dict(DICT__table_ext_to_delim)
for ext in LIST__TSV: DICT__table_ext_to_delim_[ext] = "\t"



# Communications and Metrics ###################################################

def Get_Max_Len(strings):
    """
    Return the length of the longest string in a list of strings.
    
    @strings
            (list<str>)
            The list of the strings.
    
    Get_Max_Len(list<str>) -> int
    """
    maximum = 0
    for string in strings:
        length = len(string)
        if length > maximum: maximum = length
    return maximum



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

def Validate_Read_Folder(dirpath):
    """
    Validates the dirpath of the folder.
    Return 0 if the filepath is valid.
    Return 1 otherwise.
    
    Validate_Read_Path(str) -> int
    """
    try:
        os.listdir(dirpath)
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
    
def Generate_Default_Output_File_Path_From_File(path_in, mod,
            keep_extension=False):
    """
    Generate output filepath based on the provided input filepath. The original
    file extension can be retained or discarded depending on the users'
    preference.
    
    Assumes [path_in] is a valid filepath.

    Generate_Default_Output_File_Path_From_File(str, str, bool) -> str
    """
    index = Find_Period_Index(path_in)
    if index == -1: return path_in + mod
    if keep_extension: return path_in[:index] + mod + path_in[index:]
    return path_in[:index] + mod
    
def Generate_Default_Output_File_Path_From_Folder(path_in, mod):
    """
    Generate output filepath based on the provided input dirpaths.
    
    Assumes [path_in] is a valid dirpath.

    Generate_Default_Output_File_Path_From_Folder(str, str) -> str
    """
    return path_in + mod

def Get_File_Name_Ext(filepath):
    """
    Return the name of the file, and the file extension, for the file specified
    by [filepath].
    
    If the file has no extension, return the file name and an empty string.
    
    Assumes [filepath] is the filepath for a file. If a directory path is
    supplied, an empty string will also be returned.
    
    Get_Name(str) -> [str, str]
    """
    # Slash and backslash
    index_slash = filepath.rfind("/")
    index_bslash = filepath.rfind("\\")
    if index_slash == index_bslash == -1: pass # Simple path
    else: # Complex path
        right_most = max(index_slash, index_bslash)
        filepath = filepath[right_most+1:]
    # Find period
    index_period = filepath.rfind(".")
    if index_period == -1: return [filepath, ""]
    return [filepath[:index_period], filepath[index_period+1:]]

def Get_File_Name(filepath):
    """
    Return the name of the file, minus the file extension, for the file
    specified by [filepath].
    
    Assumes [filepath] is the filepath for a file. If a directory path is
    supplied, an empty string will also be returned.
    
    Get_Name(str) -> str
    """
    # Slash and backslash
    index_slash = filepath.rfind("/")
    index_bslash = filepath.rfind("\\")
    if index_slash == index_bslash == -1: pass # Simple path
    else: # Complex path
        right_most = max(index_slash, index_bslash)
        filepath = filepath[right_most+1:]
    # Find period
    index_period = filepath.rfind(".")
    if index_period == -1: return filepath
    return filepath[:index_period]

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

def Get_Files_W_Extensions(dirpath, extensions):
    """
    Return a list of the full filepaths of every file in [dirpath] which have
    a file extension in [extensions].
    Return an empty list if there are any issues.
    
    @path_in
            (str - dirpath)
            The filepath of the folder of interest.
    @extensions
            (list<str>)
            A list of all acceptable file extensions.
    
    Get_Files_W_Extensions(str, list<str>) -> list<str>
    """
    results = []
    try:
        files = os.listdir(dirpath)
    except:
        return results
    for file_ in files:
        extension = Get_Extension(file_)
        if extension in extensions:
            full_path = dirpath + "/" + file_
            results.append(full_path)
    return results

def Get_Files_W_Substring(dirpath, substring):
    """
    Return a list of the full filepaths of every file in [dirpath] with names
    which contain [substring].
    Return None if there are any issues.
    
    @path_in
            (str - dirpath)
            The filepath of the folder of interest.
    @substring
            (str)
            The target substring
    
    Get_Files_W_Extensions(str, str) -> list<str>
    """
    results = []
    try:
        files = os.listdir(dirpath)
    except:
        return None
    for file_ in files:
        if substring in file_:
            full_path = dirpath + "/" + file_
            results.append(full_path)
    return results



def Validate_Bool(string):
    """
    Validates and returns the boolean specified. Accepts variants of Yes, No,
    True, and False.
    Return a boolean if the string is valid.
    Return None if the string is invalid.
    
    @string
        (str)
        A string denoting a boolean. (Includes Yes/No)
    
    Validate_Bool(str) -> bool
    Validate_Bool(str) -> None
    """
    if string in LIST__yes: return True
    elif string in LIST__no: return False
    else: return None



def Validate_Number(string):
    """
    Validates and returns the number specified.
    Return an integer if possible.
    Return a float if a non-integer number is specified.
    Return None if the input is invalid.
    
    @string
        (str)
        A string denoting a number.
        
    Validate_Number(str) -> int
    Validate_Number(str) -> float
    Validate_Number(str) -> None
    """
    try:
        n = int(string)
    except:
        try:
            n = float(string)
        except:
            return None
    return n

def Validate_Int_Positive(string):
    """
    Validates and returns the positive integer specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a positive integer.
        
    Validate_Int_Positive(str) -> int
    """
    try:
        n = int(string)
    except:
        return -1
    if n < 1: return -1
    return n

def Validate_Int_NonNeg(string):
    """
    Validates and returns the non-negative integer specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a non-negative integer.
        
    Validate_Int_NonNeg(str) -> int
    """
    try:
        n = int(string)
    except:
        return -1
    if n < 0: return -1
    return n

def Validate_Float_Positive(string):
    """
    Validates and returns the positive float specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a positive float.
        
    Validate_Float_Positive(str) -> float
    """
    try:
        n = float(string)
    except:
        return -1
    if n <= 0: return -1
    return n

def Validate_Float_NonNeg(string):
    """
    Validates and returns the non-negative float specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a non-negative float.
        
    Validate_Float_NonNeg(str) -> float
    """
    try:
        n = float(string)
    except:
        return -1
    if n < 0: return -1
    return n

def Validate_Float_NonZero(string):
    """
    Validates and returns the non-zero float specified.
    Return 0 if the input is invalid.
    
    @string
        (str)
        A string denoting a non-zero float.
        
    Validate_Float_NonZero(str) -> float
    """
    try:
        n = float(string)
    except:
        return 0
    if n == 0: return 0
    return n

def Validate_Table_Type(string):
    """
    Validates a table file type and returns the delimiter char for that table
    type.
    Return an empty string if the input is invalid.
    
    @string
        (str)
        A string denoting the file type. Acceptable options are:
            tsv - Tab-separated values
            csv - Comma-separated values
            ssv - Space-separated values
        
    Validate_Table_Type(str) -> str
    """
    return DICT__table_ext_to_delim_.get(string, "")



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



def Strip_X(string):
    """
    Strips leading and trailing inverted commans or brackets if a matching pair
    are flanking the string.
    
    Strip_X(str) -> str
    """
    if (    (string[0] == string[-1] == "\"") or
            (string[0] == string[-1] == "\'") or
            (string[0] == "(" and string[-1] == ")") or
            (string[0] == "{" and string[-1] == "}") or
            (string[0] == "[" and string[-1] == "]") or
            (string[0] == "<" and string[-1] == ">")
            ):
        return string[1:-1]
    return string


