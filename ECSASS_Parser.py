"""
ECSASS PARSER
(version 1.0)
by Angelo Chan

The Ebert-Chan Sequence Assembly Syntax System Parser module, implemented in
Python.

The ECSASS system is a compact system for storing genetic sequence data,
designed for scenarios where the same sequence is duplicated multiple tims,
and some copies may be altered differently to other copies. The ECSASS system
records the original sequences which the final products are based on, and any
changes or alterations which have been made to them, rather than a hard copy of
the altered sequences themselves.

The ECSASS system allows multiple "changes" to the sequences to be made with
ease, and be displayed in a human-readable format while taking up very little
hard disk space. The downside is that ECSASS sequences need to be assembled
first before being able to be used as a standard genetic sequence, which will
increase the runtime of software which bridges between the ECSASS format and the
direct basepair by basepair recroding format.



SYNTAX:
    
    FILE(<name>)
        Refer to the genetic sequence from a file with filename <name>.
    
    SEQ(<seq>)
        Directly provide a genetic sequence in plain text format.
    
    INV()
        Invert the sequence specified within the brackets.
    
    +
        Join or concatenate two sequences together.
    
    *<X>
        Duplicate a sequence <X> number of times.
    
    ~+
        Overlap-join or overlap-concatenate two sequences together. The last N
        nucleotides of the first sequence and the last N nucleotides of the last
        sequence which align will "merge" and only appear once. 
    
    ~*<X>
        Overlap-duplicate a sequence <X> number of times. The last N nucleotides
        of the sequence and the first X nucleotides which align will "merge" and
        only appear once. 

            N
                (In the case of ~+ and ~*<X>)
                N is either the largest or smallest window size within a
                specified range for which there is a valid overlap. Whether the
                largest or smallest window size is used is specified by the
                user, as is the minimum and maximum window sizes and the
                maximum permissible number of mismatches.

    [<X>:<Y>]
        Standard string slicing. Remove all nucleotides before index <X>, not
        inclusive, and after index <Y>, inclusive. If no number is provided
        before the colon, all nucleotides up to index <Y>, not inclusive, will
        be kept. If no number is provided after the colon, all nucleotides after
        index <X>, inclusive, will be kept.
        The first position is index 0. Negative numbers can be used to indicate
        the index when counting backwards from the end.

    ![<X>:<Y>]
        Truncation string slicing. All nucleotides after index <X>, inclusive,
        and before index <Y>, not inclusive. The first position is index 0.
        Negative numbers can be used to indicate the index when counting
        backwards from the end.

    ()
        Curved brackets can be used to enforce order of operations.



EXAMPLES:

    SEQ(NNNNNAACC)~+SEQ(AACCNNNNN)
        
        ->  NNNNNAACCNNNNN
    
    SEQ(NNNNNAACC)~+SEQ(AACCNNNNN)
        
        ->  NNNNNAACCNNNNN
                
    SEQ(AACCNNNNNAACC)~*3
        
        ->  AACCNNNNNAACCNNNNNAACCNNNNNAACC
                
    SEQ(AAACCCGGGTTT)[3:9]
        
        ->  CCCGGG
                
    SEQ(AAACCCGGGTTT)[3:]
        
        ->  CCCGGGTTT
                
    SEQ(AAACCCGGGTTT)[:-3]
        
        ->  AAACCCGGG
                
    SEQ(AAACCCGGGTTT)![-9:-3]
        
        ->  AAATTT
                
    SEQ(AAACCCGGGTTT)![-9:-3]
        
        ->  AAATTT
                
    INV(SEQ(AAACCCCCC))
        
        ->  GGGGGGTTT
"""

# Imported Modules #############################################################

import sys
import os

from NSeq_Match import *
from _Command_Line_Parser import *



# Sets #########################################################################

LIST__nuc = set(["A", "C", "G", "T", "N", "a", "c", "g", "t", "n"])

LIST__fasta = set(["fa", "FA", "Fa", "fasta", "FASTA", "Fasta"])



# Functions ####################################################################

