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
            [-o <output_folder>] [-w <file_width>] [-m <method> [m2]]



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
            [-o <output_folder>] [-w <file_width>] [-m <method> [*]]
"""

NAME = "Generate_Random_Chromosomes.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

FILEMOD__FASTA = ".fa"



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__width = 80
DEFAULT__method = 0 # METHOD.EQUAL = 0. If the METHOD enum is altered, sync this



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
from _Command_Line_Parser import *



# Enums ########################################################################

class METHOD:
    EQUAL=0 # If this is changed, sync DEFAULT__method variable
    GC=1



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Generate_Random_Chromosomes.py -h"



STR__read_file_invalid = "\nERROR: Chromosome names could not be derived from "\
        "chromosome sizes file."



STR__invalid_method = """
ERROR: Invalid nucleotide generation method: {s}
Please specify one of:
    EQUAL
    GC"""

STR__specify_GC_content = """
ERROR: Please specify the GC content you would like the resulting sequences to
have. Please specify either a number between 0 and 100 inclusive.
Numbers between 1 and 100 inclusive will be interpretted as a percentage.
Numbers less than 1 but greater than or equal to 0 will be interpretted as a
decimal fraction."""

STR__invalid_GC = """
ERROR: Invalid GC content: {s}
Please specify either a number between 0 and 100 inclusive.
Numbers between 1 and 100 inclusive will be interpretted as a percentage.
Numbers less than 1 but greater than or equal to 0 will be interpretted as a
decimal fraction."""



STR__metrics_N = "\nTotal N: {N}"
STR__metrics_A = "Total A: {N} ( {P}% )"
STR__metrics_C = "Total C: {N} ( {P}% )"
STR__metrics_G = "Total G: {N} ( {P}% )"
STR__metrics_T = "Total T: {N} ( {P}% )"

STR__GSC_begin = "\nRunning Generate_Random_Chromosomes..."

STR__GSC_complete = "\nGenerate_Random_Chromosomes successfully finished."



# Lists ########################################################################

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]

LIST__equal = ["E", "e", "EQUAL", "Equal", "equal"]
LIST__gc = ["GC", "gc"]

CUTOFFS__equal = [0.25, 0.5, 0.75] # A, C, G, T



# Dictionaries #################################################################

DICT__methods = {}
for i in LIST__equal: DICT__methods[i] = METHOD.EQUAL
for i in LIST__gc: DICT__methods[i] = METHOD.GC



# Apply Globals ################################################################

PRINT.PRINT_ERRORS = PRINT_ERRORS
PRINT.PRINT_PROGRESS = PRINT_PROGRESS
PRINT.PRINT_METRICS = PRINT_METRICS



# Functions ####################################################################

def Generate_Synthetic_Chromosomes(path_in, path_out, width, method,
        method_supplementary):
    """
    Generate a series of FASTA files each containing a synthetic chromosome.
    
    @path_in
            (str - filepath)
            The filepath of the chromosome sizes file used to determine the
            size of the resulting synthetic chromosomes. 
    @path_out
            (str - dirpath)
            The filepath for the folder where the resultant FASTA file(s) will 
            be created.
    @width
            (int)
            The maximum number of chars in each line of the FASTA file(s).
    @method
            (int) - Pseudo ENUM
            An int which signifies the way nucleotides are randomly generated:
                1: EQUAL
                    All nucleotides have an equal probability of occuring
                2: GC
                    Nucleotides are chosen in accordance with the desired GC
                    content, which is specified.
    @method_supplementary
            (*)
            Supplementary input (where necessary) for generating nucleotides.
            Type, structure, and significance varies depending on @method:

                1:
                    [float, float, float]
                    Cutoffs used against randomly generated numbers to
                    determine nucleotide assignment. See Generate_Cutoffs_GC()
                    for more details.
                2:
                    [float, float, float]
                    Cutoffs used against randomly generated numbers to
                    determine nucleotide assignment. See Generate_Cutoffs_GC()
                    for more details.
    
    Return a value of 0 if the function runs successfully.
    Return a value of 1 if there is a problem with the chromsome sizes file.
    
    Generate_Synthetic_Chromosomes(str, str, int, float, *) -> int
    """
    # Setup reporting
    outcomes = [] # Outcomes are added to the list after every chromosome

    # Main loop
    PRINT.printP(STR__GSC_begin)
    f = open(path_in, "U")
    line = f.readline().strip()
    if not line: # Empty chromosome sizes file
        f.close()
        return 1
    while line:
        # Parse
        values = Parse_TSV_Line(line)
        chr_file_name = path_out + "\\" + values[0] + FILEMOD__FASTA
        try: # Get chromosome size
            size = int(values[1])
        except: # Invalid chromosome size
            f.close()
            return 1
        # Generate chromosome
        if method in [METHOD.EQUAL, METHOD.GC]:
            outcome = Generate_Synthetic_Chromosome__CUTOFFS(values[0],
                    chr_file_name, size, width, method_supplementary)
            if not outcome:
                f.close()
                return 2
            outcomes.append(outcome)
        # Next line
        line = f.readline().strip()
    f.close()
    PRINT.printP(STR__GSC_complete)

    # Reporting
    if method in [METHOD.EQUAL, METHOD.GC]:
        Report_Metrics__CUTOFFS(outcomes)

    # Wrap up
    return 0

def Parse_TSV_Line(line):
    """
    Parse the raw output of a line from a TSV file.
    
    Parse_Line(str) -> list<str>
    """
    result = line.split("\t")
    if result[-1][-1] == "\n" or result[-1][-1] == "\r":
        result[-1] = result[-1][:-1]
    return result



def Generate_Synthetic_Chromosome__CUTOFFS(chr_name, path_out, chr_size, width, 
        cutoffs):
    """
    Generate a FASTA file containing a synthetic chromosome.
    
    @chr_name
            (str)
            The name of the chromosome.
    @path_out
            (str - filepath)
            The filepath for the file where the synthetic chromosome will be
            created.
    @chr_size
            (int)
            The size of the chromosome created, in basepairs.
    @width
            (int)
            The maximum number of chars in each line of the FASTA file(s).
    @cutoffs
            (list<float>)
            The cutoff list to be used for determining the likelihood of 
            different nucleotides occuring in the generated sequence.
            The list contains 3 floats. A random number generator generates a 
            number between 0 and 1. If the randomly generated number is less 
            than the first float, the resulting nucleotide is an Adenosine. If 
            the randomly generated number is greater than the first float but 
            less than or equal to the second, the resulting nucleotide is a 
            Cyotsine. If the randomly generated number is greater than the 
            second float but less than or equal to the third, the  resulting 
            nucleotide is a Guanine. If the randomly generated number is
            greater than the third float, the resulting nucleotide is a 
            Thymine.
    
    Return a list of A, C, G, and T counts.
    Return an empty list if an error occured.
    
    Generate_Synthetic_Chromosomes(str, str, int, int, [float, float, float]) 
    -> [int, int, int, int]
    """
    # Validate
    try:
        o = open(path_out, "w")
    except:
        return []
    # Name
    o.write(">" + chr_name + "\n")
    # Setup
    sb = ""
    total = 0
    char_count = 0
    counts = [0,0,0,0]
    # Loop
    while total < chr_size:
        n = Generate_Random_Nucleotide__CUTOFFS(cutoffs, counts)
        sb = sb + n
        total += 1
        char_count += 1
        if char_count == width:
            o.write(sb + "\n")
            sb = ""
            char_count = 0
    # Finish
    if char_count: o.write(sb + "\n")
    o.close()
    return counts



def Generate_Random_Nucleotide__CUTOFFS(cutoffs, counts=[0,0,0,0]):
    """
    Generate a random nucleotide using the cutoffs specified.
    Modify the list of counts to account for this nucleotide.

    @cutoffs
            [float, float, float]
            The cutoff list to be used for determining the likelihood of 
            different nucleotides occuring in the generated sequence.
            The list contains 3 floats. A random number generator generates a 
            number between 0 and 1. If the randomly generated number is less 
            than the first float, the resulting nucleotide is an Adenosine. If 
            the randomly generated number is greater than the first float but 
            less than or equal to the second, the resulting nucleotide is a 
            Cyotsine. If the randomly generated number is greater than the 
            second float but less than or equal to the third, the  resulting 
            nucleotide is a Guanine. If the randomly generated number is
            greater than the third float, the resulting nucleotide is a 
            Thymine.
    @counts
            [int,int,int,int]
            A count of the nucleotides generated so far. The original list is
            modified based on the nucleotide which was generated.
    
    Generate_Random_Nucleotide__CUTOFFS([float, float, float]) -> str
    """
    r = Random.random()
    if r < cutoffs[1]:
        if r < cutoffs[0]:
            counts[0] += 1
            return "A"
        else:
            counts[1] += 1
            return "C"
    else:
        if r < cutoffs[2]:
            counts[2] += 1
            return "G"
        else:
            counts[3] += 1
            return "T"



def Report_Metrics__CUTOFFS(outcomes):
    """
    Print a report into the command line interface of the total number of
    nucleotides generated, and their distribution.
    
    @outcomes
            (list<list<int>>)
            A list of sublists, each containing four integers. Each sublist
            corresponds to a chromosome, and each integer represents the number
            of Adenosines, Cytosines, Guanines, and Thymines, respectively.
    
    Report_Metrics__CUTOFFS([int,int,int,int]) -> None
    """
    # Setup
    A = 0
    C = 0
    G = 0
    T = 0
    # Sum
    for sublist in outcomes:
        A += sublist[0]
        C += sublist[1]
        G += sublist[2]
        T += sublist[3]
    N = A + C + G + T
    # Percentages
    Ap = (A * 100.0) / N
    Cp = (C * 100.0) / N
    Gp = (G * 100.0) / N
    Tp = (T * 100.0) / N
    # Strings
    str_N = str(N)
    str_A = str(A)
    str_C = str(C)
    str_G = str(G)
    str_T = str(T)
    str_Ap = str(Ap)
    str_Cp = str(Cp)
    str_Gp = str(Gp)
    str_Tp = str(Tp)
    # Padding and formatting
    max_size = len(str_N)
    str_A = Pad_Str(str_A, max_size, " ", 0)
    str_C = Pad_Str(str_C, max_size, " ", 0)
    str_G = Pad_Str(str_G, max_size, " ", 0)
    str_T = Pad_Str(str_T, max_size, " ", 0)
    str_Ap = Trim_Percentage_Str(str_Ap, 2)
    str_Cp = Trim_Percentage_Str(str_Cp, 2)
    str_Gp = Trim_Percentage_Str(str_Gp, 2)
    str_Tp = Trim_Percentage_Str(str_Tp, 2)
    max_size_p = max([len(str_Ap), len(str_Cp), len(str_Gp), len(str_Tp)])
    str_Ap = Pad_Str(str_Ap, max_size_p, " ", 0)
    str_Cp = Pad_Str(str_Cp, max_size_p, " ", 0)
    str_Gp = Pad_Str(str_Gp, max_size_p, " ", 0)
    str_Tp = Pad_Str(str_Tp, max_size_p, " ", 0)
    # Print
    PRINT.printM(STR__metrics_N.format(N = str_N))
    PRINT.printM(STR__metrics_A.format(N = str_A, P = str_Ap))
    PRINT.printM(STR__metrics_C.format(N = str_C, P = str_Cp))
    PRINT.printM(STR__metrics_G.format(N = str_G, P = str_Gp))
    PRINT.printM(STR__metrics_T.format(N = str_T, P = str_Tp))



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Generate_Synthetic_Genome(raw_command_line_input):
    """
    Parse the command line input and call the Generate_Synthetic_Genome function
    with appropriate arguments if the command line input is valid.
    """
    PRINT.printP(STR__parsing_args)
    # Remove the runtime environment variable and program name from the inputs
    inputs = Strip_Non_Inputs(raw_command_line_input, NAME)
    
    # No inputs
    if not inputs:
        PRINT.printE(STR__no_inputs)
        PRINT.printE(STR__use_help)
        return 1
    
    # Help option
    if inputs[0] in LIST__help:
        print(HELP_DOC)
        return 0
    
    # Initial validation (Redundant in current version)
    if len(inputs) < 1:
        PRINT.printE(STR__insufficient_inputs)
        PRINT.printE(STR__use_help)
        return 1
    
    # Validate mandatroy inputs
    path_in = inputs.pop(0)
    valid = Validate_Read_Path(path_in)
    if valid == 1:
        PRINT.printE(STR__IO_error_read.format(f = path_in))
        PRINT.printE(STR__use_help)
        return 1
    
    # Set up rest of the parsing
    width = DEFAULT__width
    method = DEFAULT__method
    method_supplementary = CUTOFFS__equal # A, C, G, T # The default
    path_out = Generate_Default_Output_Folder_Path(path_in)
    
    # Validate optional inputs (except output path)
    while inputs:
        arg = inputs.pop(0)
        try: # Second argument
            arg2 = inputs.pop(0)
        except:
            PRINT.printE(STR__insufficient_inputs)
            PRINT.printE(STR__use_help)
            return 1
        if arg == "-o": # Output files
            path_out = arg2
        elif arg == "-w": # File width
            width = Validate_Int_Positive(arg2)
            if width == -1:
                PRINT.printE(STR__invalid_width.format(s = arg2))
                return 1
        elif arg == "-m": # Method
            if arg2 in LIST__equal:
                cutoffs = CUTOFFS__equal
            elif arg2 in LIST__gc:
                try:
                    arg3 = inputs.pop(0)
                except:
                    PRINT.printE(STR__specify_GC_content)
                    return 1
                GC = Validate_GC_Content(arg3)
                if GC == -1:
                    PRINT.printE(STR__invalid_GC.format(s = arg3))
                    return 1
                method_supplementary = Generate_Cutoffs_GC(GC)
                
            else:
                PRINT.printE(STR__invalid_method)
                PRINT.printE(STR__use_help)
                return 1
        else: # Invalid
            arg = Strip_X(arg)
            PRINT.printE(STR__invalid_argument.format(s = arg))
            PRINT.printE(STR__use_help)
            return 1

    # Validate output path
    valid_out = Validate_Folder_Path(path_out, path_in)
    if valid_out == 0: pass
    elif valid_out == 1: PRINT.printM(STR__overwrite_accept)
    else:
        if valid_out == 2: PRINT.printE(STR__IO_error_write_folder_cannot)
        elif valid_out == 3: PRINT.printE(STR__overwrite_decline)
        elif valid_out == 4: PRINT.printE(STR__IO_error_write_folder_forbid)
        elif valid_out == 5:
            PRINT.printE(STR__IO_error_write_folder_nonexistent)
        elif valid_out == 6: PRINT.printE(STR__read_file_invalid)
        elif valid_out == 7: PRINT.printE(STR__IO_error_write_unexpected)
        return 1
    
    # Run program
    exit_state = Generate_Synthetic_Chromosomes(path_in, path_out, width,
            method, method_supplementary)
    
    # Exit
    if exit_state == 0: return 0
    else:
        if exit_state == 1: PRINT.printE(STR__read_file_invalid)
        PRINT.printE(STR__use_help)
        return 1



def Validate_Folder_Path(folder_path, chr_sizes_filepath):
    """
    Validates the writepath of the output folder.
    Attempts to create the folder if it does not exist.

    Assumes that @chr_sizes_filepath is a valid filepath.
    
    Return 0 if the folder path is valid and empty* and can be written into.
    Return 1 if the folder path is valid and the user decides to overwrite
            existing files.
    Return 2 if the folder path is valid and empty but cannot be written into.
    Return 3 if the folder path is valid and the user declines to overwrite
            existing files.
    Return 4 if the folder path is valid, but contains existing files and the
            program is set to forbid overwriting.
    Return 5 is the folder path does not exist and cannot be created.
    Return 6 if there is a problem with the chromsome sizes file.
    Return 7 for unexpected errors.

    * Empty - Not necessarily empty, but does not containing any naming
            conflicts with the names in the chromosome sizes file.
    
    Validate_Folder_Path(str, str) -> int
    """
    # Create folder if it does not exist
    if not os.path.isdir(folder_path):
        try:
            os.mkdir(folder_path)
        except:
            return 5
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
    try:
        f.close()
        os.remove(random_path)
    except:
        return 7
    # OVERWRITE TESTING
    FLAG_exists = 0
    f = open(chr_sizes_filepath, "U")
    line = f.readline()
    while line:
        values = line.split("\t")
        temp_path = folder_path + "\\" + values[0] + FILEMOD__FASTA
        # See if file already exists
        try:
            exist = os.path.exists(temp_path)
        except:
            return 6
        # If file already exists
        if exist:
            FLAG_exists = 1
        line = f.readline()
    f.close()
    # Return
    if FLAG_exists:
        if WRITE_PREVENT: return 4
        if WRITE_CONFIRM:
            confirm = raw_input(STR__overwrite_confirm.format(f=folder_path))
            if confirm not in LIST__yes: return 3        
        return 1
    return 0



def Validate_GC_Content(string):
    """
    Validates and returns the GC content percentage/fraction as a decimal.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting either a percentage between 1 and 100, or a decimal
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

