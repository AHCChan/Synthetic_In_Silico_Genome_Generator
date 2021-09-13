HELP_DOC = """
READ GENERATOR
(version 1.0)
by Angelo Chan

This is a program for generating DNA sequencing read data from DNA sequences.

It is designed to be paired up the Fragment Generator from this (Synthetic
In-Silico Genome Generator) library, which imitates the DNA fragmentation
process, and mimicks the NGS DNA sequencing process.



USAGE:
    
    python27 Generate_Reads.py <input_filepath> [-o <output_filepath_r1>
            <output_filepath_r2>] [-r <read_1_len> <read_2_len>] [-p <phred>]
            [-q <avg_quality> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-d
            <avg_duplicates> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-m
            <min_duplicates> <max_duplicates>] [-t <avg_truncation> N|G|U
            <stdev>|<alpha_mod>|<max_dist>]



MANDATORY:
    
    input_folder
        
        The filepath of the input folder containing the FASTA file from which
        the DNA reads will be generated.

OPTIONAL:
    
    output_filepath_r1
        
        (DEFAULT path generation available)
        
        The filepath of the output file where resultant forward reads will be
        output into.
    
    output_filepath_r1
        
        (DEFAULT path generation available)
        
        The filepath of the output file where resultant reverse reads will be
        output into.
    
    read_1_len
        
        (DEFAULT: 75)
        
        The read length of the forward reads. i.e. The first @read_1_len
        nucleotides of the fragment will be output into a read.
    
    read_2_len
        
        (DEFAULT: 75)
        
        The read length of the reverse reads. i.e. The complement of the last
        @read_2_len nucleotides of the fragment will be output into a read.
        
        Set to 0 for Single-End sequencing.
    
    phred
        
        (DEFAULT: phred33)
        
        The phred system for denoting the quality scores of each nucleotide.
    
    phred
        
        (DEFAULT: phred33)
        
        The phred system for denoting the quality scores of each nucleotide.
    
    avg_quality
        
        (DEFAULT: 0)
        
        The average quality score (phred score), for the resulting reads. The
        lower the score, the higher the error rate when transcribing fragments
        to reads.
        Specifying 0 will give perfect reads.
    
    avg_duplicates
        
        (DEFAULT: 1)
        The average number of duplicate reads or read pairs per fragment.
    
    min_duplicates
        
        (DEFAULT: 1)
        The minimum number of duplicate reads or read pairs per fragment.
    
    max_duplicates
        
        (DEFAULT: 1)
        The maximum number of duplicate reads or read pairs per fragment.
    
    avg_truncation
        
        (DEFAULT: 0)
        The average number of nucleotides truncated off the ends of the reads.
    
    N|G|U
        
        (DEFAULT (-q): N)
        (DEFAULT (-d): G)
        (DEFAULT (-t): U)
        
        The probability distribution used to determine random values for things
        like phred scores, duplicate copy number and truncation length.
            
            N   Normal variate distribution
            G   Gama variate distribution
            U   Uniform distribution
    
    stdev
        
        (Only applies if a Normal Variate distribution was specified)
        (DEFAULT (-q): 5)
        
        The standard deviation of the normal distribution.
    
    alpha_mod
        
        (Only applies if a Gamma Variate distribution was specified)
        (DEFAULT (-d): 1)
        
        The skewness factor of the Gamma distribution.
        
        The magnitude of @alpha_mod determines how unskewed the distribution is.
        As @alpha_mod approaches infinity, the resulting gamma distribution will
        begin to resemble a normal distribution. As @alpha approaches 0, the
        resulting gamma distribution will become increasingly skewed.
        
        It is known that, for a Gamma Distribution:
            
            Alpha * Beta ~= Desired_Average
        
        The Beta is automatically calculated such that:
            
            Alpha = Beta * Alpha_Mod
        
    max_dist
        
        (Only applies if a Uniform distribution was specified)
        (DEFAULT (-t): 0)
        
        The furthest away from the specified average which a randomly generated
        value can be.

CONTEXTUAL FLAGS:
(For specifying probability distribution parameters)
    
    (-q)
        
        Used to signify that the following parameters pertain to the probability
        distribution of quality scores.
    
    (-d)
        
        Used to signify that the following parameters pertain to the probability
        distribution of duplicate copy numbers.
    
    (-t)
        
        Used to signify that the following parameters pertain to the probability
        distribution of truncation length.



EXAMPLES SCENARIO EXPLANATION:
    
    1:
    An almost bare minimum use case. (Specifying the output path is not
    mandatory, but it is good practice to do so.)

EXAMPLES:
    
    python27 Generate_Reads.py Path/Input_Frags.fa -o Output_Reads.fq

USAGE:
    
    python27 Generate_Reads.py <input_filepath> [-o <output_filepath_r1>
            <output_filepath_r2>] [-r <read_1_len> <read_2_len>] [-p <phred>]
            [-q <avg_quality> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-d
            <avg_duplicates> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-m
            <min_duplicates> <max_duplicates>] [-t <avg_truncation> N|G|U
            <stdev>|<alpha_mod>|<max_dist>]
"""

