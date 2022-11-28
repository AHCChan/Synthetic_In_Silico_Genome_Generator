"""
NUCLEOTIDE SEQUENCE MATCHER
(version 2.2)
by Angelo Chan

This is a library of functions useful for querying and comparing nucleotide
sequences.
"""



# Configurations ###############################################################



# Imported Modules #############################################################



# Enums ########################################################################

class MATCH_TYPE:
    ONE=1
    TWO=2
    TWO_NOT=3
    STRICT=4
    STRICT_NOT=5



# Strings ######################################################################

STR__invalid_mode = "\nERROR: Invalid compare mode specified."

STR__seqs_must_be_equal_length = "\nERROR: Input sequences must be the same "\
        "length."

STR__query_seq_must_be_shorter = "\nERROR: Query sequences must be shorter "\
        "than the original sequence."


# Lists ########################################################################

LIST__all_n = ["A", "C", "G", "T", "R", "Y", "S", "W", "M", "K", "N", "X"]

# Basic matches
LIST__n_match__A = ["A"] # [A]denin
LIST__n_match__C = ["C"] # [C]ytosine
LIST__n_match__G = ["G"] # [G]uanine
LIST__n_match__T = ["T"] # [T]hymine
LIST__n_match__R = ["A", "G"] # Pu[r]ine
LIST__n_match__Y = ["C", "T"] # P[y]rimidine
LIST__n_match__S = ["C", "G"] # [S]trong
LIST__n_match__W = ["A", "T"] # [W]eak
LIST__n_match__M = ["A", "C"] # A[m]ino
LIST__n_match__K = ["G", "T"] # [K]eto
LIST__n_match__B = ["C", "G", "T"] # B+1 (Not A)
LIST__n_match__D = ["A", "G", "T"] # D+1 (Not C)
LIST__n_match__H = ["A", "C", "T"] # H+1 (Not G)
LIST__n_match__V = ["A", "C", "G"] # T+2 (Not T)
LIST__n_match__N = ["A", "C", "G", "T"]
LIST__n_match__X = LIST__n_match__N

# Extended matches
LIST__n_matchX__A = LIST__n_match__A
LIST__n_matchX__C = LIST__n_match__C
LIST__n_matchX__G = LIST__n_match__G
LIST__n_matchX__T = LIST__n_match__T
LIST__n_matchX__R = ["A", "G", "R"]
LIST__n_matchX__Y = ["C", "T", "Y"]
LIST__n_matchX__S = ["C", "G", "S"]
LIST__n_matchX__W = ["A", "T", "W"]
LIST__n_matchX__M = ["A", "C", "M"]
LIST__n_matchX__K = ["G", "T", "K"]
LIST__n_matchX__B = ["C", "G", "T", "Y", "S", "K"]
LIST__n_matchX__D = ["A", "G", "T", "R", "W", "K"]
LIST__n_matchX__H = ["A", "C", "T", "Y", "W", "M"]
LIST__n_matchX__V = ["A", "C", "G", "R", "S", "M"]
LIST__n_matchX__N = LIST__all_n
LIST__n_matchX__X = LIST__n_matchX__N



# Dictionaries #################################################################

DICT__complements = {"B": "V", "V": "B", "D": "H", "H": "D",
    "R": "Y", "Y": "R", "S": "S", "W": "W", "M": "M", "K": "K",
    "A": "T", "T": "A", "C": "G", "G": "C", "N": "N", "X": "X"}

DICT__matches = {
    "A": LIST__n_match__A, "C": LIST__n_match__C, "G": LIST__n_match__G,
    "T": LIST__n_match__T, "R": LIST__n_match__R, "Y": LIST__n_match__Y,
    "S": LIST__n_match__S, "W": LIST__n_match__W, "M": LIST__n_match__M,
    "K": LIST__n_match__K, "B": LIST__n_match__B, "D": LIST__n_match__D,
    "H": LIST__n_match__H, "V": LIST__n_match__V, "N": LIST__n_match__N,
    "X": LIST__n_match__X}