def Generate_Cutoffs_GC(gc_content):
    """
    Return a cutoff list to be used for determining the likelihood of different
    nucleotides occuring in the generated sequence.
    The list contains 3 floats. A random number generator generates a number
    between 0 and 1. If the randomly generated number is less than the first
    float, the resulting nucleotide is an Adenosine. If the randomly generated
    number is greater than the first float but less than or equal to the second,
    the resulting nucleotide is a Cyotsine. If the randomly generated number is
    greater than the second float but less than or equal to the third, the 
    resulting nucleotide is a Guanine. If the randomly generated number is
    greater than the third float, the resulting nucleotide is a Thymine.

    Return an empty list if an invalid fraction is supplied.
    
    @gc_content
        (float)
        The fraction of the sequence which is Cytosine or Guanine.
        (Ex. 0.55 means the sequence should have a GC content of 55%)
        
    Generate_Cutoffs_GC(float) -> [float, float, float]
    """
    if type(gc_content) != float: return []
    # Pyrimidines
    pyr_content = gc_content/2
    # Purines
    at_content = 1 - gc_content
    pur_content = at_content/2
    # Calculate cutoffs
    cutoff_a = pur_content
    cutoff_c = pur_content + pyr_content
    cutoff_g = pur_content + gc_content
    # Check and return
    if cutoff_g >= 1: return []
    return [cutoff_a, cutoff_c, cutoff_g]



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Generate_Synthetic_Genome(sys.argv)