NAME = "Generate_Reads.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

FILEMOD__FASTQ = "__READS.fq"

# For name string
COPY_DIGITS = 3
STR__forward = "r1"
STR__reverse = "r2"

PRINT_INTERVAL = 10000



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"
    
DEFAULT__read_1_len = 75
DEFAULT__read_2_len = 75

DEFAULT__phred = "phred33"

DEFAULT__avg_quality = 20
DEFAULT__quality_dist = 1 # DIST.NORMAL = 1. Alter if the DIST enum is altered
DEFAULT__quality_param = 5

DEFAULT__avg_dupes = 1
DEFAULT__dupes_dist = 2 # DIST.GAMMA = 2. Alter if the DIST enum is altered
DEFAULT__dupes_param = 5
DEFAULT__min_dupes = 1
DEFAULT__max_dupes = 1

DEFAULT__avg_trunc = 0
DEFAULT__trunc_dist = 3 # DIST.UNIFORM = 3. Alter if the DIST enum is altered
DEFAULT__trunc_param = 0



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
from _Command_Line_Parser import *

from NSeq_Match import *
from Phred import *

from FASTA_File_Reader import *



# Enums ########################################################################

class DIST: # For Distribution
    NORMAL=1 # If this is changed, sync relevant defaults
    GAMMA=2
    UNIFORM=3



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Generate_Reads.py -h"



STR__invalid_dist = """
ERROR: Invalid statistical distribution: {s}
Please specify one of:
    NORMAL
    GAMMA
    UNIFORM"""

STR__invalid_dist_params = """
ERROR: Invalid {S} parameters:
    (Distribution): {D}
    (Parameter):    {P}

For the distribution model, please specify one of:
    NORMAL
    GAMMA
    UNIFORM

For the parameter, depending on the distribution model chosen, please specify:
    NORMAL - A non-negative number.
    GAMMA - A non-zero number.
    UNIFORM - A non-negative integer."""



STR__input_invalid = "\nERROR: An unexpected error occured when reading from "\
        "the input file."
STR__output_invalid = "\nERROR: An unexpected error occured when writing to "\
        "the output file."
STR__generation_invalid = "\nERROR: An unexpected error occured during the "\
        "fragment generation process."



STR__metrics = """
    Total reads/pairs generated: {C}

    Average forward read length: {F}
    Average reverse read length: {R}

          Average quality score: {Q}
        Average duplicate count: {D}
"""

STR__GenReads_begin = "\nRunning Generate_Reads..."

STR__GenReads_complete = "\nGenerate_Reads successfully finished."



# String Lists #################################################################

STR_LIST__specify_dist_param = [ # Indexes are based on the DIST enum
"""
ERROR: Please specify the standard deviation you want your normal distribution
to have. The standard deviations must be a positive number.""","""
ERROR: Please specify the alpha you want your gamma distribution to have. If the
alpha ius negative, a flipped and shifted gamma distribution will be applied
instead of a normal gamma distribution.""","""
ERROR: Please specify the maximum distance from the average you want your
uniformly distributed values to have. The maximum distance must be a
non-negative number."""]



# Lists ########################################################################

LIST__normal = ["N", "n", "NORMAL", "Normal", "normal", "NORM", "Norm", "norm"]
LIST__gamma = ["G", "g", "GAMMA", "Gamma", "gamma"]
LIST__uniform = ["U", "u", "UNIFORM", "Uniform", "uniform", "UNI", "Uni", "uni"]



# Dictionaries #################################################################

DICT__dists = {}
for i in LIST__normal: DICT__dists[i] = DIST.NORMAL
for i in LIST__gamma: DICT__dists[i] = DIST.GAMMA
for i in LIST__uniform: DICT__dists[i] = DIST.UNIFORM



# Apply Globals ################################################################

PRINT.PRINT_ERRORS = PRINT_ERRORS
PRINT.PRINT_PROGRESS = PRINT_PROGRESS
PRINT.PRINT_METRICS = PRINT_METRICS



# Functions ####################################################################

def Generate_Reads(path_in, path_out, read_lengths, quality_params,
            duplicate_params, duplicate_minmax, truncation_params):
    """
    """
    return



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Generate_Reads(raw_command_line_input):
    """
    Parse the command line input and call the Generate_Reads function
    with appropriate arguments if the command line input is valid.
    """
    return



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Generate_Reads(sys.argv)