def Parse_ECSASS(ECSASS_seq, seq_folders, window_range, error_max,
            ignore_bad_slicing, mismatch_handling):
    """
    Parse and return an ECSASS sequence and transform it into a normal genetic
    sequence.
    
    @ECSASS_seq
            (str)
            The input ECSASS sequence to be parsed. Requires that none of the
            files referenced have whitespaces in their file names. If file names
            contain whitespaces, users may need to resort to _Parse_ECSASS(),
            which may be rendered nonfunctional by the presence of other
            whitespace characters.
    @seq_folders
            (list<str - dirpath>)
            The folders containing the FASTA files containing the sequences
            which will be used to generate the final sequences. In the event of
            a name conflict, the folders listed earlier in this list will be
            given priority.
    @window_range
            (list<int>)
            A list of acceptable overlap window sizes, in order of preference.
    @error_max
            (int)
            The maximum number of mismatches permitted for two sequences to
            qualify for an overlap-join or an overlap-duplicate.
    @ignore_bad_slicing
            (bool)
            Whether or not to ignore bad string slicing indexes, typically for
            when the START index is higher than the END index.
    @mismatch_handling
            (int)
            How to handle mismatches, in the event some mismatches (@error_max)
            are permitted for overlap-joins and overlap-duplicates:
                0:  Use "N"
                1:  Use the char from the first sequence in joins
                    Use the char from the 5' end in duplicates
                2:  Use the char from the second sequence in joins
                    Use the char from the 3' end in duplicates
    
    Parse_ECSASS(str, str, int, int, int, bool) -> str
    """
    ECSASS_seq = Strip_Whitespaces(ECSASS_seq)
    return _Parse_ECSASS(ECSASS_seq, seq_folders, window_range, error_max,
            ignore_bad_slicing, mismatch_handling)

def Strip_Whitespaces(string):
    """
    Return [string] with all whitespaces removed.
    """
    sb = ""
    for c in string:
        if c != " ": sb += c
    return sb

def _Parse_ECSASS(ECSASS_seq, seq_folders, window_range, error_max,
            ignore_bad_slicing, mismatch_handling):
    """
    The recursive, subfunction of Parse_ECSASS(). Assumes [ECSASS_seq] contains
    no whitespace characters.
    """
    # print("\nPARSING:\n\t" + ECSASS_seq + "\n") # Development tool
    # Flags and counters
    parts = []
    operations = []
    sb = ""
    bracket_level = 0
    # Parsing infrastructure
    length = len(ECSASS_seq)
    # Traverse string
    i = 0
    while i < length:
        char = ECSASS_seq[i]
        # Brackets
        if char == "(":
            bracket_level += 1
        elif char == ")":
            bracket_level -= 1
            if bracket_level < 0:
                raise Exception("ERROR: Unmatched closing bracket.")
            elif bracket_level == 0:
                sb = _Parse_ECSASS(sb[1:], seq_folders, window_range, error_max,
                        ignore_bad_slicing, mismatch_handling)
                parts.append(sb)
                sb = ""
        # In brackets
        if bracket_level:
            sb += char
        # File
        elif ECSASS_seq[i:i+5] == "FILE(":
            i += 5
            char = ECSASS_seq[i]
            while char and char != ")":
                sb += char
                i += 1
                char = ECSASS_seq[i]
            seq = Get_Seq_From_File(sb, seq_folders)
            parts.append(seq)
            sb = ""
        # Sequence
        elif ECSASS_seq[i:i+4] == "SEQ(":
            i += 4
            char = ECSASS_seq[i]
            while char and char != ")":
                # if char in LIST__nuc: raise Exception
                sb += char
                i += 1
                char = ECSASS_seq[i]
            parts.append(sb)
            sb = ""
        # Invert
        elif ECSASS_seq[i:i+4] == "INV(":
            i += 4
            bracket_level += 1
            while bracket_level > 0:
                try:
                    char = ECSASS_seq[i]
                except:
                    raise Exception("ERROR: Unmatched closing bracket.")
                # Brackets
                if char == "(":
                    bracket_level += 1
                elif char == ")":
                    bracket_level -= 1
                # Other
                sb += char
                i += 1
            sb = sb[:-1] # Remove trailing bracket
            sb = _Parse_ECSASS(sb, seq_folders, window_range, error_max,
                        ignore_bad_slicing, mismatch_handling)
            sb = Get_Complement(sb, True)
            parts.append(sb)
            sb = ""
            i -= 1
        # Slice
        elif char == "[" or ECSASS_seq[i:i+2] == "![":
            # Check for string to slice
            if not parts: raise Exception("ERROR: No sequence to slice.")
            # Slice type
            if char == "[":
                flag = True # True for keep, False for excise
                i += 1
            else:
                flag = False
                i += 2
            # Setup
            start = ""
            end = ""
            # Parse first number
            loop = True
            while loop:
                try:
                    char = ECSASS_seq[i]
                except:
                    raise Exception("ERROR: Unmatched opening square bracket.")
                if char == ":": loop = False
                else: start += char
                i += 1
            # Parse second number
            loop = True
            while loop:
                try:
                    char = ECSASS_seq[i]
                except:
                    raise Exception("ERROR: Unmatched opening square bracket.")
                if char == "]": loop = False
                else: end += char
                i += 1
            i -= 1 # Undo last forward
            # Process numbers
            try:
                if start: start = int(start)
                else: start = None
                if end: end = int(end)
                else: end = None
            except:
                raise Exception("ERROR: Invalid indexes for string slicing.")
            # Slice
            if flag: parts[-1] = parts[-1][start:end]
            else:
                if start and end:
                    length_ = len(parts[-1])
                    if start < 0: start = length_ + start
                    if end < 0: end = length_ + end
                    if end < start and not ignore_bad_slicing:
                        raise Exception("ERROR: Overlapping indexes for "\
                                "string slicing.")
                    temp = parts[-1][:start] + parts[-1][end:]
                elif start:
                    temp = parts[-1][:start]
                elif end:
                    temp = parts[-1][end:]
                parts[-1] = temp
        # Join and overlap-join
        elif char == "+":
            operations.append([1, None])
        elif ECSASS_seq[i:i+2] == "~+":
            operations.append([2, None])
            i += 1
        # Duplicate and overlap-duplicate
        elif char == "*" or ECSASS_seq[i:i+2] == "~*":
            # Check for preceding part
            if not parts: raise Exception("ERROR: Sequence required before "\
                    "operator.")
            # Duplicate type
            if char == "*":
                type_ = 3 # 3 for no overlap, 4 for overlap
                i += 1
            else:
                type_ = 4
                i += 2
            # First
            try:
                char = ECSASS_seq[i]
            except:
                raise Exception("ERROR: Multiplier required.")
            # Get number
            while char and char.isdigit():
                sb += char
                i += 1
                try:
                    char = ECSASS_seq[i]
                except:
                    char = ""
                    i += 1
            i -= 1
            # Convert and append
            num = int(sb)
            operations.append([type_, num])
            sb = ""
        # Invalid
        else:
            raise Exception("ERROR: Unknown parsing error.")     
        # Prep for next loop iteration
        i += 1
    # Unclosed loop
    if bracket_level:
        raise Exception("ERROR: Unmatched opening bracket.")
    # Combine Parts
    while operations:
        op_type, arg2 = operations.pop(0)
        if op_type == 1: # Add
            parts[0] = parts[0] + parts.pop(1)
        elif op_type == 2: # Overlap-add
            parts[0] = Overlap_Add(parts[0], parts.pop(1), window_range,
                    error_max, mismatch_handling)
        elif op_type == 3: # Duplicate
            parts[0] = parts[0] * arg2
        elif op_type == 4: # Overlap-duplicate
            parts[0] = Overlap_Dup(parts[0], arg2, window_range, error_max,
                    mismatch_handling)
        else:
            raise Exception("\nCRITICAL ERROR\n")
    # Excess parts
    if len(parts) > 1:
        raise Exception("ERROR: Excess components in the formula. Operator "\
                "may potentially be missing.")
    # Return
    return parts[0]

