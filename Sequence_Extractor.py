HELP_DOC = """
SEQUENCE EXTRACTOR
(version 1.0)
by Angelo Chan

This is a program for excising sequences from a genomic template, such as
extracting genetic elements from a genome.

The sequences will be excised according to a table of genomic coordinates (which
is assumed to be sorted and non-overlapping) and output into an output folder. A
post-excision version of the genome will be output into a different output
folder. A coordinates table will also be generated, recording where the
sequences were excised from and therefore, where they need to be inserted in the
post-excision version to restore the original.

Derivatives of the coordinates table can be made to simulate mutations. Changes
to the original excised sequences can simulate substitutions and indels, while
changes to the coordinates can simulate transposition. Replications and complete
deletions can also be simulated by modifying the coordinates table.

The Table_To_Table program can be used to adapt existing genomic coordinates
files to the format required for the input coordinates file.



IMPORTANT POINT TO NOTE:

If the coordinates of two Transposable Elements overlap, and the overlapped
Nucleotide is copied into both TE sequences, the overlapped Nucleotide will
be effectively duplicated upon reinsertion.



USAGE:
    
    python27 Sequence_Extractor.py <genome_folder> <target_coordinates_table>
            [-d Y|N] [-o <edited_genome_folder> <extracted_sequences_folder>
            <coordinates_table> <chr_sizes_file>]



MANDATORY:
    
    genome_folder
        
        The filepath of the input folder containing the template FASTA file(s).
        Each FASTA file is assumed to only contain one DNA sequence per file.
    
    target_coordinates_table
        
        The filepath of the input file containing the coordinates for extracting
        the target sequences from. The file needs to be in a TSV format and
        the first four columns need to contain the genomic coordinates:
            
            1) Chromosome name
            2) Start
            3) End
            4) Directionality* (+/-)
            
            * If the value in the Directionality column is neither "+" nor "-",
              the program will treat it as "+" by default. In cases where no
              directionality value is available, filling this column with random
              or irrelevant values will allow all entries to be treated as
              being on the forward strand of the "genome".
        
        This information will be retained as the first four columns of the
        output Coordinates Table file. The contents of any additional columns
        will also be retained in the seventh column and beyond of the output
        Coordinates Table file.

OPTIONAL:
    
    Y|N
        
        (DEFAULT: N)
        
        Whether or not to duplicate a nucleotide if the coordinates of two
        Transposable Elements overlap.
    
    edited_genome_folder
        
        (DEFAULT path generation available)
        
        The filepath of the output folder where resultant post-excision genomic
        templates will be outputted to.
    
    extracted_sequences_folder
        
        (DEFAULT path generation available)
        
        The filepath of the output folder where resultant excised sequences will
        be outputted to.
    
    coordinates_table
        
        (DEFAULT path generation available)
        
        The filepath of the output Coordinates Table file. This file will
        contain the information of a genetic element in each row, with its
        genomic coordinates in the first four columns, its ID in the fifth
        column, any additional input information in the seventh and up columns,
        while the sixth column will contain all the information necessary for
        determining its genomic sequence, including which original excised
        sequence is being used as the template, as well as any modifications
        which were subsequently made to said template.
    
    chr_sizes_file
        
        (DEFAULT path generation available)
        
        The filepath of the output chromosome sizes file. This file may be
        necessary when coordinates of the genetic elements are altered to
        simulate "transposition" or "duplication".



EXAMPLES SCENARIO EXPLANATION:
    
    1&2:
    A modified RMSK file is used to provide coordinates for the Transposons in a
    genome, which are cut out of it.

EXAMPLES:
    
    python27 Sequence_Extractor.py Path/GenomeFolder rmsk__MOD.tsv
    
    python27 Sequence_Extractor.py Path/GenomeFolder rmsk__MOD.tsv -o
            Path/TransposonlessGenome Path/Transposons
            Path/TransposonCoordinates.tsv Path/NewChrSizes.tsv -d Y

USAGE:
    
    python27 Sequence_Extractor.py <genome_folder> <target_coordinates_table>
            [-d Y|N] [-o <edited_genome_folder> <extracted_sequences_folder>
            <coordinates_table> <chr_sizes_file>]
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

DIRMOD__SEQS = "__EXTRACTS"
DIRMOD__EDIT = "__EXCISED"
FILEMOD__COORDS = "__POST_INSERT_COORDS.tsv"
FILEMOD__SIZES = "__POST_INSERT_SIZES.tsv"
FILEMOD__FASTA = ".fa"

# For name string
ID_BASE = "TE_"
ID_SIZE = 9



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__width = 80

DEFAULT__overlap = False



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
from _Command_Line_Parser import *

from NSeq_Match import *

from Chr_FASTA_File_Reader import *
from Table_File_Reader import *
from Width_File_Writer import *



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Sequence_Extractor.py -h"

STR__error_no_FASTA = """
ERROR: No FASTA files detected in:
    {f}"""

STR__error_no_chr = """
ERROR: Unable to open chromosome FASTA file:
    {c}"""



STR__metrics = """
    Sequences in template: {A}

    Basepairs in template: {B}
      Basepairs extracted: {C}
                 Overlaps: {D}
      Basepairs remaining: {E}

      Sequences extracted: {F}
     Average extract size: {G}"""

STR__Extract_begin = "\nRunning Extract_Sequences..."

STR__Extract_complete = "\nExtract_Sequences successfully finished."



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

def Extract_Sequences(input_genome, input_coordinates, overlap, output_genome,
            output_sequences, output_coordinates, output_chr_sizes):
    """
    Extract DNA sequences from the DNA template (usually a genome or genome-like
    biological entity) according to the input coordinates, and output the
    post-excision version of the template, the extracted sequences, and a
    table of coordinates for the output sequences.
    
    @input_genome
            (str - dirpath)
            The filepath of the folder containing the FASTA file(s) from which
            the sequences are to be extracted. Each file should only contain a
            single DNA sequence.
            The folder will typically be a "genome", with each of the files
            within being a chromosome, but does not absolutely have to be a
            "genome".
    @input_coordinates
            (str - filepath)
            The file containing the genomic coordinates and auxiliary
            information of the DNA sequences to be excised.
    @overlap
            (bool)
            Whether or not to duplicate nucleotides when the coordinates of
            neighboring genetic elements overlap. (Only applies to the single
            nucleotide at the end of the preceding genetic element.)
    @output_genome
            (str - dirpath)
            The post-excision version of the original template from which the
            sequences were extracted.
    @output_sequences
            (str - dirpath)
            A folder containing the sequences which were extracted. Each
            sequence will be stored in a separate FASTA file. Each sequence will
            also be given a new unique ID, which will also be used as the file
            name, and the sequence name. This ID will also be referenced in the
            resulting [output_coordinates] file, and subsequently derived files.
    @output_coordinates
            (str - filepath)
            The file containg the coordinates and details of the extracted
            sequences. It can be used to reinsert the extracted sequences back
            into the template. Derivatives of this file can be made which list
            genetic changes to the sequences, including substitutions,
            insertions, deletions, inversions, duplications, and fragmentations.
            These changes are listed in a way which is fairly human-readable,
            and without the need to create multiple folders containing highly
            similar information.
    @outpust_chr_sizes
            (str - filepath)
            The file containing the new chromosome sizes of [output_genome].
    
    Return a value of 0 if the function runs successfully.
    Return a value of 1 if there is a problem accessing the data or if there are
            no valid FASTA files in the input genome folder.
    Return a value of 2 if there is a problem with the output file.
    Return a value of 3 if there is a problem during the sequence extraction
            process.
    
    Extract_Sequences(str, str, bool, str, str, str, str) -> int
    """
    # Setup reporting
    chromosomes = 0
    basepairs_original = 0
    basepairs_excised = 0
    overlaps = 0
    seqs_excised = 0
    
    # Setup the I/O
    current_chr_name = ""
    f = Chr_FASTA_Reader()
    old_end = -1
    current_index = -1
    post_ex_index = -1
    non_direction_flag = False # For when an entry has no +/-
    sb = ""
    prev_n = ""
    
    t = Table_Reader(input_coordinates)
    t.Set_Delimiter("\t")
    
    c = open(output_coordinates, "w")
    s = open(output_chr_sizes, "w")
    w = Width_File_Writer()
    w.Overwrite_Allow()
    w.Set_Width(DEFAULT__width)
    w.Set_Newline("\n")
    w.Toggle_Printing_M(False)
    o = Width_File_Writer()
    o.Overwrite_Allow()
    o.Set_Width(DEFAULT__width)
    o.Set_Newline("\n")
    o.Toggle_Printing_M(False)
    
    # Main loop
    PRINT.printP(STR__Extract_begin)
    t.Open()
    while not t.End():
        seqs_excised += 1
        # Read
        t.Read()
        elements = t.Get_Current()
        chr_name = elements[0]
        start = int(elements[1])
        start_ = start - 1
        end = int(elements[2])
        size = end-start+1
        direction = elements[3]
        extras = elements[4:]
        # New chromosome
        if chr_name != current_chr_name:
            # Finish up previous chromosome
            while not f.End():
                f.Read()
                current_index += 1
                w.Write_1(f.Get())
                basepairs_original += 1
            f.Close()
            if current_chr_name:
                s.write(current_chr_name + "\t" + str(current_index) + "\n")
            # New chromosome
            current_chr_name = chr_name
            chr_file_path = Get_Chr_File_Path(input_genome, chr_name)
            f.Open(chr_file_path)
            if f.End():
                c.close()
                s.close()
                w.Close()
                o.Close()
                t.Close()
                PRINT.printE(STR__error_no_chr.format(c = chr_name))
                return 1
            chr_write_path = output_genome + "\\" + chr_name + FILEMOD__FASTA
            w.Close()
            w.Open(chr_write_path)
            w.Write_F(">" + f.Get_Name())
            w.Newline()
            chromosomes += 1
            old_end = -1
            current_index = 0
            post_ex_index = 1
        # Non overlap
        if start == old_end and overlap:
            overlaps += 1
            sb = prev_n
            basepairs_excised += 1
        old_end = end
        # Read along chromosome and add, to new template
        while current_index < start_:
            f.Read()
            current_index += 1
            w.Write_1(f.Get())
            post_ex_index += 1
            basepairs_original += 1
        # Read along chromosome and add, to sequences
        while current_index < end:
            f.Read()
            current_index += 1
            sb += f.Get()
            basepairs_excised += 1
            basepairs_original += 1
        # Last chromosome in sequence
        prev_n = f.Get()
        # Direction
        if direction == "-": sb = Get_Complement(sb, True)
        elif direction == "+": pass
        else: non_direction_flag = True
        # New coordinates
        post_ex_end = post_ex_index + size - 1
        # Process
        ID = Generate_Seq_ID(seqs_excised)
        path = output_sequences + "/" + ID + FILEMOD__FASTA
        o.Open(path)
        o.Write_F(">" + ID + "\t" + "\t".join(elements))
        o.Newline()
        o.Write(sb)
        o.Close_Newline()
        c.write(chr_name + "\t" + str(post_ex_index) + "\t")
        c.write(str(post_ex_end) + "\t" + direction + "\t")
        c.write(ID + "\tFILE(" + ID + ")\t")
        c.write("\t".join(extras) + "\n")
        # Reset stringbuilder
        sb = ""
    PRINT.printP(STR__Extract_complete)
    
    # Close up
    c.close()
    
    while not f.End():
        f.Read()
        w.Write_1(f.Get())
        basepairs_original += 1
    s.write(current_chr_name + "\t" + str(current_index) + "\n")
    s.close()
    
    w.Close()
    f.Close()
    
    t.Close()
    
    # Reporting
    Report_Metrics(chromosomes, basepairs_original, basepairs_excised,
            overlaps, seqs_excised)

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
    
def Generate_Seq_ID(counter):
    """
    Generate a sequence ID for a DNA sequence based on how many sequences have
    already been generated.
    """
    sb = Pad_Str(str(counter), ID_SIZE, "0", 0)
    sb = ID_BASE + sb
    return sb

def Report_Metrics(chromosomes, basepairs_original, basepairs_excised,
            overlaps, seqs_excised):
    """
    Print a report into the command line interface of the metrics of the
    operation.
    
    @chromosomes
            (int)
            The number of chromosomes which were processed.
    @basepairs_original
            (int)
            The number of basepairs in the original chromosomes.
    @basepairs_excised
            (int)
            The number of basepairs excised into separate sequences.
    @overlaps
            (int)
            The number of basepairs within overlap regions, and which were
            duplicated across both elements.
    @seqs_excised
            (int)
            The number of sequences which were excised.
    
    Report_Metrics(int, int, int, int, int) -> None
    """
    # Calculate
    remaining = basepairs_original - basepairs_excised + overlaps
    average_ex_size = basepairs_excised/float(seqs_excised)
    # Strings
    average_ex_size = str(average_ex_size) + "0"
    average_ex_size = Trim_Percentage_Str(average_ex_size, 2)
    chromosomes = str(chromosomes) + "   "
    basepairs_original = str(basepairs_original) + "   "
    basepairs_excised = str(basepairs_excised) + "   "
    overlaps = str(overlaps) + "   "
    remaining = str(remaining) + "   "
    seqs_excised = str(seqs_excised) + "   "
    # Pad
    max_size = max(len(average_ex_size), len(chromosomes), len(seqs_excised),
            len(basepairs_original), len(basepairs_excised), len(remaining),
            len(overlaps))
    average_ex_size = Pad_Str(average_ex_size , max_size, " " , 0)
    chromosomes = Pad_Str(chromosomes , max_size, " " , 0)
    basepairs_original = Pad_Str(basepairs_original , max_size, " " , 0)
    basepairs_excised = Pad_Str(basepairs_excised , max_size, " " , 0)
    overlaps = Pad_Str(overlaps , max_size, " " , 0)
    remaining = Pad_Str(remaining , max_size, " " , 0)
    seqs_excised = Pad_Str(seqs_excised , max_size, " " , 0)
    # Print
    PRINT.printM(STR__metrics.format(A = chromosomes, B = basepairs_original,
            C = basepairs_excised, D = overlaps, E = remaining,
            F = seqs_excised, G = average_ex_size))



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Extract_Sequences(raw_command_line_input):
    """
    Parse the command line input and call the Extract_Sequences function
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
    
    # Initial validation
    if len(inputs) < 2:
        PRINT.printE(STR__insufficient_inputs)
        PRINT.printE(STR__use_help)
        return 1
    
    # Validate mandatory inputs
    path_in_folder = inputs.pop(0)
    valid = Validate_FASTA_Folder(path_in_folder)
    if valid == 1:
        PRINT.printE(STR__IO_error_read_folder)
        PRINT.printE(STR__use_help)
        return 1
    elif valid == 2:
        PRINT.printE(STR__error_no_FASTA.format(f = path_in_folder))
        PRINT.printE(STR__use_help)
        return 1
    path_in_file = inputs.pop(0)
    valid = Validate_Read_Path(path_in_file)
    if valid == 1:
        PRINT.printE(STR__IO_error_read.format(f = path_in_file))
        PRINT.printE(STR__use_help)
        return 1
    
    # Set up rest of the parsing
    overlap = DEFAULT__overlap
    path_out_genome = path_in_folder + DIRMOD__EDIT
    path_out_seqs = path_in_folder + DIRMOD__SEQS
    path_out_coords = path_in_folder + FILEMOD__COORDS
    path_out_sizes = path_in_folder + FILEMOD__SIZES
    
    # Validate optional inputs (except output path)
    while inputs:
        arg = inputs.pop(0)
        try: # Second argument
            arg2 = inputs.pop(0)
        except:
            PRINT.printE(STR__insufficient_inputs)
            PRINT.printE(STR__use_help)
            return 1
        if arg == "-d": # Duplicate overlap nucleotides
            overlap = Validate_Bool(arg2)
            if overlap == None:
                PRINT.printE(STR__invalid_bool)
                PRINT.printE(STR__use_help)
        elif arg == "-o": # Output files
            try: # Third and fourth argument
                arg3 = inputs.pop(0)
                arg4 = inputs.pop(0)
                arg5 = inputs.pop(0)
            except:
                PRINT.printE(STR__insufficient_inputs)
                PRINT.printE(STR__use_help)
                return 1
            path_out_genome = arg2
            path_out_seqs = arg3
            path_out_coords = arg4
            path_out_sizes = arg5
        else: # Invalid
            arg = Strip_X(arg)
            PRINT.printE(STR__invalid_argument.format(s = arg))
            PRINT.printE(STR__use_help)
            return 1

    # Validate output paths
    valid_out_1 = Validate_Write_Path__FOLDER(path_out_genome)
    valid_out_2 = Validate_Write_Path__FOLDER(path_out_seqs)
    valids = [valid_out_1, valid_out_2]
    if valid_out_1 == 0 and valid_out_2 == 0: pass
    elif valid_out_1 == 1 and valid_out_1 == 1:
        PRINT.printM(STR__overwrite_accept)
    else:
        if 2 in valids: PRINT.printE(STR__IO_error_write_folder_cannot)
        if 3 in valids: PRINT.printE(STR__overwrite_decline)
        if 4 in valids: PRINT.printE(STR__IO_error_write_folder_forbid)
        if 5 in valids:
            PRINT.printE(STR__IO_error_write_folder_nonexistent)
        if 6 in valids: PRINT.printE(STR__IO_error_write_unexpected)
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
    exit_state = Extract_Sequences(path_in_folder, path_in_file, overlap,
            path_out_genome, path_out_seqs, path_out_coords, path_out_sizes)
    
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
    exit_code = Parse_Command_Line_Input__Extract_Sequences(sys.argv)


