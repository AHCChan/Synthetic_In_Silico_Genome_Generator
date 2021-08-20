HELP_DOC = """
RANDOM CHROMOSOME GENERATOR
(version 1.0)
by Angelo Chan

This is a program for generating random DNA sequences with the names and sizes
specified by the Chromosome Sizes file. The resulting chromosomes will be
output into separate FASTA files in the FASTA format.

These sequences are intended as the basis for synthetic chromosomes, which,
combined, form a synthetic genome.

The resultant FASTA files are output into the output folder, which can either be
specified by the user, or automatically generated.



USAGE:
    
    python27 Generate_Random_Chromosomes.py <chr_sizes_file>
            [-o <output_folder] [-w <file_width] [-m <method> [m2]]



MANDATORY:
    
    chr_sizes_file
        
        The filepath of the chromosome sizes file. The chromosome sizes file
        is a TSV (Tab-Separated Values) file with two columns. The first
        column contains the name of the chromosome, while the second contains
        the size )in basepairs) of said chromosome.

OPTIONAL:
    
    output_folder
        
        (DEFAULT path generation available)
        
        The filepath of the output folder where resultant FASTA files will be
        output into.
    
    file_width
        
        (DEFAULT: 80)
        
        The "width" of the output files, also known as the maximum number of
        characters allowed in each line of the output file(s).
    
    method
        
        (DEFAULT: EQUAL)
        
        The method used to generate the random nucleotide sequences. Valid
        methods are:
            
            EQUAL
                All four nucleotides have an equally likely chance of occuring
                at any given position.
            
            GC
                The desired GC content of the resultant sequences.
    
    m2
        
        Additional parameters specifying the method used to generate the random
        nucleotide sequences. Depends on @method:
            
            EQUAL
                No extra parameters are required. 
            
            GC
                A float, denoting either the percentage of nucleotides which
                are GC, or a decimal number denoting the fraction of nucleotides
                which are GC.

EXAMPLES:
    
    python27 Generate_Random_Chromosomes.py data\chr_sizes.tsv
            -o data\test_genome
    
    python27 Generate_Random_Chromosomes.py data\chr_sizes.tsv
            -o data\test_genome -m EQUAL
    
    python27 Generate_Random_Chromosomes.py data\chr_sizes.tsv
            -o data\test_genome -w 40 -m GC 55

USAGE:
    
    python27 Generate_Random_Chromosomes.py <chr_sizes_file>
            [-o <output_folder] [-w <file_width] [-m <method> [*]]
"""

NAME = "Generate_Random_Chromosomes.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__width = 80
DEFAULT__method = 0 # METHOD.EQUAL = 0. If the METHOD enum is altered, sync this

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Imported Modules #############################################################

import random as Random

import os



# Enums ########################################################################

class METHOD:
    EQUAL=0 # If this is changed, sync DEFAULT__method variable
    GC=1



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Generate_Random_Chromosomes.py -h"

STR__no_inputs = "\nERROR: No inputs were given."

STR__IO_error_read = "\nERROR: Input file does not exist or could not be "\
        "opened."
STR__IO_error_write_invalid = """
ERROR: You specified an output folder which does not exist and cannot be
created. Please specify a different output folder."""
STR__IO_error_write_forbid = """
ERROR: You specified an output folder which cannot be written into. Please
specify a different output folder."""
STR__IO_error_write_unexpected = """
ERROR: An unexpected error occured with the specified output path. Contact the
developers because this error should never be triggered from normal usage of
this software."""

STR__invalid_width = """
ERROR: Invalid width: {s}
Please specify a positive integer.
"""

STR__invalid_method = """
ERROR: Invalid nucleotide generation method: {s}
Please specify one of:
    EQUAL
    GC"""


STR__metrics_N = "\nTotal_N: {N}"
STR__metrics_A = "Total_A:  {N} ( {P}% )"
STR__metrics_C = "Total_C:  {N} ( {P}% )"
STR__metrics_G = "Total_G:  {N} ( {P}% )"
STR__metrics_T = "Total_T:  {N} ( {P}% )"

STR__parsing_args = "\nParsing arguments..."

STR__GPC_begin = "\nRunning Generate_Random_Chromosomes..."

STR__GPC_complete = "\nGenerate_Random_Chromosomes successfully finished."



# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"]

LIST__equal = ["E", "e", "EQUAL", "Equal", "equal"]
LIST__gc = ["GC", "gc"]



# Dictionaries #################################################################

DICT__methods = {}
for i in LIST__equal: DICT__methods[i] = METHOD.EQUAL
for i in LIST__gcl: DICT__methods[i] = METHOD.GC



# Functions ####################################################################



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Generate_Synthetic_Genome():
    """
    Parse the command line input and call the Generate_Synthetic_Genome function
    with appropriate arguments if the command line input is valid.
    """
    printP(STR__parsing_args)
    # Remove the runtime environment variable and program name from the inputs
    inputs = Strip_Non_Inputs(raw_command_line_input)
    
    # Safe exit
    return 0



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



def Validate_Write_Path(folder_path):
    """
    Validates the writepath of the output folder.
    Attempts to create the folder if it does not exist.
    
    Return 0 if the folder path is valid.
    Return 1 if the folder path does not exist and cannot be created.
    Return 2 if the folder path is valid, but cannot be written into.
    Return 3 for unexpected errors.
    
    Validate_Write_Path(str) -> int
    """
    # Create folder if it does not exist
    if not os.path.isdir(folder_path):
        try:
            os.mkdir(folder_path)
        except:
            return 1
    # Create a random file for testing purposes
    random_name = str(Random.random())
    random_path = folder_path + "\\" + random_name
    while os.path.exists(random_path):
        random_name = str(Random.random())
        random_path = folder_path + "\\" + random_name
    # Attempt to write to the folder
    try:
        f = open(random_path, "w")
    except:
        return 2
    # Unexpected errors
    f.close()
    os.remove(random_path)
    return 3



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



def Validate_GC_Content(string):
    """
    Validates and returns the GC content percentage/fraction as a decimal.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denotingeither a percentage between 1 and 100, or a decimal
        number between 0 and 1.
        If the user wishes to specify a percentage of less than 1%, they will
        need to convert it into its decimal equivalent.
        
    Validate_Column_Number(str) -> float
    """
    try:
        n = float(string)
    except:
        return -1
    if n > 100: return -1
    if n > 1: return n/100
    if n < 0: return -1
    return n



def Strip_Non_Inputs(list1):
    """
    Remove the runtime environment variable and program name from the inputs.
    Assumes this module was called and the name of this module is in the list of
    command line inputs.
    
    Strip_Non_Inputs(list<str>) -> list<str>
    """
    if NAME in list1[0]: return list1[1:]
    return list1[2:]



# Controlled Print Statements ##################################################

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



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Generate_Synthetic_Genome(sys.argv)