DICT__matchesX = {
    "A": LIST__n_matchX__A, "C": LIST__n_matchX__C, "G": LIST__n_matchX__G,
    "T": LIST__n_matchX__T, "R": LIST__n_matchX__R, "Y": LIST__n_matchX__Y,
    "S": LIST__n_matchX__S, "W": LIST__n_matchX__W, "M": LIST__n_matchX__M,
    "K": LIST__n_matchX__K, "B": LIST__n_matchX__B, "D": LIST__n_matchX__D,
    "H": LIST__n_matchX__H, "V": LIST__n_matchX__V, "N": LIST__n_matchX__N,
    "X": LIST__n_matchX__X}

DICT__n_match__1 = {} # 1-way match with an original and a query
DICT__n_match__2 = {} # 2-way match; potential matches can go both ways
DICT__n_match__2N = {} # 2-way anti-match. Opposite of DICT__n_match__2

DICT__mismatches = {"A": LIST__n_match__B, "C": LIST__n_match__D,
    "G": LIST__n_match__H, "T": LIST__n_match__V, "N": LIST__n_match__N}



# Resolve Dictionaries #########################################################

# DICT__n_match__1
for original in LIST__all_n: 
    ref = DICT__matchesX[original]
    temp = {}
    for query in LIST__all_n:
        if query in ref: temp[query] = 0
        else: temp[query] = 1
    DICT__n_match__1[original] = temp

# DICT__n_match__2
# DICT__n_match__N
for seq1 in LIST__all_n:
    ref1 = DICT__matchesX[seq1]
    temp1 = {}
    temp2 = {}
    for seq2 in LIST__all_n:
        ref2 = DICT__matchesX[seq2]
        if seq1 in ref2 or seq2 in ref1:
            temp1[seq2] = 0
            temp2[seq2] = 1
        else:
            temp1[seq2] = 1
            temp2[seq2] = 0
    DICT__n_match__2[seq1] = temp1
    DICT__n_match__2N[seq1] = temp2



# Functions ####################################################################

def Get_Complement(sequence, reverse=True):
    """
    Return the complement of the given nucleotide [sequence].
    
    If [reverse] is True, then the output sequence will be given in the 5' to 3'
    format. If [reverse] is False, then the output sequence will be in the same
    direction as the original sequence.

    @sequence
            (str - DNA Sequence)
    @reverse
            (bool)
            Whether the resulting sequence should be given in the 5' to 3'
            format, or be given in the same direction as the original sequence.
    
    Get_Complement(str, bool) -> str
    """
    sb = ""
    for n in sequence:
        c = DICT__complements[n]
        if reverse: sb = c + sb
        else: sb += c
    return sb



def Get_Earliest_Candidate_Match_Position(original, query, threshold=0,
            mode=MATCH_TYPE.ONE):
    """
    This function has not yet been implemented.
    """
    # Initial transformation and setup
    original = list(original)
    original_length = len(original)
    original_range = range(original_length)
    
    query = list(query)
    query_length = len(query)
    query_range = range(query_length)
    
    difference = original_length - query_length
    candidate_range = range(difference)
    
    # Modified Boyer-Moore setup
    raise Exception("FUNCTION NOT YET IMPLEMENTED")



def Candidate_Match_Position__TAIL(original, query, threshold=0,
            mode=MATCH_TYPE.ONE):
    """
    NOTE: This is an inefficient but more comprehensive function with N^2
    scaling. It is intended to be used with relatively short sequences.
    
    Return the earliest index at the tail end of the original sequence which
    might contain the query sequence.
    
    Return None if no suitable matches are found.
    
    @original
            (str - DNA Sequence)
            Needs to be the same length as @query.
    
    @query
            (str - DNA Sequence)
            Needs to be the same length as @original.
    
    @threshold
            (int)
            The maximum permissible number of matches/mismatches.
    
    @mode
            (int)
            See NSeq_Match.
    
    Candidate_Match_Position__TAIL(str, str, int, int) -> int
    Candidate_Match_Position__TAIL(str, str, int, int) -> None
    """
    length_o = len(original)
    length_q = len(query)
    subseq = original[-length_q:]
    position = Candidate_Match_Position__TAIL_EQUAL(subseq, query)
    if position == None: return None
    return length_o - length_q + position



