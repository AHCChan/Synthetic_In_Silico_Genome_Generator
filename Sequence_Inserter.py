HELP_DOC = """
SEQUENCE INSERTER
(version 1.0)
by Angelo Chan

The counterpart to the Sequence Extractor program.

This is a program for inserting sequences into a genomic template, such as
inserting genetic elements from a genome.

Inserted sequences do not have to originate from the genomic template or its
precursor.



USAGE:
    
    python27 Sequence_Inserter.py <genome_folder> <coordinates_table>
            <sequences_folder> [-o <output_folder> <output_coordinates_table>
            <output_chr_sizes_file>] [-a <window_min> <window_max>
            <errors_max> Y|N] [-m Y|N]



MANDATORY:
    
    genome_folder
        
        The filepath of the input folder containing the template FASTA file(s).
        Each FASTA file is assumed to only contain one DNA sequence per file,
        similar to chromosomal FASTA files.
    
    coordinates_table
        
        The filepath of the input file containing the coordinates for sequences
        to be inserted, as well as how to obtain the sequence. The first six
        columns need to contain the genomic coordinates:
            
            1) Chromosome name
            2) Start
            3) End
            4) Directionality* (+/-)
            5) ID/Name (Unneeded)
            6) How to obtain the genetic sequence:
                
                Raw genetic sequences can either be specified by "FILE:" or
                "SEQ:". "FILE:" means to lift a sequence from the following
                FASTA file, while "SEQ:" means to use the following text as the
                sequence.
                
                "INV:" means to invert the following sequence.
                
                "+" means to join/concatenate two sequences together.
                
                "~+" means to overlap-join/overlap-concatenate two sequences
                together. The last X nucleotides of the first sequence and the
                last X nucleotides of the last sequence which align will "merge"
                and only appear once. X needs to be, at minimum, 4 or higher.
                Ex. "SEQ:NNNNNAACC~+SEQ:AACCNNNNN" will result in
                "NNNNNAACCNNNNN" instead of "NNNNNAACCAACCNNNNN".
                
                "*X" means to diplicate a sequence X times.
                
                "~*X" means to overlap-duplicate a sequence X times. The last X
                nucleotides of the sequence and the first X nucleotides which
                align will "merge" and only appear once. X needs to be, at
                minimum, 4 or higher.
                Ex. "SEQ:AACCNNNNNAACC~*3" will result in
                "AACCNNNNNAACCNNNNNAACCNNNNNAACC" instead of
                "AACCNNNNNAACCAACCNNNNNAACCAACCNNNNNAACC".
                
                Standard string slicing:
                "[X:Y]" means to remove all nucleotides before index X, not
                inclusive, and after index Y, inclusive. If no number is
                provided before the colon, all nucleotides up to index Y, not
                inclusive, will be kept. If no number is provided after the
                colon, all nucleotides after index X, inclusive, will be kept.
                The first position is index 0. Negative numbers can be used to
                indicate the index when counting backwards from the end. (-1
                means the last index, -2 means the second last index, etc.)
                
                Truncation slicing:
                "![X:Y]" means to remove all nucleotides after index X,
                inclusive, and before index Y, not inclusive. The first position
                is index 0. Negative numbers can be used to indicate the index
                when counting backwards from the end. (-1 means the last index,
                -2 means the second last index, etc.)
                
                "(" and ")"
                Curved brackets may be used to indicate order of operations.
        
        The genomic coordinates apply to the pre-insertion template, and insert
        at the nucleotide specified in the start column, not after. (So
        inserting a sequence into position 1 will insert at the very start of
        the chromosome, effectively displacing ALL nucleotides.)
    
    sequence_folder
        
        The filepath of the input folder containing the FASTA file(s) containing
        the sequences to be inserted.  Each FASTA file is assumed to only
        contain one DNA sequence per file, similar to chromosomal FASTA files.

OPTIONAL:
    
    output_folder
        
        (DEFAULT path generation available)
        
        The filepath of the output folder where resultant post-insertion genomic
        templates will be outputted to.
    
    output_coordinates_table
        
        (DEFAULT path generation available)
        
        The filepath of the output Coordinates Table file. This file will
        contain the information of a genetic element in each row, with its new
        genomic coordinates in the first four columns, its ID in the fifth
        column, any additional input information in the seventh and up columns,
        while the sixth column will contain all the information necessary for
        determining its genomic sequence, including which original excised
        sequence is being used as the template, as well as any modifications
        which were subsequently made to said template.
    
    output_chr_sizes_file
        
        (DEFAULT path generation available)
        
        The filepath of the output chromosome sizes file, which lists all the
        chromosomes and their post-insertion sizes.
    
    window_min
        
        (DEFAULT: 4)
        
        The minimum window size allowed for overlap-joins and
        overlap-duplicates.

    window_max
        
        (DEFAULT: 100)
        
        The maximum window size allowed for overlap-joins and
        overlap-duplicates.

    errors_max
        
        (DEFAULT: 0)
        
        The maximum number of mismatches permitted for two sequences to qualify
        for an overlap-join or an overlap-duplicate.

    Y|N
        (-a)
        
        (DEFAULT: Y)
        
        Whether or not the largest qualifying window size will be used for
        overlap-joins and overlap-duplicates. If set to "N", the smallest
        qualifying window will be used instead.

    Y|N
        (-m)
        
        (DEFAULT: N)
        
        Whether or not to create a "masked" insertion genome. Instead of the
        specified sequence being inserted, a series of Ns of equal length to
        the sequence will be inserted instead.



EXAMPLES SCENARIO EXPLANATION:
    
    1:
    A minimal use case.
    
    2:
    Chimeric elements which have been marked for merge-joining will scan the
    last 6 nucleotides match of the pre-junction component sequence and the
    first 6 nucleotides of the post-junction component sequence, and if the
    two have 1 or fewer mismatches, the "junction" will not be duplicated in the
    resulting chimeric output sequence.
    
    3:
    Insert sequences and mask them.

EXAMPLES:
    
    python27 Sequence_Inserter.py Path/PostExGenomeFolder Path/PostEdCoords.tsv
            Path/ExtractedSequencesFolder
    
    python27 Sequence_Inserter.py Path/PostExGenomeFolder Path/PostEdCoords.tsv
            Path/ExtractedSequencesFolder -o Path/FinalGenomeFolder
            Path/FinalCoords.tsv Path/FinalSizes.tsv -a 6 7 1 Y
    
    python27 Sequence_Inserter.py Path/PostExGenomeFolder Path/PostEdCoords.tsv
            Path/ExtractedSequencesFolder -m Y

USAGE:
    
    python27 Sequence_Inserter.py <genome_folder> <coordinates_table>
            <sequences_folder> [-o <output_folder> <output_coordinates_table>
            <output_chr_sizes_file>] [-a <window_min> <window_max>
            <errors_max> Y|N] [-m Y|N]
"""

