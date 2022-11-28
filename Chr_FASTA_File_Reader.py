"""
CHROMOSOME FASTA FILE READER
(version 1.0)
by Angelo Chan

This module contains a Class capable of reading and interpretting FASTA files
which contain a single Chromosome.
"""

# Imported Modules #############################################################

from File_Reader import *



# Lists ########################################################################

LIST__nucleotide_chars = ["A", "C", "G", "T", "a", "c", "g", "t", "N", "n"]



# Classes ######################################################################

class Chr_FASTA_Reader(File_Reader):
    """
    The Chromosome FASTA Reader is a file reader designed specifically to work
    with FASTA files which contain a single Chromosome.

    Designed for the following use:
    
    f = Chr_File_Reader()
    f.Open("F:/Filepath.fa")
    while not f.End():
        f.Read()
        # Your code - You may access buffered elements in f
    f.Close()
    """
    
    # Minor Configurations #####################################################
    
    empty_element = ""
    
    # Minor Configurations #####################################################
    
    _CONFIG__print_errors = True
    _CONFIG__print_progress = False
    _CONFIG__print_metrics = True
    
    
    
    # Strings ##################################################################
    
    _MSG__object_type = "Chromosome FASTA File Reader"
    _MSG__units_of_measure = "Nucleotides"
    
    # Constructor & Destructor #################################################
    
    def __init__(self, file_path="", auto_open=False):
        """
    `   Creates a Chromsome FASTA File Reader object. The filepath will be
        tested if a filepath is supplied.
        """
        self.name = ""
        File_Reader.__init__(self, file_path, auto_open)
    
    
    
    # Property Methods #########################################################
    
    def Get_Name(self):
        """
        Return the name of the chromosome in the current file.
        """
        return self.name
    
    def Copy_Element(self, element):
        """
        (Strings do not require a special copy method)
        """
        return element
    
    def Get_Size(self):
        """
        Return the size of the chromosome in the FASTA file.
        
        Return -1 if no filepath has been set.
        """
        if self.file_path:
            count = 0
            f = open(self.file_path, "U")
            f.readline()
            char = f.read(1)
            while char:
                if char in LIST__nucleotide_chars: count += 1
                char = f.read(1)
            f.close()
            return count
        return -1
    
    
    
    # File I/O Methods #########################################################
    
    # File Reading Methods #####################################################
    
    def Read_Header(self):
        """
        Read in the first line of the file and get the name of the chromosome.
        """
        line = self.file.readline()
        if line[0] == ">": line = line[1:]
        if line[-1] in LIST__newline: line = line[:-1]
        values = line.split(" ")
        self.name = values[0]
    
    def _get_next_element(self):
        """
        Read up to the next nucleotide character and return it.
        
        Return an empty string if the end of the file has been reached.
        """
        char = self.file.read(1)
        while char and char not in LIST__nucleotide_chars:
            char = self.file.read(1)
        return char
    
    def Is_Empty_Element(self, element):
        """
        Return True if [element] is an "empty" element, that is to say, an empty
        string.
        
        Return False otherwise.
        """
        if element == self.empty_element:
            return True
        return False


