HELP_DOC = """
SISGG AUTOMATED TEST MODULE
(version 1.0)
by Angelo Chan

This is a tool designed to ensure that core functions of the SISGG package are
working correctly.

It does not test whether or not the code works from Command Line.
"""

# Define Test Function #########################################################

def SISGG_Automated_Test():
    """
    """
    # Start ####################################################################
    print("Running automated tests for SISGG package...\n")
    
    
    
    # Missing Dependencies #####################################################
    print("Checking to make sure all dependencies are present...")

    # Command Line Tools
    try:
        import _Controlled_Print as X
    except:
        print("\"_Controlled_Print\" module missing.")
        return 0
    try:
        import _Command_Line_Parser as X
    except:
        print("\"_Command_Line_Parser\" module missing.")
        return 0
    
    # File Readers
    try:
        import File_Reader as X
    except:
        print("\"File_Reader\" module missing.")
        return 0
    try:
        import Chr_FASTA_File_Reader as X
    except:
        print("\"Chr_FASTA_File_Reader\" module missing.")
        return 0
    try:
        import FASTA_File_Reader as X
    except:
        print("\"FASTA_File_Reader\" module missing.")
        return 0
    try:
        import Table_File_Reader as X
    except:
        print("\"Table_File_Reader\" module missing.")
        return 0
    
    #
    try:
        import File_Writer as X
    except:
        print("\"File_Writer\" module missing.")
        return 0
    try:
        import Width_File_Writer as X
    except:
        print("\"Width_File_Writer\" module missing.")
        return 0
    
    # Other Supporting Modules
    try:
        import Deque as X
    except:
        print("\"Deque\" module missing.")
        return 0
    try:
        import Phred as X  
    except:
        print("\"Phred\" module missing.")
        return 0
    try:
        import NSeq_Match as X
    except:
        print("\"NSeq_Match\" module missing.")
        return 0
    try:
        import ECSASS_Parser as X
    except:
        print("\"ECSASS_Parser\" module missing.")
        return 0
    
    
    
    # Missing Programs #########################################################
    print("Checking to make sure all files are present...")
    
    try:
        import Generate_Random_Chromosomes as M1
    except:
        print("\"Generate_Random_Chromosomes\" program missing.")
        return 0
    try:
        import Sequence_Extractor as M2
    except:
        print("\"Sequence_Extractor\" program missing.")
        return 0
    try:
        import Sequence_Inserter as M3
    except:
        print("\"Sequence_Inserter\" program missing.")
        return 0
    try:
        import Generate_Fragments as M4
    except:
        print("\"Generate_Fragments\" program missing.")
        return 0
    try:
        import Generate_Reads as M5
    except:
        print("\"Generate_Reads\" program missing.")
        return 0
    
    
    
    # Core Functionality #######################################################
    print("Commencing testing of core functionality...")
    
    try:
        pass
    except:
        print("\"\" function missing or error.")
        return 0
    
    
    
    # Data Validation ##########################################################
    print("Validating output...")
    
    try:
        pass
    except:
        print("\"\" data incorrect.")
        return 0
    
    
    
    # Finish ###################################################################
    print("Testing complete.")



def Compare_Files(file_1, file2):
    f1 = open(file_1, "U")
    f2 = open(file_2, "U")
    c1 = f1.read(1)
    c2 = f2.read(2)
    while c1 or c2:
        if c1 != c2:
            f1.close()
            f2.close()
            return False
        c1 = f1.read(1)
        c2 = f2.read(2)
    f1.close()
    f2.close()
    return True



# Call Test Function ###########################################################

SISGG_Automated_Test()


