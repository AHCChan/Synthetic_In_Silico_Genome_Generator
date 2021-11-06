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
            <sequences_folder> [-o <output_folder> <output_coordinates_table]
            [-a <window_min> <window_max> <errors_max> Y|N]



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
        
        (DEFAULT: 0)
        
        Whether or not the largest qualifying window size will be used for
        overlap-joins and overlap-duplicates. If set to "N", the smallest
        qualifying window will be used instead.



EXAMPLES SCENARIO EXPLANATION:

EXAMPLES:

USAGE:
    
    python27 Sequence_Inserter.py <genome_folder> <coordinates_table>
            <sequences_folder> [-o <output_folder> <output_coordinates_table]
            [-a <window_min> <window_max> <errors_max> Y|N]
"""

NAME = "Sequence_Extractor.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

DIRMOD__EDIT = "__INSERTED"
FILEMOD__COORDS = "__FINAL_COORDS.tsv"
FILEMOD__FASTA = ".fa"



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__width =  = 80

DEFAULT__overhang_min = 4
DEFAULT__overhang_max = 100
DEFAULT__overhang_mismatches = 0
DEFAULT__overhang_largest = True



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
"Sequence_Extractor.py -h"

STR__error_no_FASTA = """
ERROR: No FASTA files detected in:
    {f}"""



STR__metrics = """
     Pre-insertion genome size: {A}
    Post-insertion genome size: {B}
    
         Number of chromosomes: {C}
       Average chromosome size: {D}
    
             Number of inserts: {E}
           Average insert size: {F}"""

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
            overhang_max, error_max, highest_preferred):
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
        start_ = start -1
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
        # New sequence
        seq = Parse_ECSASS(ECSASS_seq)
        if direction == "-": seq = Get_Complement(seq)
        elif direction == "+": pass
        else: irregular_direction = True
        length = len(seq)
        total_start = str(total_index)
        total_end = str(total_index + length - 1)
        # Insert sequence
        o.Write(seq)
        t.write(chr_name + "\t" + total_start + "\t" + total_end + "\t" +
                "\t".join(retain) + "\n")
        total_index += size
            
    PRINT.printP(STR__Insert_complete)
    
    # Close up
    t.Close()
    
    while not f.End():
        f.Read()
        total_index += 1
        o.Write_1(f.Get())
        basepairs_original += 1
    f.Close()
    o.Close()
    
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
    pass



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Insert_Sequences(raw_command_line_input):
    """
    Parse the command line input and call the Insert_Sequences function
    with appropriate arguments if the command line input is valid.
    """
    PRINT.printP(STR__parsing_args)



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Insert_Sequences(sys.argv)


