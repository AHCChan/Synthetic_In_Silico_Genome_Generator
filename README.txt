
DESCRIPTION

A series of programs useful for generating a Synthetic In-Silico Genome in a
step-by-step manner.



REQUIREMENTS (SYSTEM)

This program runs in Python 2. It will not work properly with Python 3.

Please ensure you have Python 2 installed on your computer.

Please ensure you are using the correct version of Python to run this program.



REQUIREMENTS (INPUT FILES)

A featureless, bare minimum synthetic genome only requires the following input
files:

    1) A chromosome sizes file

However, a standard synthetic genome would require the following input files:

    1) A chromosome sizes file
    2) ...
    3) ...



INSTRUCTIONS (HOW TO USE)

You don't need to know how to use git to use this program. You can simply open
the Python files in your online browser and copy their contents into a local 
file on your computer with the same name.

To run the program, open up a command line window and enter one of the 
following commands (substituting the appropriate file paths) to bring up the 
relevant help doc:

    C:\Path\To\Python\python.exe C:\Path\To\The\File\Generate_Random_Chromosomes.py -h

You should get a large wall of text explaining how to use this program, along
with some examples.

Alternatively, code in these files can be used as a module by other Python 
programs using standard import methods.



INSTRUCTIONS (WORKFLOW)

1)  Generate_Random_Chromosomes.py
        
        Begin by generating synthetic chromosomes of random nucleotides based 
        on  specified chromsome sizes and nucleotide distribution settings.
        
        Alternatively, use existing chromosomal sequences.

2)  Then...



TESTING AND FEEDBACK

The files provided in the Testing_Before and Testing_After folders can be used 
as a reference for making sure the program works properly and/or for 
implementing this in another language. The Testing_Before folder contains all
the input files required to run the tests, while the Testing_After folder
contains the required input files, as well as examples of the files which
should be generated as a result of running the code in Testing_Commands.txt.

Note that due to Nucleotide sequences being randomly generated, the resulting
files will be different each run. Discretion is advised when confirming whether
or not the programs are working as intended.

Feel free to contact Angelo Chan (angelo.hoi.chung.chan@gmail.com) if you have
any questions, feedback, or bugs to report.


 