NAME = "Sequence_Inserter.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

DIRMOD__EDIT = "__INSERTED"
FILEMOD__COORDS = "__POST_INSERT_COORDS.tsv"
FILEMOD__SIZES = "__POST_INSERT_SIZES.tsv"
FILEMOD__FASTA = ".fa"

CONFIG__ignore_bad_slicing = False
CONFIG__mismatch_handling = 0



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__width = 80

DEFAULT__overhang_min = 4
DEFAULT__overhang_max = 100
DEFAULT__overhang_mismatches = 0
DEFAULT__overhang_largest = True
DEFAULT__mask = False



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
from _Command_Line_Parser import *

from NSeq_Match import *
from ECSASS_Parser import *

from Chr_FASTA_File_Reader import *
from Table_File_Reader import *
from Width_File_Writer import *



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Sequence_Inserter.py -h"

STR__error_no_FASTA = """
ERROR: No FASTA files detected in:
    {f}"""

STR__irregular_direction = """
WARNING: Irregular directionality symbol detected.
    "+" is used to denote forward-oriented sequences
    "-" is used to denote sequences on the complementary strand
    Any other symbol or text will be irregular, and default to being treated as
        a forward-oriented sequence."""

STR__min_greater_than_max = """
ERROR: The minimum permitted overlap window size must not be greater than the
maximum permitted overlap window size."""

STR__invalid_min_oh = """
ERROR: Invalid value given for minimum permitted overlap window size."""

STR__invalid_max_oh = """
ERROR: Invalid value given for maximum permitted overlap window size."""

STR__invalid_err_max = """
ERROR: Invalid value given for maximum permitted number of mismatches for a
window to qualify for overlap-merge."""

