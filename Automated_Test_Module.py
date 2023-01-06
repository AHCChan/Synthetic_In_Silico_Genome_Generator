HELP_DOC = """
SISGG AUTOMATED TEST MODULE
(version 1.0)
by Angelo Chan

This is a tool designed to ensure that core functions of the SISGG package are
working correctly.

It does not test whether or not the code works from Command Line.
"""

import os

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
        import _Controlled_Print as PRINT
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
        M1.WRITE_PREVENT = False
        M1.WRITE_CONFIRM = False
    except:
        print("\"Generate_Random_Chromosomes\" program missing.")
        return 0
    try:
        import Generate_Fragments as M2
        M2.WRITE_PREVENT = False
        M2.WRITE_CONFIRM = False
    except:
        print("\"Generate_Fragments\" program missing.")
        return 0
    try:
        import Generate_Reads as M3
        M3.WRITE_PREVENT = False
        M3.WRITE_CONFIRM = False
    except:
        print("\"Generate_Reads\" program missing.")
        return 0
    try:
        import Sequence_Extractor as M4
        M4.WRITE_PREVENT = False
        M4.WRITE_CONFIRM = False
    except:
        print("\"Sequence_Extractor\" program missing.")
        return 0
    try:
        import Sequence_Inserter as M5
        M5.WRITE_PREVENT = False
        M5.WRITE_CONFIRM = False
    except:
        print("\"Sequence_Inserter\" program missing.")
        return 0

    # Override Print Settings ##################################################
    
    M1.PRINT.PRINT_ERRORS = False   # All modules import the same "PRINT"
    M1.PRINT.PRINT_PROGRESS = False # ... so the print settings are reflected
    M1.PRINT.PRINT_METRICS = False  # ... between all of them
    
    
    
    # Core Functionality #######################################################
    print("Commencing testing of core functionality...")
    
    count_total = 0
    count_passed = 0
    count_failed = 0
    count_uncaught = 0 
    
    
    
    #############################
    #
    # Generate Random Chromosomes
    #
    #############################
    
    print("\tTesting \"Parse_Command_Line_Input__Generate_Synthetic_Genome\":")
    try: # Minimal parameters
        count_total += 1
        test_name = "minimal input parameters"
        exit_code = M1.Parse_Command_Line_Input__Generate_Synthetic_Genome([
                "python",
                "..\\Generate_Random_Chromosomes.py",
                "Testing_Auto\\Input_01__Chromosome_Sizes.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file
        count_total += 1
        test_name = "invalid input file"
        exit_code = M1.Parse_Command_Line_Input__Generate_Synthetic_Genome([
                "python",
                "..\\Generate_Random_Chromosomes.py",
                "Testing_Auto\\404.tsv"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Output specified
        count_total += 1
        test_name = "output filepath specified"
        exit_code = M1.Parse_Command_Line_Input__Generate_Synthetic_Genome([
                "python",
                "..\\Generate_Random_Chromosomes.py",
                "Testing_Auto\\Input_01__Chromosome_Sizes.tsv",
                "-o",
                "Testing_Auto\\Output_02__Random_Genome"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    
    
    
    ####################
    #
    # Generate Fragments
    #
    ####################
    
    print("\tTesting \"Parse_Command_Line_Input__Generate_Fragments\":")
    try: # Minimal parameters
        count_total += 1
        test_name = "minimal input parameters"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file
        count_total += 1
        test_name = "invalid input file"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\404.tsv"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Output specified
        count_total += 1
        test_name = "output filepath specified"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-o",
                "Testing_Auto\\Output_04__Fragments__DEFAULT.fa"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # All parameters used
        count_total += 1
        test_name = "all parameters specified"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-d", "10",
                "-c", "N", "2",
                "-r", "150",
                "-l", "500",
                "-f", "N", "500",
                "-u", "XXX"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - All parameters invalid
        count_total += 1
        test_name = "all parameters invalid"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-d", "A",
                "-c", "A", "A",
                "-r", "A",
                "-l", "A",
                "-f", "A", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid flag
        count_total += 1
        test_name = "invalid flag"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-z", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid depth
        count_total += 1
        test_name = "invalid depth"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-d", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid coverage type
        count_total += 1
        test_name = "invalid coverage type"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-c", "A", "2"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid coverage
        count_total += 1
        test_name = "invalid coverage"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-c", "N", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid read length
        count_total += 1
        test_name = "invalid read length"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-r", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid fragment length
        count_total += 1
        test_name = "invalid fragment length"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-l", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid fragment size distribution type
        count_total += 1
        test_name = "invalid size distribution type"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-f", "A", "500"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid fragment size distribution
        count_total += 1
        test_name = "invalid size distribution"
        exit_code = M2.Parse_Command_Line_Input__Generate_Fragments([
                "python",
                "..\\Generate_Fragments.py",
                "Testing_Auto\\Input_02__Genome",
                "-f", "N", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    
    
    
    ################
    #
    # Generate Reads
    #
    ################
    
    print("\tTesting \"Parse_Command_Line_Input__Generate_Reads\":")
    try: # Minimal parameters
        count_total += 1
        test_name = "minimal input parameters"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file
        count_total += 1
        test_name = "invalid input file"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\404.fa"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Output specified
        count_total += 1
        test_name = "output filepath specified"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-o",
                "Testing_Auto\\Output_05__Reads_r1.fa",
                "Testing_Auto\\Output_05__Reads_r2.fa"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # All parameters used
        count_total += 1
        test_name = "all parameters specified"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-r", "75", "75",
                "-p", "phred64",
                "-q", "30", "U", "5",
                "-d", "5", "N", "2",
                "-m", "0", "5",
                "-t", "0", "N", "2",
                "-x", "16",
                "-u", "XXX"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - All parameters invalid
        count_total += 1
        test_name = "all parameters invalid"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-r", "A", "A",
                "-p", "A",
                "-q", "A", "A", "A",
                "-d", "A", "A", "A",
                "-m", "A", "A",
                "-t", "A", "A", "A",
                "-x", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid flag
        count_total += 1
        test_name = "invalid flag"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-a", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid read length 1
        count_total += 1
        test_name = "invalid read length 1"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-r", "A", "75"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid read length 2
        count_total += 1
        test_name = "invalid read length 2"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-r", "75", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid phred
        count_total += 1
        test_name = "invalid phred"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-p", "phred1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid quality
        count_total += 1
        test_name = "invalid quality"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "A", "N", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid quality - gamma distribution
        count_total += 1
        test_name = "invalid quality - gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "0", "G", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid quality type
        count_total += 1
        test_name = "invalid quality type"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "A", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid quality - normal distribution
        count_total += 1
        test_name = "valid quality: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "N", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid quality - uniform distribution
        count_total += 1
        test_name = "valid quality: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "U", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid quality - gamma distribution
        count_total += 1
        test_name = "valid quality: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "G", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in quality (normal distribution)
        count_total += 1
        test_name = "invalid standard deviation,\n\t\t\t"\
                "quality: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "N", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in quality (uniform distribution)
        count_total += 1
        test_name = "invalid max distance from mean,\n\t\t\t"\
                "quality: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "U", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid alpha value in quality (gamma distribution)
        count_total += 1
        test_name = "invalid alpha value,\n\t\t\t"\
                "quality: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-q", "30", "G", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid duplicates
        count_total += 1
        test_name = "invalid duplicates"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "A", "N", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid duplicates - gamma distribution
        count_total += 1
        test_name = "invalid duplicates - gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "0", "G", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid duplicates type
        count_total += 1
        test_name = "invalid duplicates type"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "A", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid duplicates - normal distribution
        count_total += 1
        test_name = "valid duplicates: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "N", "1"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid duplicates - uniform distribution
        count_total += 1
        test_name = "valid duplicates: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "U", "1"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid duplicates - gamma distribution
        count_total += 1
        test_name = "valid duplicates: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "G", "1"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in dupes (normal distribution)
        count_total += 1
        test_name = "invalid standard deviation,\n\t\t\t"\
                "duplicates: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "N", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in dupes (uniform distribution)
        count_total += 1
        test_name = "invalid max distance from mean,\n\t\t\t"\
                "duplicates: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "U", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid alpha value in dupes (gamma distribution)
        count_total += 1
        test_name = "invalid alpha value,\n\t\t\t"\
                "duplicates: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-d", "2", "G", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid min duplicates
        count_total += 1
        test_name = "invalid min duplicates"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-m", "A", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid max duplicates
        count_total += 1
        test_name = "invalid max duplicates"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-m", "0", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Min greater than max
        count_total += 1
        test_name = "min duplicates greater than max duplicates"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-m", "5", "0"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid truncation
        count_total += 1
        test_name = "invalid truncation"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "A", "N", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid truncation - gamma distribution
        count_total += 1
        test_name = "invalid truncation - gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "G", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid truncation type
        count_total += 1
        test_name = "invalid truncation type"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "A", "5"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid truncation - normal distribution
        count_total += 1
        test_name = "valid truncation: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "N", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid truncation - uniform distribution
        count_total += 1
        test_name = "valid truncation: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "U", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Valid truncation - gamma distribution
        count_total += 1
        test_name = "valid truncation: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "1", "G", "5"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except Exception, e:
        print e
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in trunc (normal distribution)
        count_total += 1
        test_name = "invalid standard deviation,\n\t\t\t"\
                "truncation: normal distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "N", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid standard deviation in trunc (uniform distribution)
        count_total += 1
        test_name = "invalid max distance from mean,\n\t\t\t"\
                "truncation: uniform distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "0", "U", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid alpha value in trunc (gamma distribution)
        count_total += 1
        test_name = "invalid alpha value,\n\t\t\t"\
                "truncation: gamma distribution"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-t", "1", "G", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid threads
        count_total += 1
        test_name = "invalid threads"
        exit_code = M3.Parse_Command_Line_Input__Generate_Reads([
                "python",
                "..\\Generate_Reads.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-x", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    
    
    
    ####################
    #
    # Sequence Extractor
    #
    ####################
    
    print("\tTesting \"Parse_Command_Line_Input__Extract_Sequences\":")
    try: # Minimal parameters
        count_total += 1
        test_name = "minimal input parameters"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input files 1
        count_total += 1
        test_name = "invalid input files 1"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\404",
                "Testing_Auto\\Input_05__Coords_Table.tsv"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input files 2
        count_total += 1
        test_name = "invalid input files 2"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\404.tsv"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Insufficient outputs specified
        count_total += 1
        test_name = "insufficient outputs specified"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv",
                "-o",
                "Testing_Auto\\Output_06__Genome"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Output specified
        count_total += 1
        test_name = "output filepath specified"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv",
                "-o",
                "Testing_Auto\\Output_06__Genome__Post_Excision",
                "Testing_Auto\\Output_07__Extracted_Sequences",
                "Testing_Auto\\Output_08__Coords_Table.tsv",
                "Testing_Auto\\Output_09__Chromosome_Sizes.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Duplicate overlaps yes
        count_total += 1
        test_name = "duplicate overlaps yes"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv",
                "-d", "Y",
                "-o",
                "Testing_Auto\\Output_10__Genome__Post_Excision",
                "Testing_Auto\\Output_11__Extracted_Sequences",
                "Testing_Auto\\Output_12__Coords_Table.tsv",
                "Testing_Auto\\Output_13__Chromosome_Sizes.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Duplicate overlaps no
        count_total += 1
        test_name = "duplicate overlaps no"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv",
                "-d", "N",
                "-o",
                "Testing_Auto\\Output_14__Genome__Post_Excision",
                "Testing_Auto\\Output_15__Extracted_Sequences",
                "Testing_Auto\\Output_16__Coords_Table.tsv",
                "Testing_Auto\\Output_17__Chromosome_Sizes.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Duplicate overlaps invalid
        count_total += 1
        test_name = "duplicate overlaps invalid"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_04__Genome",
                "Testing_Auto\\Input_05__Coords_Table.tsv",
                "-d", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid flag
        count_total += 1
        test_name = "invalid flag"
        exit_code = M4.Parse_Command_Line_Input__Extract_Sequences([
                "python",
                "..\\Sequence_Extractor.py",
                "Testing_Auto\\Input_03__Fragments.fa",
                "-a", "Y"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    
    
    
    ###################
    #
    # Sequence Inserter
    #
    ###################
    
    print("\tTesting \"Parse_Command_Line_Input__Insert_Sequences\":")
    try: # Minimal parameters
        count_total += 1
        test_name = "minimal input parameters"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file 1
        count_total += 1
        test_name = "invalid input path 1"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\404",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file 2
        count_total += 1
        test_name = "invalid input path 2"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\404.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file 3
        count_total += 1
        test_name = "invalid input path 3"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\404"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid input file
        count_total += 1
        test_name = "empty sequences folder"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_09__Empty_Folder"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Output specified
        count_total += 1
        test_name = "output filepath specified"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences",
                "-o",
                "Testing_Auto\\Output_18__Genome__Post_Insertion",
                "Testing_Auto\\Output_19__Coords_Table.tsv",
                "Testing_Auto\\Output_20__Chromosome_Sizes.tsv"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # All parameters used
        count_total += 1
        test_name = "all parameters specified"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences",
                "-a", "6", "10", "1", "N",
                "-m", "Y"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - All parameters invalid
        count_total += 1
        test_name = "all parameters invalid"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences",
                "-a", "A", "A", "A", "A",
                "-m", "A"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Inserted nucleotides masked
        count_total += 1
        test_name = "inserted nucleotides masked"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences",
                "-o",
                "Testing_Auto\\Output_21__Genome__Post_Insertion",
                "Testing_Auto\\Output_22__Coords_Table.tsv",
                "Testing_Auto\\Output_23__Chromosome_Sizes.tsv",
                "-m", "Y"])
        if exit_code != 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tCAUGHT ERROR")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    try: # Error - Invalid flag
        count_total += 1
        test_name = "invalid flag"
        exit_code = M5.Parse_Command_Line_Input__Insert_Sequences([
                "python",
                "..\\Sequence_Inserter.py",
                "Testing_Auto\\Input_06__Genome__Post_Excision",
                "Testing_Auto\\Input_07__Coords_Table.tsv",
                "Testing_Auto\\Input_08__Extracted_Sequences",
                "-a", "1"])
        if exit_code == 0:
            print("\t*\tFAILED: " + test_name + "\n\t\t\tERROR NOT THROWN")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tUNCAUGHT ERROR")
        count_uncaught += 1
    
    
    
    # Data Validation ##########################################################
    print("Validating output...")
    
    # Sequence extractor - duplicate overlaps
    try:
        count_total += 1
        test_name = "sequence extractor - duplicate overlaps"
        os.listdir("Testing_Auto\\Output_10__Genome__Post_Excision")
        os.listdir("Testing_Auto\\Output_11__Extracted_Sequences")
        f = open("Testing_Auto\\Output_12__Coords_Table.tsv", "U")
        f.close()
        f = open("Testing_Auto\\Output_13__Chromosome_Sizes.tsv", "U")
        f.close()
        if (Compare_Folders("Testing_Auto\\Output_10__Genome__Post_Excision",
                "Testing_Auto\\Benchmark_10__Genome__Post_Excision") and
                Compare_Folders("Testing_Auto\\Output_11__Extracted_Sequences",
                "Testing_Auto\\Benchmark_11__Extracted_Sequences") and
                Compare_Files("Testing_Auto\\Output_12__Coords_Table.tsv",
                "Testing_Auto\\Benchmark_12__Coords_Table.tsv") and
                Compare_Files("Testing_Auto\\Output_13__Chromosome_Sizes.tsv",
                "Testing_Auto\\Benchmark_13__Chromosome_Sizes.tsv")):
            print("\t*\tFAILED: " + test_name +
                    "\n\t\t\tOUTPUT DOES NOT MATCH MODEL ANSWER")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tFILES NOT GENERATED")
        count_failed += 1
    # Sequence extractor - do not duplicate overlaps
    try:
        count_total += 1
        test_name = "sequence extractor - do notduplicate overlaps"
        os.listdir("Testing_Auto\\Output_14__Genome__Post_Excision")
        os.listdir("Testing_Auto\\Output_15__Extracted_Sequences")
        f = open("Testing_Auto\\Output_16__Coords_Table.tsv", "U")
        f.close()
        f = open("Testing_Auto\\Output_17__Chromosome_Sizes.tsv", "U")
        f.close()
        if (Compare_Folders("Testing_Auto\\Output_14__Genome__Post_Excision",
                "Testing_Auto\\Benchmark_14__Genome__Post_Excision") and
                Compare_Folders("Testing_Auto\\Output_15__Extracted_Sequences",
                "Testing_Auto\\Benchmark_15__Extracted_Sequences") and
                Compare_Files("Testing_Auto\\Output_16__Coords_Table.tsv",
                "Testing_Auto\\Benchmark_16__Coords_Table.tsv") and
                Compare_Files("Testing_Auto\\Output_17__Chromosome_Sizes.tsv",
                "Testing_Auto\\Benchmark_17__Chromosome_Sizes.tsv")):
            print("\t*\tFAILED: " + test_name +
                    "\n\t\t\tOUTPUT DOES NOT MATCH MODEL ANSWER")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tFILES NOT GENERATED")
        count_failed += 1
    # Sequence inserter
    try:
        count_total += 1
        test_name = "sequence inserter"
        os.listdir("Testing_Auto\\Output_18__Genome__Post_Insertion")
        f = open("Testing_Auto\\Output_19__Coords_Table.tsv", "U")
        f.close()
        f = open("Testing_Auto\\Output_20__Chromosome_Sizes.tsv", "U")
        f.close()
        if (Compare_Folders("Testing_Auto\\Output_18__Genome__Post_Insertion",
                "Testing_Auto\\Benchmark_18__Genome__Post_Insertion") and
                Compare_Files("Testing_Auto\\Output_19__Coords_Table.tsv",
                "Testing_Auto\\Benchmark_19__Coords_Table.tsv") and
                Compare_Files("Testing_Auto\\Output_20__Chromosome_Sizes.tsv",
                "Testing_Auto\\Benchmark_20__Chromosome_Sizes.tsv")):
            print("\t*\tFAILED: " + test_name +
                    "\n\t\t\tOUTPUT DOES NOT MATCH MODEL ANSWER")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tFILES NOT GENERATED")
        count_failed += 1
    # Sequence inserter
    try:
        count_total += 1
        test_name = "sequence inserter - masked"
        os.listdir("Testing_Auto\\Output_21__Genome__Post_Insertion")
        f = open("Testing_Auto\\Output_22__Coords_Table.tsv", "U")
        f.close()
        f = open("Testing_Auto\\Output_23__Chromosome_Sizes.tsv", "U")
        f.close()
        if (Compare_Folders("Testing_Auto\\Output_21__Genome__Post_Insertion",
                "Testing_Auto\\Benchmark_21__Genome__Post_Insertion") and
                Compare_Files("Testing_Auto\\Output_22__Coords_Table.tsv",
                "Testing_Auto\\Benchmark_22__Coords_Table.tsv") and
                Compare_Files("Testing_Auto\\Output_23__Chromosome_Sizes.tsv",
                "Testing_Auto\\Benchmark_23__Chromosome_Sizes.tsv")):
            print("\t*\tFAILED: " + test_name +
                    "\n\t\t\tOUTPUT DOES NOT MATCH MODEL ANSWER")
            count_failed += 1
        else:
            print("\t\tPASSED: " + test_name)
            count_passed += 1
    except:
        print("\t*\tFAILED: " + test_name + "\n\t\t\tFILES NOT GENERATED")
        count_failed += 1
    
    
    
    # Finish ###################################################################
    print("\nTesting results:")
    print("    Total tests run: " + str(count_total))
    print("             Passed: " + str(count_passed))
    print("             Failed: " + str(count_failed))
    print("     Uncaught error: " + str(count_uncaught))
    print("\nTesting complete.")



def Compare_Files(file_1, file_2):
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

def Compare_Folders(folder_1, folder_2):
    list1 = os.listdir(folder_1)
    list2 = os.listdir(folder_2)
    list1 = sorted(list1)
    list2 = sorted(list2)
    if list1 != list2: return False
    else:
        for filename in list1:
            path_1 = folder_1 + "\\" + filename
            path_2 = folder_2 + "\\" + filename
            if not Compare_Files(path_1, path_2): return False
    return True



# Call Test Function ###########################################################

SISGG_Automated_Test()