def Candidate_Match_Position__TAIL_EQUAL(original, query, threshold=0,
            mode=MATCH_TYPE.ONE):
    """
    NOTE: This is an inefficient but more comprehensive function with N^2
    scaling. It is intended to be used with relatively short sequences.
    
    Return the earliest index at which the original sequence might contain the
    query sequence. Assumes the two sequences are the same length.
    
    Return None if no suitable matches are found.
    
    @original
            (str - DNA Sequence)
            Needs to be the same length as @query.
    
    @query
            (str - DNA Sequence)
            Needs to be the same length as @original.
    
    @threshold
            (int)
            The maximum permissible number of matches/mismatches.
    
    @mode
            (int)
            See NSeq_Match.

    Candidate_Match_Position__TAIL_EQUAL(str, str, int, int) -> int
    Candidate_Match_Position__TAIL_EQUAL(str, str, int, int) -> None
    """
    query += "-"
    length = len(original)
    range_ = range(length)
    for i in range_:
        temp_original = original[i:]
        temp_query = query[:-i-1]
        print temp_original, temp_query
        mismatches = NSeq_Match(temp_original, temp_query, mode)
        if mismatches <= threshold: return i
    return None
    


def NSeq_Search(original, query, threshold=0, mode=MATCH_TYPE.ONE):
    """
    NOTE: This is an inefficient but more comprehensive function with N^2
    scaling. It is intended to be used with relatively short sequences.
    
    Return a list of candidate positions for the [query] sequences within the
    [original] sequence. A position is a candidate position if the subsequence
    beginning at said position has [threshold] or fewer matches or mismatches.
    Whether the results are calculated based on matches or mismatches depends on
    the [mode].
    
    Return the results as a list of pairs. Each pair consists of two ints, the
    first representing a positional index and the second representing the number
    of matches/mismatches.

    @original
            (str - DNA Sequence)
    
    @query
            (str - DNA Sequence)
    
    @threshold
            (int)
            The maximum permissible number of matches/mismatches.
    
    @mode
            (int)
            An integer that determines the comparison method and the output:

                1: ONE_DIRECTIONAL_QUERY (default)
            
                    Return the number of mismatches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, but not vice versa.
        
                2: TWO_DIRECTIONAL_COMPARISON
            
                    Return the number of mismatches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, and vice versa.
        
                3: TWO_DIRECTIONAL_COMPARISON_NOT
            
                    Return the number of matches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, and vice versa.
        
                4: STRICT_MATCH
            
                    Return the number of strict matches.
        
                5: STRICT_MATCH_NOT
            
                    Return the number of mismatches and potential mismatches.
    
    NSeq_Search(str, str, int, int) -> list<[int, int]>
    """
    # Lengths and range
    length_query = len(query)
    length_original = len(original)
    length_difference = length_original - length_query
    if length_difference < 0: raise Exception(STR__query_seq_must_be_shorter)
    
    # Setup
    range_ = range(length_difference)
    temp = [0] * length_difference
    results = []
    
    # Looping through the original
    for i in range_:
        for j in range(length_query):
            temp[i] += NSeq_Match(original[i+j], query[j], mode)
    
    # Compile qualified results
    for i in range_:
        n = temp[i]
        if n <= threshold: results.append([i, n])
    
    # Return results
    return results