STR__invalid_high_pref = """
ERROR: Invalid value given for whether or not the highest permitted window size
is preferred."""

STR__invalid_mask = """
ERROR: Invalid value given for whether or not to mask the inserted sequences."""


STR__metrics = """
        Pre-insertion genome size: {A}
       Post-insertion genome size: {B}
    
            Number of chromosomes: {C}
    Average chromosome size (old): {D}
    Average chromosome size (new): {E}
    
                Number of inserts: {F}
               Basepairs inserted: {G}
              Average insert size: {H}"""

STR__Insert_begin = "\nRunning Insert_Sequences..."

STR__Insert_complete = "\nInsert_Sequences successfully finished."



STR__unexpected_failure = "\nProgram exited with an unexpected error."

STR__overwrite_confirm_2 = """
Files may exist in destination folder:
    {f}
Do you wish to overwrite them in the event of a naming clash? (y/n): """



# Lists ########################################################################

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]



# Dictionaries #################################################################



# Apply Globals ################################################################

PRINT.PRINT_ERRORS = PRINT_ERRORS
PRINT.PRINT_PROGRESS = PRINT_PROGRESS
PRINT.PRINT_METRICS = PRINT_METRICS



# Functions ####################################################################

def Insert_Sequences(input_genome, input_coordinates, input_sequences,
            output_genome, output_coordinates, output_chr_sizes, overhang_min,
            overhang_max, error_max, highest_preferred, mask):
    """
    Assemble and insert DNA sequences into the DNA template (usually a genome or
    genome-like biological entity) according to the sequence assembly
    instructions and the genomic coordinates.
    
    @input_genome
            (str - dirpath)        
            The input folder containing the template FASTA file(s). Each FASTA
            file is assumed to only contain one DNA sequence per file, similar
            to chromosomal FASTA files.
    @input_coordinates
            (str - filepath)
            The input file containing the coordinates for sequences to be
            inserted, as well as how to obtain the sequence. The first six
            columns need to contain the genomic coordinates:
                
                1) Chromosome name
                2) Start
                3) End
                4) Directionality* (+/-)
                5) ID/Name (Unneeded)
                6) How to obtain the genetic sequence:
                    
                    Raw genetic sequences can either be specified by "FILE:" or
                    "SEQ:". "FILE:" means to lift a sequence from the following
                    FASTA file, while "SEQ:" means to use the following text as
                    the sequence.
                    
                    "INV:" means to invert the following sequence.
                
                    "+" means to join/concatenate two sequences together.
                
                    "~+" means to overlap-join/overlap-concatenate two sequences
                    together. The last X nucleotides of the first sequence and
                    the last X nucleotides of the last sequence which align will
                    "merge" and only appear once. X needs to be, at minimum, 4
                    or higher. Ex. "SEQ:NNNNNAACC~+SEQ:AACCNNNNN" will result in
                    "NNNNNAACCNNNNN" instead of "NNNNNAACCAACCNNNNN".
                    
                    "*X" means to diplicate a sequence X times.
                    
                    "~*X" means to overlap-duplicate a sequence X times. The
                    last X nucleotides of the sequence and the first X
                    nucleotides which align will "merge" and only appear once. X
                    needs to be, at minimum, 4 or higher.
                    Ex. "SEQ:AACCNNNNNAACC~*3" will result in
                    "AACCNNNNNAACCNNNNNAACCNNNNNAACC" instead of
                    "AACCNNNNNAACCAACCNNNNNAACCAACCNNNNNAACC".
                    
                    Standard string slicing:
                    "[X:Y]" means to remove all nucleotides before index X, not
                    inclusive, and after index Y, inclusive. If no number is
                    provided before the colon, all nucleotides up to index Y,
                    not inclusive, will be kept. If no number is provided after
                    the colon, all nucleotides after index X, inclusive, will be
                    kept. The first position is index 0. Negative numbers can be
                    used to indicate the index when counting backwards from the
                    end. (-1 means the last index, -2 means the second last
                    index, etc.)
                    
                    Truncation slicing:
                    "![X:Y]" means to remove all nucleotides after index X,
                    inclusive, and before index Y, not inclusive. The first
                    position is index 0. Negative numbers can be used to
                    indicate the index when counting backwards from the end. (-1
                    means the last index, -2 means the second last index, etc.)
                    
                    "(" and ")"
                    Curved brackets may be used to indicate order of operations.
        
            The genomic coordinates apply to the pre-insertion template, and
            insert at the nucleotide specified in the start column, not after.
            (So inserting a sequence into position 1 will insert at the very
            start of the chromosome, effectively displacing ALL nucleotides.)
    @input_sequences
            (str - dirpath)
            A folder containing the sequences which are to be inserted.
    @output_genome
            (str - dirpath)
            The post-insertion version of the original template from which the
            sequences were extracted.
    @output_coordinates
            (str - filepath)
            The file containg the post-insertion coordinates and other details
            of the inserted sequences.
    @output_chr_sizes
            (str - filepath)
            The output file containing the new chromosome sizes.
    @overhang_min
            (int)
            The minimum window size allowed for overlap-joins and
            overlap-duplicates. Assumed to be smaller than, or equal to
            [overhang_max].
    @overhang_max
            (int)
            The maximum window size allowed for overlap-joins and
            overlap-duplicates. Assumed to be greater than, or equal to
            [overhang_min].
    @error_max
            (int)
            The maximum number of mismatches permitted for two sequences to
            qualify for an overlap-join or an overlap-duplicate.
    @highest_preferred
            (bool)
            Whether or not the largest qualifying window size will be used for
            overlap-joins and overlap-duplicates. If False, the smallest
            qualifying window will be used instead.
    @mask
            (bool)
            Whether or not to "masked" the inserted sequences by replacing them
            with a string of Ns of equal length.
    
    Return a value of 0 if the function runs successfully.
    Return a value of 1 if there is a problem accessing the data or if there are
            no valid FASTA files in the input genome folder.
    Return a value of 2 if there is a problem with the output file.
    Return a value of 3 if there is a problem during the sequence extraction
            process.
    
    Insert_Sequences(str, str, str, str, str, int, int, int, bool) -> int
    """
    # Setup reporting
    chromosomes = 0
    basepairs_original = 0
    seqs_inserted = 0
    basepairs_inserted = 0
    
    irregular_direction = False
    
    # Pre-calculate
    if highest_preferred: window_range = range(overhang_max, overhang_min, -1)
    else: window_range = range(overhang_min, overhang_max)
    
    # Setup the I/O
    current_chr_name = ""
    f = Chr_FASTA_Reader() # Chromosome reader
    original_index = -1
    total_index = -1
    
    t = Table_Reader(input_coordinates) # Coordinates table file reader
    t.Set_Delimiter("\t")
    
    o = Width_File_Writer() # Write new chromosomes
    o.Overwrite_Allow()
    o.Set_Width(DEFAULT__width)
    o.Set_Newline("\n")
    o.Toggle_Printing_M(False)
    
    c = open(output_coordinates , "w") # New coordinates table
    
    s = open(output_chr_sizes, "w") # New chromosome sizes
    
    # Main loop
    PRINT.printP(STR__Insert_begin)
    t.Open()
    while not t.End():
        seqs_inserted += 1
        # Read
        t.Read()
        elements = t.Get_Current()
        chr_name = elements[0]
        start = int(elements[1])
        start_ = start - 1
        end = int(elements[2])
        size = end-start+1
        direction = elements[3]
        ECSASS_seq = elements[5]
        retain = elements[4:]
        # New chromosome
        if chr_name != current_chr_name:
            # Finish up previous chromosome
            while not f.End():
                f.Read()
                total_index += 1
                o.Write_1(f.Get())
                basepairs_original += 1
            f.Close()
            if o.IsOpen(): o.Newline()
            o.Close()
            if current_chr_name:
                s.write(current_chr_name + "\t" + str(total_index) + "\n")
            # New chromosome - reading
            current_chr_name = chr_name
            chr_file_path = Get_Chr_File_Path(input_genome, chr_name)
            f.Open(chr_file_path)
            # New chromosome - writing
            chr_write_path = output_genome + "\\" + chr_name + FILEMOD__FASTA
            o.Open(chr_write_path)
            o.Write_F(">" + f.Get_Name())
            o.Newline()
            # Others
            chromosomes += 1
            original_index = 0
            total_index = 0
        # Copy until insertion point
        while original_index < start_:
            f.Read()
            original_index += 1
            total_index += 1
            o.Write_1(f.Get())
            basepairs_original += 1
        # New sequence
        seq = Parse_ECSASS(ECSASS_seq, [input_sequences], window_range,
                error_max, CONFIG__ignore_bad_slicing,
                CONFIG__mismatch_handling)
        if mask:
            seq = len(seq)*"N"
        else:
            if direction == "-": seq = Get_Complement(seq)
            elif direction == "+": pass
            else: irregular_direction = True
        length = len(seq)
        total_start = str(total_index + 1)
        total_end = str(total_index + length)
        # Insert sequence
        o.Write(seq)
        c.write(chr_name + "\t" + total_start + "\t" + total_end + "\t" +
                direction + "\t" + "\t".join(retain) + "\n")
        total_index += length
        basepairs_inserted += length
    
    PRINT.printP(STR__Insert_complete)
    
    # Close up
    t.Close()
    c.close()
    
    while not f.End():
        f.Read()
        total_index += 1
        o.Write_1(f.Get())
        basepairs_original += 1
    o.Newline()
    o.Close()
    f.Close()
    
    if current_chr_name:
        s.write(current_chr_name + "\t" + str(total_index) + "\n")
    s.close()
    
    # Reporting
    Report_Metrics(chromosomes, basepairs_original, seqs_inserted,
            basepairs_inserted, irregular_direction)
    
    # Wrap up
    return 0