def Get_Seq_From_File(name, folders):
    """
    Get the genetic sequence from a file with [name] from folders. The folders
    will be scanned in order of listing, with the folders listed earlier
    effectively being given priority in the event of a naming clash.
    
    @name
            (str)
            The name of the file, such as a gene name.
    @folders
            (list<str - dirpath>)
            A list of folder paths, which will be scanned.
    
    Get_Seq_From_File(str, list<str>) -> str
    """
    # Attempt to locate file
    final_path = ""
    for folder in folders:
        file_names = os.listdir(folder)
        for file_name in file_names:
            file_name_, ext = Get_File_Name_Ext(file_name)
            if file_name_ == name and ext in LIST__fasta:
                searching = False
                if not final_path: final_path = folder + "//" + file_name
    # File not located
    if not final_path: raise Exception("No file named \"{S}\" found.".format(
            S = name))
    # File located, extract sequence
    seq = ""
    f = open(final_path, "U")
    f.readline()
    for line in f:
        if line and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
        seq += line
    f.close()
    return seq

def Overlap_Add(seq1, seq2, window_range, error_max, mismatch_handling):
    """
    Attempts to overlap-join two sequences.
    
    The function scans the list of acceptable window ranges, and searches for
    the first window size for which the last N nucleotides of [seq1] and the
    last N nucleotides of [seq2] match each other with [error_max] or fewer
    mismatches.
    
    If no acceptable window size is found, the two sequences will be joined
    normally.
    
    @seq1
            (str)
            The first nucleotide sequence. Will form the 5' end of the resulting
            chimeric sequence.
    @seq2
            (str)
            The second nucleotide sequence. Will form the 3' end of the
            resulting chimeric sequence.
    @window_range
            (list<int>)
            A list of acceptable window sizes, in order of preference.
    @error_max
            (int)
            The maximum permitted number of mismatches for a window to be
            classified as an overlap.
    @mismatch_handling
            (int)
            How mismatches should be handled when generating the resulting
            chimeric sequence:
                0:  Use "N"
                1:  Use the nucleotide in [seq1]
                2:  Use the nucleotide in [seq2]
        
    Overlap_Add(str, str, list<int>, int, int) -> str
    """
    overlap_size = Find_Overlap(seq1, seq2, window_range, error_max)
    if overlap_size == -1: return seq1 + seq2
    else:
        junction = Get_Junction(seq1, seq2, overlap_size, mismatch_handling)
        return seq1[:-overlap_size] + junction + seq2[overlap_size:]
    