def NSeq_Match(original, query, mode=MATCH_TYPE.ONE):
    """
    Compare [query] string against [original] and return the number of
    matches/mismatches. The returned value is calcuated differently depending on
    [mode].
    
    Assumes [original] and [query] are the same length.
    
    @original
            (str - DNA Sequence)
    @query
            (str - DNA Sequence)
    @mode
            (int)
            An integer that determines the comparison method and the output:

                1: ONE_DIRECTIONAL_QUERY (default)
            
                    Return the number of mismatches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, but not vice versa.
        
                2: TWO_DIRECTIONAL_COMPARISON
            
                    Return the number of mismatches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, and vice versa.
        
                3: TWO_DIRECTIONAL_COMPARISON_NOT
            
                    Return the number of matches.
                    A definite [query] nucleotide will match against an
                    ambiguous [original] nucleotide, and vice versa.
        
                4: STRICT_MATCH
            
                    Return the number of strict matches.
        
                5: STRICT_MATCH_NOT
            
                    Return the number of mismatches and potential mismatches.
    
    NChar_Compare_1(str, str, int) -> int
    """
    length = len(original)
    if length != len(query): raise Exception(STR__seqs_must_be_equal_length)
    range_ = range(length)
    
    result = 0
    for i in range_: result += NChar_Compare(original[i], query[i], mode)
    
    return result



def NChar_Compare(original, query, mode):
    """
    Compare [query] char against [original]. The comparison works different
    depending on the mode:

        1: ONE_DIRECTIONAL_QUERY
            
            A definite [query] will match against an ambiguous [original] but
            not the other way around. Return 0 for a match, 1 for a mismatch.
        
        2: TWO_DIRECTIONAL_COMPARISON
            
            Both [query] and [original] are both treated as sequences with
            neither receiving priority. As long as a match is possible in
            either direction, return 0. Return 1 otherwise.
        
        3: TWO_DIRECTIONAL_COMPARISON_NOT
            
            The opposite of Option 2. Return 1 if a match is possible, return
            0 otherwise.
        
        4: STRICT_MATCH
            
            Return 0 if the [query] and [original] are identical.
            Return 1 otherwise.
        
        5: STRICT_MATCH_NOT
            
            Return 1 if the [query] and [original] are identical.
            Return 0 otherwise.
    
    NChar_Compare_1(str, str, int) -> int
    """
    if mode == MATCH_TYPE.ONE: return NChar_Compare_1(original, query)
    elif mode == MATCH_TYPE.TWO: return NChar_Compare_2(original, query)
    elif mode == MATCH_TYPE.TWO_NOT: return NChar_Compare_2N(original, query)
    elif mode == MATCH_TYPE.STRICT:
        if original == query: return 0
        return 1
    elif mode == MATCH_TYPE.STRICT_NOT:
        if original == query: return 1
        return 0
    else: raise Exception(STR__invalid_mode) # Invalid mode specified

def NChar_Compare_1(original, query):
    """
    Compare [query] char against [original] and return a 0 if [query] is a
    suitable match. Return 1 otherwise.
    
    Redundancy only applies one way. i.e.:
    A [query] of "A" would match an [original] of "N", but not vice versa.
    
    NChar_Compare_1(str, str) -> int
    """
    return DICT__n_match__1[original][query]

def NChar_Compare_2(seq1, seq2):
    """
    Compare 2 characters and return 0 if they are compatible.
    Return 1 otherwise.
    
    This match accepts 2-way nucleotide uncertainty. i.e.:
    An "A" will match with an "R" and vice versa.
    
    NChar_Compare_2(str, str) -> int
    """
    return DICT__n_match__2[seq1][seq2]

def NChar_Compare_2N(seq1, seq2):
    """
    Compare 2 characters and return 1 if they are compatible.
    Return 0 otherwise.
    
    This match accepts 2-way nucleotide uncertainty. i.e.:
    An "A" will match with an "R" and vice versa.
    
    NChar_Compare_2N(str, str) -> int
    """
    return DICT__n_match__2N[seq1][seq2]



# Controlled Print Statements ##################################################



# Main Loop ####################################################################


