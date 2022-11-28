"""
FASTA FILE READER
(version 1.0)
by Angelo Chan

This module contains a Class capable of reading and interpretting FASTA files.
"""

# Imported Modules #############################################################

from File_Reader import *



# Lists ########################################################################

LIST__nucleotide_chars = ["A", "C", "G", "T", "a", "c", "g", "t", "N", "n"]



# Classes ######################################################################

class FASTA_Reader(File_Reader):
    """
    The FASTA Reader is a file reader designed to work with FASTA files.

    Designed for the following use:
    
    f = FASTA_Reader()
    f.Open("F:/Filepath.fa")
    while not f.End():
        f.Read()
        # Your code - You may access buffered elements in f
    f.Close()
    """
    
    # Minor Configurations #####################################################
    
    empty_element = ["", "", ""]
    
    # Minor Configurations #####################################################
    
    _CONFIG__print_errors = True
    _CONFIG__print_progress = False
    _CONFIG__print_metrics = True
    
    
    
    # Strings ##################################################################
    
    _MSG__object_type = "FASTA File Reader"
    _MSG__units_of_measure = "Sequences"
    
    # Constructor & Destructor #################################################
    
    def __init__(self, file_path="", auto_open=False):
        """
    `   Creates a Chromsome FASTA File Reader object. The filepath will be
        tested if a filepath is supplied.
        """
        File_Reader.__init__(self, file_path, auto_open)
    
    
    
    # Property Methods #########################################################
        
    def Get_Name(self):
        """
        Return the name of the current sequence.
        """
        return self.current_element[0]
    
    def Get_Anno(self):
        """
        Return the annotation of the current sequence.
        """
        return self.current_element[1]
    
    def Get_Seq(self):
        """
        Return the nucleotide sequence of the current sequence.
        """
        return self.current_element[2]
    
    def Copy_Element(self, element):
        """
        Return a copy of the current element.
        """
        return list(element)
    
    def Get_Size(self):
        """
        Return the number of sequences in the FASTA file.
        
        Return -1 if no filepath has been set.
        """
        if self.file_path:
            count = 0
            f = open(self.file_path, "U")
            line = f.readline()
            while line:
                if line[0] == ">": count += 1
                line = f.readline()
            f.close()
            return count
        return -1
    
    
    
    # File I/O Methods #########################################################
    
    # File Reading Methods #####################################################
    
    def _read(self):
        """
        Read in the next element.
        
        Unlike the standard File Reader base class, the next element is not
        fully ready at the start of a read operation. Each read action only
        reads up until the first line of the next element. The name of the read
        and the annotations are stored, since they are found on the first line,
        denoted by ">", but the sequence is not.
        
        In essence, each read action reads in the nucleotide sequence of the
        current element, and the name and annotations of the next element.
        
        Flat files with an indeterminate number of lines per entry, like FASTA
        files, are what the original File_Reader base class were designed to
        account for with its "next" buffer.
        """
        self.current_index += 1
        # Current seq
        sb = ""
        line = self.file.readline()
        while line and line[0] != ">":
            if line[-1] in LIST__newline: line = line[:-1]
            sb += line
            line = self.file.readline()
        # Slide
        self.next_element.append(sb)        
        self.current_element = self.next_element
        # Next element
        if line and line[-1] in LIST__newline: line = line[:-1]
        if line:
            values = line.split(" ", 1)
            values[0] = values[0][1:]
            self.next_element = values
            if len(self.next_element) == 1: self.next_element.append("")
        else: # EOF
            self.EOF = True
            self.printP(self._MSG__EOF_reached)
    
    def Is_Empty_Element(self, element):
        """
        Return True if [element] is an "empty" element.
        
        Return False otherwise.
        """
        for s in element:
            if s != "": return False
        return True