def Overlap_Dup(seq1, multiplier, window_range, error_max, mismatch_handling):
    """
    Attempts to overlap-duplicate a sequence
    
    The function scans the list of acceptable window ranges, and searches for
    the first window size for which the last N nucleotides of [seq1] and the
    last N nucleotides of [seq1] match each other with [error_max] or fewer
    mismatches.
    
    The overlap junction will only appear once, not twice in the resulting
    back-to-back duplicates of [seq1]
    
    @seq1
            (str)
            The nucleotide sequence to be duplicated.
    @multiplier
            (int)
            The number of times the sequence is to be duplicated.
    @window_range
            (list<int>)
            A list of acceptable window sizes, in order of preference.
    @error_max
            (int)
            The maximum permitted number of mismatches for a window to be
            classified as an overlap.
    @mismatch_handling
            (int)
            How mismatches should be handled when generating the resulting
            chimeric sequence:
                0:  Use "N"
                1:  Use the nucleotide in [seq1]
                2:  Use the nucleotide in [seq2]
        
    Overlap_Add(str, int, list<int>, int, int) -> str
    """
    overlap_size = Find_Overlap(seq1, seq1, window_range, error_max)
    if overlap_size == -1: return seq1 * multiplier
    else: 
        junction = Get_Junction(seq1, seq1, overlap_size, mismatch_handling)
        multi = (junction + seq1[overlap_size:-overlap_size]) * multiplier
        return multi + junction

def Find_Overlap(seq1, seq2, window_range, error_max):
    """
    Return the highest preferred window size for which the last N nucleotides of
    [seq1] and the first N nucleotides of [seq2] overlap with [error_max] or
    fewer matches.
    
    @seq1
            (str)
            The first nucleotide sequence. Will form the 5' end of the resulting
            chimeric sequence.
    @seq2
            (str)
            The second nucleotide sequence. Will form the 3' end of the
            resulting chimeric sequence.
    @window_range
            (list<int>)
            A list of acceptable window sizes, in order of preference.
    @error_max
            (int)
            The maximum permitted number of mismatches for a window to be
            classified as an overlap.
    
    Find_Overlap(str, str, list<int>, int) -> int
    """
    max_size = min([len(seq1), len(seq2)])
    for size in window_range:
        if size > max_size: pass
        else:
            errors = 0
            i = 0
            i_ = -size
            while i < size:
                if seq1[i_] != seq2[i]:
                    errors += 1
                    if errors > error_max: i = size
                i += 1
                i_ += 1
            if errors <= error_max: return size
    return -1

def Get_Junction(seq1, seq2, overlap_size, mismatch_handling):
    """
    Return the junction sequence formed by merging the last [overlap_size]
    nucleotides of [seq1] with the last [overlap_size] nucleotides of [seq2].
    
    @seq1
            (str)
            The first nucleotide sequence. Will provide the 5' end of the
            resulting chimeric sequence.
    @seq2
            (str)
            The second nucleotide sequence. Will provide the 3' end of the
            resulting chimeric sequence.
    @overlap_size
            (int)
            The size of the overlap junction.
    @mismatch_handling
            (int)
            How mismatches should be handled when generating the resulting
            chimeric sequence:
                0:  Use "N"
                1:  Use the nucleotide in [seq1]
                2:  Use the nucleotide in [seq2]
        
    Overlap_Add(str, str, int, int) -> str
    """
    sb = ""
    i = 0
    i_ = -overlap_size
    while i < overlap_size:
        if seq1[i_] == seq2[i]: sb += seq1[i_]
        else:
            if mismatch_handling == 1: sb += seq1[i_]
            elif mismatch_handling == 2: sb += seq2[i]
            else: sb += "N"
        i += 1
        i_ += 1
    return sb