def Get_Chr_File_Path(genome_folder_path, chr_name):
    """
    Return the file path to the Chromosomal FASTA file with [chr_name] as its
    name from the directory [genome_folder_path].
    Return an empty string if no matching file name is found.
    """
    names = os.listdir(genome_folder_path)
    for name in names:
        first = name.split(".")[0]
        if first == chr_name:
            filepath = genome_folder_path + "\\" + name
            return filepath
    return ""

def Report_Metrics(chromosomes, basepairs_original, seqs_inserted,
            basepairs_inserted, irregular_direction):
    """
    Print a report into the command line interface of the metrics of the
    operation.
    
    @chromosomes
            (int)
            The number of chromosomes which were processed.
    @basepairs_original
            (int)
            The number of basepairs in the original chromosomes.
    @seqs_inserted
            (int)
            The number of sequences inserted into the chromosomes.
    @basepairs_inserted
            (int)
            The number of basepairs inserted into the chromosomes.
    @irregular_direction
            (bool)
            Whether or not a directionality symbol occured in the file which was
            not either a "+" or a "-".
    
    Report_Metrics(int, int, int, int, int) -> None
    """
    if irregular_direction: PRINT.printE(STR__irregular_direction)
    # Calculate
    new_size = basepairs_original + basepairs_inserted
    avg_chr_size_pre = basepairs_original/(float(chromosomes))
    avg_chr_size_post = new_size/(float(chromosomes))
    avg_insert_size = (float(basepairs_inserted))/seqs_inserted
    # Strings
    chromosomes = str(chromosomes) + "   "
    basepairs_original = str(basepairs_original) + "   "
    seqs_inserted = str(seqs_inserted) + "   "
    basepairs_inserted = str(basepairs_inserted) + "   "
    new_size = str(new_size) + "   "
    avg_chr_size_pre = str(avg_chr_size_pre) + "0"
    avg_chr_size_pre = Trim_Percentage_Str(avg_chr_size_pre, 2)
    avg_chr_size_post = str(avg_chr_size_post) + "0"
    avg_chr_size_post = Trim_Percentage_Str(avg_chr_size_post, 2)
    avg_insert_size = str(avg_insert_size) + "0"
    avg_insert_size = Trim_Percentage_Str(avg_insert_size, 2)
    # Pad
    max_size = max([len(chromosomes), len(basepairs_original), len(new_size),
            len(seqs_inserted), len(basepairs_inserted), len(avg_chr_size_pre),
            len(avg_chr_size_post)])
    chromosomes = Pad_Str(chromosomes, max_size, " ", 0)
    basepairs_original = Pad_Str(basepairs_original, max_size, " ", 0)
    seqs_inserted = Pad_Str(seqs_inserted, max_size, " ", 0)
    basepairs_inserted = Pad_Str(basepairs_inserted, max_size, " ", 0)
    new_size = Pad_Str(new_size, max_size, " ", 0)
    avg_chr_size_pre = Pad_Str(avg_chr_size_pre, max_size, " ", 0)
    avg_chr_size_post = Pad_Str(avg_chr_size_post, max_size, " ", 0)
    avg_insert_size = Pad_Str(avg_insert_size, max_size, " ", 0)
    # Print
    PRINT.printM(STR__metrics.format(A = basepairs_original, B = new_size,
            C = chromosomes, D = avg_chr_size_pre, E = avg_chr_size_post,
            F = seqs_inserted, G = seqs_inserted, H = avg_insert_size))



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Insert_Sequences(raw_command_line_input):
    """
    Parse the command line input and call the Insert_Sequences function
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
        return 0
    
    # Initial validation
    if len(inputs) < 3:
        PRINT.printE(STR__insufficient_inputs)
        PRINT.printE(STR__use_help)
        return 1
    
    # Validate mandatory inputs
    input_genome_filepath = inputs.pop(0) # Input genome
    valid = Validate_FASTA_Folder(input_genome_filepath)
    if valid == 1:
        PRINT.printE(STR__IO_error_read_folder)
        PRINT.printE(STR__use_help)
        return 1
    elif valid == 2:
        PRINT.printE(STR__error_no_FASTA.format(f = input_genome_filepath))
        PRINT.printE(STR__use_help)
        return 1
    input_coordinates_filepath = inputs.pop(0) # Input coordinates
    valid = Validate_Read_Path(input_coordinates_filepath)
    if valid == 1:
        PRINT.printE(STR__IO_error_read.format(f = input_coordinates_filepath))
        PRINT.printE(STR__use_help)
        return 1
    input_sequences_filepath = inputs.pop(0)
    valid = Validate_FASTA_Folder(input_sequences_filepath) # Input seqs
    if valid == 1:
        PRINT.printE(STR__IO_error_read_folder)
        PRINT.printE(STR__use_help)
        return 1
    elif valid == 2:
        PRINT.printE(STR__error_no_FASTA.format(f = input_sequences_filepath))
        PRINT.printE(STR__use_help)
        return 1
    
    # Set up rest of the parsing
    path_out_genome = input_genome_filepath + DIRMOD__EDIT
    path_out_coords = input_coordinates_filepath + FILEMOD__COORDS
    path_out_sizes = input_genome_filepath + FILEMOD__SIZES
    overhang_min = DEFAULT__overhang_min
    overhang_max = DEFAULT__overhang_max
    error_max = DEFAULT__overhang_mismatches
    highest_preferred = DEFAULT__overhang_largest
    mask = DEFAULT__mask
    
    # Initial validation
    while inputs:
        arg = inputs.pop(0)
        flag = 0
        try: # Following arguments
            if arg in ["-m"]:
                arg2 = inputs.pop(0)
            elif arg in ["-o"]:
                arg2 = inputs.pop(0)
                arg3 = inputs.pop(0)
                arg4 = inputs.pop(0)
            elif arg in ["-a"]:
                arg2 = inputs.pop(0)
                arg3 = inputs.pop(0)
                arg4 = inputs.pop(0)
                arg5 = inputs.pop(0)
            else: # Invalid
                arg = Strip_X(arg)
                PRINT.printE(STR__invalid_argument.format(s = arg))
                PRINT.printE(STR__use_help)
                return 1
        except:
            PRINT.printE(STR__insufficient_inputs)
            PRINT.printE(STR__use_help)
            return 1
        if arg == "-a":
            flag = False
            overhang_min = Validate_Int_NonNeg(arg2)
            overhang_max = Validate_Int_NonNeg(arg3)
            error_max = Validate_Int_NonNeg(arg4)
            highest_preferred = Validate_Bool(arg5)
            if overhang_min == -1:
                flag = True
                PRINT.printE(STR__invalid_min_oh.format(s = arg2))
            if overhang_max == -1:
                flag = True
                PRINT.printE(STR__invalid_max_oh.format(s = arg3))
            if error_max == -1:
                flag = True
                PRINT.printE(STR__invalid_err_max.format(s = arg3))
            if highest_preferred == None:
                flag = True
                PRINT.printE(STR__invalid_high_pref.format(s = arg3))
            if overhang_min > overhang_max:
                flag = True
                PRINT.printE(STR__min_greater_than_max)
            if flag: return 1
        elif arg == "-o":
            path_out_genome = arg2
            path_out_coords = arg3
            path_out_sizes = arg4
        elif arg == "-m":
            mask = Validate_Bool(arg2)
            if mask == None:
                PRINT.printE(STR__invalid_mask.format(s = arg3))
                return 1
    
    # Validate output paths
    valid_out = Validate_Write_Path__FOLDER(path_out_genome)
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
    valid_out_1 = Validate_Write_Path__FILE(path_out_coords)
    valid_out_2 = Validate_Write_Path__FILE(path_out_sizes)
    valids = [valid_out_1, valid_out_2]
    if valid_out_1 == 0 and valid_out_2 == 0: pass
    elif valid_out_1 == 1 and valid_out_1 == 1:
        PRINT.printM(STR__overwrite_accept)
    else:
        if 2 in valids:
            PRINT.printE(STR__overwrite_decline)
        if 3 in valids:
            PRINT.printE(STR__IO_error_write_forbid)
        if 4 in valids:
            PRINT.printE(STR__IO_error_write_unable)
        return 1
    
    # Run program
    exit_state = Insert_Sequences(input_genome_filepath,
            input_coordinates_filepath, input_sequences_filepath,
            path_out_genome, path_out_coords, path_out_sizes,
            overhang_min, overhang_max, error_max, highest_preferred, mask)
    
    # Exit
    if exit_state == 0: return 0
    else:
        if exit_state == 1: PRINT.printE(STR__unexpected_failure)
        PRINT.printE(STR__use_help)
        return 1
    
    

def Validate_FASTA_Folder(dirpath):
    """
    Validates the dirpath of the input file as containing FASTA files.
    Return 0 if the dirpath is valid and contains at least 1 FASTA file.
    Return 1 if the dirpath is valid but contains no FASTA files.
    Return 2 if the dirpath is invalid.
    
    Validate_Read_Path(str) -> int
    """
    try:
        os.listdir(dirpath)
        files = Get_Files_W_Extensions(dirpath, LIST__FASTA)
        if len(files) > 0: return 0
        return 1
    except:
        return 2



def Validate_Write_Path__FILE(filepath):
    """
    Validates the filepath of the output file.
    Return 0 if the filepath is writtable.
    Return 1 if the user decides to overwrite an existing file.
    Return 2 if the user declines to overwrite an existing file.
    Return 3 if the file exists and the program is set to forbid overwriting.
    Return 4 if the program is unable to write to the filepath specified.
    
    Validate_Write_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
    except: # File does not exist. 
        try:
            f = open(filepath, "w")
            f.close()
            return 0 # File does not exist and it is possible to write
        except:
            return 4 # File does not exist but it is not possible to write
    # File exists
    if WRITE_PREVENT: return 3
    if WRITE_CONFIRM:
        confirm = raw_input(STR__overwrite_confirm.format(f = filepath))
        if confirm not in LIST__yes: return 2
    # User is not prevented from overwritting and may have chosen to overwrite
    try:
        f = open(filepath, "w")
        f.close()
        if WRITE_CONFIRM: return 1 # User has chosen to overwrite existing file
        return 0 # Overwriting existing file is possible
    except:
        return 4 # Unable to write to specified filepath

def Validate_Write_Path__FOLDER(folder_path):
    """
    Validates the writepath of the output folder.
    Attempts to create the folder if it does not exist.
    
    Return 0 if the folder path is valid and empty and can be written into.
    Return 1 if the folder path is valid and the user decides to overwrite
            existing files.
    Return 2 if the folder path is valid and empty but cannot be written into.
    Return 3 if the folder path is valid and the user declines to overwrite
            existing files.
    Return 4 if the folder path is valid, but contains existing files and the
            program is set to forbid overwriting.
    Return 5 is the folder path does not exist and cannot be created.
    Return 6 for unexpected errors.
    
    Validate_Folder_Path(str, str) -> int
    """
    new_dir = False
    # Create folder if it does not exist
    if not os.path.isdir(folder_path):
        try:
            os.mkdir(folder_path)
        except:
            return 5
        new_dir = True
    
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
        return 6
    
    if new_dir: return 0
    
    # OVERWRITE TESTING
    FLAG_exists = 0
    if WRITE_PREVENT: return 4
    if WRITE_CONFIRM:
        confirm = raw_input(STR__overwrite_confirm_2.format(f=folder_path))
        if confirm not in LIST__yes: return 3        
    return 1



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Insert_Sequences(sys.argv)


