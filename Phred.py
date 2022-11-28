"""
PHRED
(version 1.0)
by Angelo Chan

This is a library of data structures and values useful for working with data
which involves Phred scores.

The formula used for calculating the error rate was:
    
    Q = 10^(-P/10)
"""



# Lists ########################################################################

LIST__phred33 = ["PHRED33", "Phred33", "phred33", "P33", "p33", "33"]

LIST__phred64 = ["PHRED64", "Phred64", "phred64", "P64", "p64", "64"]



# Dictionaries #################################################################

DICT__scores_to_probs = {
0: 0, 1 : 0.205671765275719, 2: 0.369042655519807, 3: 0.498812766372728,
4: 0.601892829446503, 5: 0.683772233983162, 6: 0.748811356849042,
7: 0.800473768503112, 8: 0.841510680753889, 9: 0.874107458820583,
10: 0.900000000000000, 11: 0.920567176527572, 12: 0.936904265551981,
13: 0.949881276637273, 14: 0.960189282944650, 15: 0.968377223398316,
16: 0.974881135684904, 17: 0.980047376850311, 18: 0.984151068075389,
19: 0.987410745882058, 20: 0.990000000000000, 21: 0.992056717652757,
22: 0.993690426555198, 23: 0.994988127663727, 24: 0.996018928294465,
25: 0.996837722339832, 26: 0.997488113568490, 27: 0.998004737685031,
28: 0.998415106807539, 29: 0.998741074588206, 30: 0.999000000000000,
31: 0.999205671765276, 32: 0.999369042655520, 33: 0.999498812766373,
34: 0.999601892829446, 35: 0.999683772233983, 36: 0.999748811356849,
37: 0.999800473768503, 38: 0.999841510680754, 39: 0.999874107458821,
40: 0.999900000000000, 41: 0.999920567176528, 42: 0.999936904265552}

DICT__scores_to_chars__phred33 = {
0: '!', 1: '"', 2: '#', 3: '$', 4: '%', 5: '&', 6: "'", 7: '(', 8: ')',
9: '*', 10: '+', 11: ',', 12: '-', 13: '.', 14: '/', 15: '0', 16: '1',
17: '2', 18: '3', 19: '4', 20: '5', 21: '6', 22: '7', 23: '8', 24: '9',
25: ':', 26: ';', 27: '<', 28: '=', 29: '>', 30: '?', 31: '@', 32: 'A',
33: 'B', 34: 'C', 35: 'D', 36: 'E', 37: 'F', 38: 'G', 39: 'H', 40: 'I',
41: 'J', 42: 'K'}

DICT__scores_to_chars__phred64 = {
0: '@', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H',
9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P',
17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X',
25: 'Y', 26: 'Z', 27: '[', 28: '\\', 29: ']', 30: '^', 31: '_', 32: '`',
33: 'a', 34: 'b', 35: 'c', 36: 'd', 37: 'e', 38: 'f', 39: 'g', 40: 'h',
41: 'i', 42: 'j'}

DICT__chars_to_scores__phred33 = {
"!": 0, "\"": 1, "#": 2, "$": 3, "%": 4, "&": 5, "'": 6, "(": 7, ")": 8,
"*": 9, "+": 10, ",": 11, "-": 12, ".": 13, "/": 14, "0": 15, "1": 16,
"2": 17, "3": 18, "4": 19, "5": 20, "6": 21, "7": 22, "8": 23, "9": 24,
":": 25, ";": 26, "<": 27, "=": 28, ">": 29, "?": 30, "@": 31, "A": 32,
"B": 33, "C": 34, "D": 35, "E": 36, "F": 37, "G": 38, "H": 39, "I": 40,
"J": 41, "K": 42}

DICT__chars_to_scores__phred64 = {
"@": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
"I": 9, "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16,
"Q": 17, "R": 18, "S": 19, "T": 20, "U": 21, "V": 22, "W": 23, "X": 24,
"Y": 25, "Z": 26, "[": 27, "\\": 28, "]": 29, "^": 30, "_": 31, "`": 32,
"a": 33, "b": 34, "c": 35, "d": 36, "e": 37, "f": 38, "g": 39, "h": 40,
"i": 41, "j": 42}



# Functions ####################################################################

def Scores_To_Str(scores, phred):
    """
    Convert a list of numbers representing Phred scores, into a string of
    characters representing those scores in Phred form, using the provided phred
    dictionary.
    Return an empty string if an invalid [phred] input was given.
    
    @scores
            (list<int>)
            The list of scores/values.
    
    @phred
            (str)
            OR 
            (dict<int:str>)
            
            A string denoting the phred system to use.
            
            OR
            
            A phred dictionary the keys of which are phred scores, and the
            values of which are the corresponding chars.
    
    Scores_To_Str(list<int>, str/dict<int:str>) -> str
    """
    if type(phred) == str: return Scores_To_Str__STR(scores, phred)
    elif type(phred) == dict: return Scores_To_Str__DICT(scores, phred)
    return ""

def Scores_To_Str__STR(scores, phred):
    """
    Convert a list of numbers representing Phred scores, into a string of
    characters representing those scores in Phred form. The Phred system to be
    used is specified by the [phred] string.
    Return an empty string if an invalid string was used for [phred].
    
    @scores
            (list<int>)
            The list of scores/values.
    
    @phred
            (str)
            A string denoting the phred system to use.
    
    Scores_To_Str(list<int>, str) -> str
    """
    if phred in LIST__phred33:
        return Scores_To_Str__DICT(scores, DICT__scores_to_chars__phred33)
    elif phred in LIST__phred64:
        return Scores_To_Str__DICT(scores, DICT__scores_to_chars__phred64)
    return ""

def Scores_To_Str__DICT(scores, phred_dict):
    """
    Convert a list of numbers representing Phred scores, into a string of
    characters representing those scores in Phred form, using the provided phred
    dictionary.
    
    @scores
            (list<int>)
            The list of scores/values.
    
    @phred
            (dict<int:str>)
            A phred dictionary the keys of which are phred scores, and the
            values of which are the corresponding chars.
    
    Scores_To_Str(list<int>, dict<int:str>) -> str
    """
    sb = ""
    for i in scores:
        char = phred_dict[i]
        sb += char
    return sb


