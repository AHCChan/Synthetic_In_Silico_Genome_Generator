HELP_DOC = """
READ GENERATOR
(version 1.0)
by Angelo Chan

This is a program for generating DNA sequencing read data from DNA sequences.

It is designed to be paired up the Fragment Generator from this (Synthetic
In-Silico Genome Generator) library, which imitates the DNA fragmentation
process, and mimicks the NGS DNA sequencing process.



USAGE:
    
    python27 Generate_Reads.py <input_filepath> [-o <output_filepath_r1>
            <output_filepath_r2>] [-r <read_1_len> <read_2_len>] [-p <phred>]
            [-q <avg_quality> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-d
            <avg_duplicates> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-m
            <min_duplicates> <max_duplicates>] [-t <avg_truncation> N|G|U
            <stdev>|<alpha_mod>|<max_dist>] [-x <threads>] [-u <unique_id_mod>]



MANDATORY:
    
    input_folder
        
        The filepath of the input folder containing the FASTA file from which
        the DNA reads will be generated.

OPTIONAL:
    
    output_filepath_r1
        
        (DEFAULT path generation available)
        
        The filepath of the output file where resultant forward reads will be
        output into.
    
    output_filepath_r1
        
        (DEFAULT path generation available)
        
        The filepath of the output file where resultant reverse reads will be
        output into.
    
    read_1_len
        
        (DEFAULT: 75)
        
        The read length of the forward reads. i.e. The first @read_1_len
        nucleotides of the fragment will be output into a read.
    
    read_2_len
        
        (DEFAULT: 75)
        
        The read length of the reverse reads. i.e. The complement of the last
        @read_2_len nucleotides of the fragment will be output into a read.
        
        Set to 0 for Single-End sequencing.
    
    phred
        
        (DEFAULT: phred33)
        
        The phred system for denoting the quality scores of each nucleotide.
    
    avg_quality
        
        (DEFAULT: 0)
        
        The average quality score (phred score), for the resulting reads. The
        lower the score, the higher the error rate when transcribing fragments
        to reads.
        Specifying 0 will give perfect reads.
    
    avg_duplicates
        
        (DEFAULT: 1)
        The average number of duplicate reads or read pairs per fragment.
    
    min_duplicates
        
        (DEFAULT: 1)
        The minimum number of duplicate reads or read pairs per fragment.
    
    max_duplicates
        
        (DEFAULT: 1)
        The maximum number of duplicate reads or read pairs per fragment.
    
    avg_truncation
        
        (DEFAULT: 0)
        The average number of nucleotides truncated off the ends of the reads.
    
    N|G|U
        
        (DEFAULT (-q): N)
        (DEFAULT (-d): G)
        (DEFAULT (-t): N)
        
        The probability distribution used to determine random values for things
        like phred scores, duplicate copy number and truncation length.
            
            N   Normal variate distribution
            G   Gama variate distribution
            U   Uniform distribution
    
    stdev
        
        (Only applies if a Normal Variate distribution was specified)
        (DEFAULT (-q): 5)
        (DEFAULT (-t): 0)
        
        The standard deviation of the normal distribution.
    
    alpha_mod
        
        (Only applies if a Gamma Variate distribution was specified)
        (DEFAULT (-d): 1)
        
        The skewness factor of the Gamma distribution.
        
        The magnitude of @alpha_mod determines how unskewed the distribution is.
        As @alpha_mod approaches infinity, the resulting gamma distribution will
        begin to resemble a normal distribution. As @alpha approaches 0, the
        resulting gamma distribution will become increasingly skewed.
        
        It is known that, for a Gamma Distribution:
            
            Alpha * Beta ~= Desired_Average
        
        The Beta is automatically calculated such that:
            
            Alpha = Beta * Alpha_Mod
        
    max_dist
        
        (Only applies if a Uniform distribution was specified)
        
        The furthest away from the specified average which a randomly generated
        value can be.
        
    threads
        
        (DEFAULT: 1)
        
        (Multithreading is not yet implemented. This is a placeholder.)
        The number of threads to use.
    
    unique_id_mod
    
        (DEFAULT: (None))
        
        A string prefix which forms part of the fragment ID. Allows reads from
        different runs to be pooled together and still have unique IDs relative
        to each other.

CONTEXTUAL FLAGS:
(For specifying probability distribution parameters)
    
    (-q)
        
        Used to signify that the following parameters pertain to the probability
        distribution of quality scores.
    
    (-d)
        
        Used to signify that the following parameters pertain to the probability
        distribution of duplicate copy numbers.
    
    (-t)
        
        Used to signify that the following parameters pertain to the probability
        distribution of truncation length.



EXAMPLES SCENARIO EXPLANATION:
    
    1:
    A bare minimum use case. (All options use defaults)
    
    2:
    Flawlessly accurate sequencing.
    
    3:
    Some truncation occurs.
    
    4:
    All fragments generate 1-5 duplicates, with the duplicate count uniformly
    distributed.
    
    5:
    Single-end, 75bp sequencing.

EXAMPLES:
    
    python27 Generate_Reads.py Path/Input_Frags.fa
    
    python27 Generate_Reads.py Path/Input_Frags.fa -q 0 N 0
    
    python27 Generate_Reads.py Path/Input_Frags.fa -t 2 G 0.01
    
    python27 Generate_Reads.py Path/Input_Frags.fa -d 3 U 2 -m 1 5
    
    python27 Generate_Reads.py Path/Input_Frags.fa -r 75 0

USAGE:
    
    python27 Generate_Reads.py <input_filepath> [-o <output_filepath_r1>
            <output_filepath_r2>] [-r <read_1_len> <read_2_len>] [-p <phred>]
            [-q <avg_quality> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-d
            <avg_duplicates> N|G|U <stdev>|<alpha_mod>|<max_dist>] [-m
            <min_duplicates> <max_duplicates>] [-t <avg_truncation> N|G|U
            <stdev>|<alpha_mod>|<max_dist>] [-x <threads>] [-u <unique_id_mod>]
"""

NAME = "Generate_Reads.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

FILEMOD__FASTQ_1 = "__READS_r1.fq"
FILEMOD__FASTQ_2 = "__READS_r2.fq"

# For name string
DEFAULT__STR__unique_id_mod = ""
COPY_DIGITS = 3
STR__forward = "__r1"
STR__reverse = "__r2"

PRINT_INTERVAL = 10000



# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__phred = "phred33"
    
DEFAULT__read_1_len = 75
DEFAULT__read_2_len = 75

DEFAULT__avg_quality = 20
DEFAULT__quality_dist = 1 # DIST.NORMAL = 1. Alter if the DIST enum is altered
DEFAULT__quality_param = 5

DEFAULT__avg_dupes = 1
DEFAULT__dupes_dist = 2 # DIST.GAMMA = 2. Alter if the DIST enum is altered
DEFAULT__dupes_param = 5
DEFAULT__min_dupes = 1
DEFAULT__max_dupes = 1

DEFAULT__avg_trunc = 0
DEFAULT__trunc_dist = 1 # DIST.NORMAL = 1. Alter if the DIST enum is altered
DEFAULT__trunc_param = 0

DEFAULT__threads = 1



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
from _Command_Line_Parser import *

from NSeq_Match import *
from Phred import *

from FASTA_File_Reader import *



# Enums ########################################################################

class DIST: # For Distribution
    NORMAL=1 # If this is changed, sync relevant defaults
    GAMMA=2
    UNIFORM=3



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Generate_Reads.py -h"



STR__invalid_lengths = """
ERROR: Invalid read lengths:
    {s1}
    {s2}
Please specify non-negative integers, at least one of which should also be
non-zero."""

STR__invalid_phred = """
ERROR: Invalid phred system specified:
    {s}
Please specify either "phred33" or "phred64"."""

STR__invalid_min_dupe = """
ERROR: Invalid minimum number of duplicates: {s}
Please specify a non-negative integer."""
STR__invalid_max_dupe = """
ERROR: Invalid maximum number of duplicates: {s}
Please specify a positivee integer."""

STR__invalid_avg = """
ERROR: Invalid {s} average: {m}
Please specify a number."""
STR__invalid_params = """
ERROR: Invalid {s} statistical distribution parameters:
    (Distribution): {d}
    (Parameter):    {p}

For the distribution model, please specify one of:
    NORMAL
    GAMMA
    UNIFORM

For the parameter, depending on the distribution model chosen, please specify:
    NORMAL - A non-negative number.
    GAMMA - A non-zero number.
    UNIFORM - A non-negative integer."""

STR__invalid_threads = """
ERROR: Invalid number of threads specified: {s}
Please specify a positive integer."""



STR__input_invalid = "\nERROR: An unexpected error occured when reading from "\
        "the input file."
STR__output_invalid = "\nERROR: An unexpected error occured when writing to "\
        "the output file."
STR__generation_invalid = "\nERROR: An unexpected error occured during the "\
        "fragment generation process."



STR__metrics = """
      Total fragments processed: {F}
          Total reads generated: {R}

    Average forward read length: {L1}
        Average errors per read: {E1}

    Average reverse read length: {L2}
        Average errors per read: {E2}

          Average quality score: {Q}
        Average duplicate count: {D}
"""

STR__GenReads_begin = "\nRunning Generate_Reads..."

STR__GenReads_complete = "\nGenerate_Reads successfully finished."



# String Lists #################################################################

STR_LIST__specify_dist_param = [ # Indexes are based on the DIST enum
"""
ERROR: Please specify the standard deviation you want your normal distribution
to have. The standard deviations must be a positive number.""","""
ERROR: Please specify the alpha you want your gamma distribution to have. If the
alpha ius negative, a flipped and shifted gamma distribution will be applied
instead of a normal gamma distribution.""","""
ERROR: Please specify the maximum distance from the average you want your
uniformly distributed values to have. The maximum distance must be a
non-negative number."""]



# Lists ########################################################################

LIST__normal = ["N", "n", "NORMAL", "Normal", "normal", "NORM", "Norm", "norm"]
LIST__gamma = ["G", "g", "GAMMA", "Gamma", "gamma"]
LIST__uniform = ["U", "u", "UNIFORM", "Uniform", "uniform", "UNI", "Uni", "uni"]



# Dictionaries #################################################################

DICT__dists = {}
for i in LIST__normal: DICT__dists[i] = DIST.NORMAL
for i in LIST__gamma: DICT__dists[i] = DIST.GAMMA
for i in LIST__uniform: DICT__dists[i] = DIST.UNIFORM



# Apply Globals ################################################################

PRINT.PRINT_ERRORS = PRINT_ERRORS
PRINT.PRINT_PROGRESS = PRINT_PROGRESS
PRINT.PRINT_METRICS = PRINT_METRICS



# Functions ####################################################################

def Generate_Reads(path_in, paths_out, phred, read_lengths, quality_settings,
            duplicate_settings, duplicate_minmax, truncation_settings, threads,
            unique_id_mod):
    """
    Generate a series of DNA reads from the DNA fragments in a FASTA file. This
    is designed to imitate the sequencing of DNA fragments in NGS.
    
    @path_in
            (str - filepath)
            The filepath of the FASTA file which contains the DNA fragment
            sequences.
    @paths_out
            (list<str - filepath))
            The files to which the forward and reverse reads respectively are
            to be written.
    @phred
            (dict<int:str>)
            OR
            (str)
            A phred dictionary which can convert phred scores into their
            corresponding chars.
            OR
            A string denoting the relevant phred dictionary.
    @read_lengths
            ([int, int])
            The length of the forward and reverse reads respectively.
    @quality_settings
            ([int, int, float])
            If the first value in the list is set to 0, reads will 100% accurate
            transcriptions of the template, and the quality scores will be set
            to 42 (the maximum) for every base.
            Otherwise, this list contains the "quality score" settings used for
            randomly generating quality scores (and thus accuracy) of the read
            basepairs.
            Otherwise, this is list containing the following three variables:
                1)  (int)
                    The mean value of the statistical distribution.
                2)  (int) - Pseudo ENUM
                    An int which signifies which statistical distribution to
                    use:
                        0: Normal distribution
                        1: Gamma distribution
                        2: Uniform distribution
                3)  (float)
                    The paramter variable to use for the statistical
                    distribution specified by the second variable in this list.
                    Its meaning will vary depending on the distribution:
                        NORMAL DISTRIBUTION:
                            This variable is the standard deviation.
                        GAMMA DISTRIBUTION:
                            This variable is the alpha modifier of the
                            distribution. The beta value is automatically
                            calculated such at A*B=Average_Depth.
                        UNIFORM DISTRIBUTION:
                            (Only relevant for fragment lenth settings)
                            This variable is the difference between the mean of
                            the distribution, and either the upper or lower
                            limits of the distribution range.
    @duplicate_settings
            ([int, int, float])
            The "quality score" settings used for randomly generating the
            number of read/read-pair duplicates on different individual
            fragments.
            A list containing three variables with an identical layout to
            @quality_settings. (See above)
    @duplicate_minmax
            ([int, int])
            The minimum and maximum number of duplicates permitted per fragment.
    @truncation_settings
            ([int, int, float])
            The "quality score" settings used for randomly generating the
            number of nucleotides to be truncated on different individual
            reads.
            A list containing three variables with an identical layout to
            @quality_settings. (See above)
    @threads
            (int)
            The number of threads to use. (Multi-threading) Functionality not
            implemented yet.
    @unique_id_mod
            (str)
            A string prefix which forms part of the fragment ID. Allows reads
            from different runs to be pooled together and still have unique
            IDs relative to each other.
    
    Return a value of 0 if the function runs successfully.
    Return a value of 1 if there is a problem with the input file.
    Return a value of 2 if there is a problem with the output file.
    Return a value of 3 if there is a problem during the read generation
            process.
    Return a value of 4 if there is a problem with [phred].
    
    Generate_Reads(str, str, [int, int], [int, int, float], [int, int, float],
            [int, int], [int, int, float], int) -> int
    """
    # Setup reporting
    fragments = 0
    reads = 0
    bases_forward = 0
    errors_forward = 0
    bases_reverse = 0
    errors_reverse = 0
    cumulative_score = 0
    cumulative_copies = 0
    # Calculate distribution parameters
    quality_settings = Calculate_Dist_Params(quality_settings)
    duplicate_settings = Calculate_Dist_Params(duplicate_settings)
    truncation_settings = Calculate_Dist_Params(truncation_settings)
    # Phred
    if type(phred) == str:
        if phred in LIST__phred33: phred = DICT__scores_to_chars__phred33
        elif phred in LIST__phred64: phred = DICT__scores_to_chars__phred64
        else: return 4
    # Setup the I/O
    try:
        f = FASTA_Reader()
        f.Open(path_in)
    except:
        return 1
    try:
        if read_lengths[0]: o1 = open(paths_out[0], "w")
        else: o1 = None
        if read_lengths[1]: o2 = open(paths_out[1], "w")
        else: o2 = None
        o = [o1, o2]
    except:
        return 2
    # Muli-threading
    """
    TODO: Multi-threading has not yet been implemented.
    """
    threading = None
    # Main loop
    PRINT.printP(STR__GenReads_begin)
    while not f.End():
        f.Read()
        frag = f.Get_Current_SOFT()
        metrics = Generate_Reads_From_Frag(frag, o, phred, read_lengths,
            quality_settings, duplicate_settings, duplicate_minmax,
            truncation_settings, threading, unique_id_mod)
        # Update metrics
        fragments += 1
        reads += metrics[0]
        bases_forward += metrics[1]
        errors_forward += metrics[2]
        bases_reverse += metrics[3]
        errors_reverse += metrics[4]
        cumulative_score += metrics[5]
        cumulative_copies += metrics[6]
    # Finish up
    if read_lengths[0]: o1.close()
    if read_lengths[1]: o2.close()
    f.Close()
    PRINT.printP(STR__GenReads_complete)
    # Reporting
    Report_Metrics(fragments, reads, bases_forward, errors_forward,
            bases_reverse, errors_reverse, cumulative_score, cumulative_copies)
    # Wrap up
    return 0



def Generate_Reads_From_Frag(frag, outputs, phred, read_lengths,
            quality_settings, duplicate_settings, duplicate_minmax,
            truncation_settings, threading, unique_id_mod):
    """
    Generate a number of DNA reads from a given DNA fragment.
    
    Return a list containing various metrics for how this operation went.
    
    This is a modular component of Generate_Reads. Generate_Reads works with an
    entire input file which contains multiple fragments. This function deals
    with individual fragments.
    """
    # Metrics
    reads = 0
    bases_forward = 0
    errors_forward = 0
    bases_reverse = 0
    errors_reverse = 0
    cumulative_score = 0
    cumulative_copies = 0
    # Unpacking
    frag_name, anno, frag_seq = frag
    length_f, length_r = read_lengths
    min_, max_ = duplicate_minmax
    d1, d2, d3 = duplicate_settings
    t1, t2, t3 = truncation_settings
    # Determine duplicates
    if min_ == max_:
        duplicates = min_
    else:
        duplicates = Custom_Random_Distribution(d1, d2, d3)
        if duplicates < min_: duplicates = min_
        elif duplicates > max_: duplicates = max_
    # Per duplicate
    while duplicates > 0:
        # Lengths
        if ( t2 == DIST.NORMAL and t3 == 0 ):
            if type(t1) == float: t1 = int(t1+0.5)
            trunc_f = trunc_r = t1
        else:
            trunc_f = Custom_Random_Distribution(t1, t2, t3)
            trunc_r = Custom_Random_Distribution(t1, t2, t3)
        if trunc_f < 0: trunc_f = 0
        if trunc_r < 0: trunc_r = 0
        temp_f = length_f - trunc_f
        temp_r = length_r - trunc_r
        # Generate reads
        flag_copy = False
        if temp_f > 1: # Forward
            # Generate read
            name = Generate_Name(unique_id_mod, frag_name, duplicates,
                    STR__forward)
            seq = frag_seq[:temp_f]
            results = Generate_Read_From_Seq(seq, phred, temp_f,
                    quality_settings)
            read, scores, errors, total = results
            # Write
            sb = "@" + name + "\n" + read + "\n+\n" + scores + "\n"
            outputs[0].write(sb)
            # Metrics
            reads += 1
            bases_forward += temp_f
            errors_forward += errors
            flag_copy = True
            cumulative_score += total
        if temp_r > 1: # Reverse
            # Generate read
            name = Generate_Name(unique_id_mod, frag_name, duplicates,
                    STR__reverse)
            temp = frag_seq[-temp_r:]
            seq = Get_Complement(temp)
            results = Generate_Read_From_Seq(seq, phred, temp_r,
                    quality_settings)
            read, scores, errors, total = results
            # Write
            sb = "@" + name + "\n" + read + "\n+\n" + scores + "\n"
            outputs[1].write(sb)
            # Metrics
            reads += 1
            bases_reverse += temp_r
            errors_reverse += errors
            flag_copy = True
            cumulative_score += total
        #
        if flag_copy: cumulative_copies += 1
        duplicates -= 1
    # Return
    return [reads, bases_forward, errors_forward, bases_reverse,
            errors_reverse, cumulative_score, cumulative_copies]

def Generate_Read_From_Seq(seq, phred, length, quality_settings):
    """
    Generate a DNA read from a given DNA sequence.
    
    This is a modular component of Generate_Reads_From_Frag. Each fragment can
    generate multiple reads. This function deals with individual reads.
    """
    if length > len(seq): length = len(seq)
    # Quality
    q1, q2, q3 = quality_settings
    if ( q2 == DIST.NORMAL or q2 == DIST.UNIFORM ) and q3 == 0:
        if q1 == 0: # Perfect accuracy
            scores = phred[42] * length
            return [seq, scores, 0, 0]
        # Consistent accuracy
        flag = True
    else: flag = False # Inconsistent accuracy
    # Metric
    total = 0
    errors = 0
    # Setup
    read = ""
    scores = ""
    # Loop
    for char in seq:
        q = Custom_Random_Distribution(q1, q2, q3, True)
        if q > 42: q = 42
        threshold = DICT__scores_to_probs[q]
        r = Random.random()
        if r < threshold: # Match
            read += char
        else: # Mismatch
            errors += 1
            possible = DICT__mismatches[char]
            char = Random.choice(possible)
            read += char
        scores += phred[q]
        total += q   
    # Return
    if len(read) != len(scores): print "###"
    return [read, scores, errors, total]



def Calculate_Dist_Params(settings):
    """
    Return a processed and expanded version of the randomized statistical
    distribution parameter settings.
    
    @settings
            ([int/float, int, int/float])
            Three values, which are the mean, the distribution method, and the
            additional parameters respectively.
    
    Calculate_Dist_Params([int/float, int, int/float]) -> [int/float, int,
            int/float]
    """
    mean, dist, param = settings
    if dist == DIST.GAMMA:
        beta = ( float(mean) / param ) ** 0.5
        alpha = float(mean) / beta
        param = [alpha, beta]
    elif dist == DIST.UNIFORM:
        if param:
            lower = mean - param
            upper = mean + param
            param = range(lower, upper+1)
            mean = 0
        else:
            param = 0
            while mean > 1:
                param += 1
                mean -= 1
    return [mean, dist, param]

def Custom_Random_Distribution(mean, method, param, must_positive=False):
    """
    MAY BE DIFFERENT FROM OTHER Custom_Random_Distribution FUNCTIONS IN OTHER
    PROGRAMS.
    
    Generate a random integer.
    
    The distribution of the amortized results of this function being run,
    multiple times, with the same parameters, will be equal to [mean], or
    [mean]+[param] in the case of certain uniform distributions.

    MAJORLY DIFFERING SPECIAL BEHAVIOUR:
    If [mean] is 0 and the normal distribution method is chosen, one of the
    values in [param] will be chosen at random
    
    @mean
            (int/float)
            The desired average outcome.
            In the case where a Uniform distribution is chosen and @mean is not
            0, then the average outcome of this function with the same
            parameters will be @mean+@param.
    @method
            (int) - Pseudo ENUM
            An integer signifying which probability distribution to use:
                0: Normal distribution
                1: Gamma distribution
                2: Uniform distribution
    @param
            (*)
            Varies depending on the distribution method chosen:
                NORMAL DISTIRBUTION:
                    (float)
                    The standard deviation of the normal distribution.
                GAMMA DISTRIBUTION:
                    ([float, float, bool])
                    A list containing the Alpha and Beta to be used for the
                    Gamma distribution.
                UNIFORM:
                    (list/int)
                    If @mean is 0, then @param is a list of values, one of which
                    will be chosen at random with equal probability.
                    If @mean is not zero, then @param is the number to add,
                    essentially resulting in a series of numbers which are
                    either FLOOR(@mean) or CEILING(@mean), the average of which
                    is @mean.
    @must_positive
            (bool)
            Whether or not to forcibly make the result positive if it is
            negative.
    
    Custom_Random_Distribution(int/float, int, *, bool) -> int
    """
    if method == DIST.UNIFORM:
        if mean:
            r = Random.random()
            if r > mean: return param+1
            else: return param
        else:
            r = Random.choice(param)
    else:
        if method == DIST.NORMAL:
            r = Random.normalvariate(mean, param)
        elif method == DIST.GAMMA:
            r = Random.gammavariate(param[0], param[1])
        r = int(r+0.5)
    if must_positive:
        if r < 0: r = -r
    return r

def Generate_Name(unique_id, frag_name, duplicates, direction):
    """
    Generate a read name, given the name of a fragment, the current duplicate
    number, and the orientation of the read.
    
    @unique_id   (str)
    @frag_name   (str)
    @duplicates  (int)
    @direction   (str)
    
    Generate_Name(str, str, int, str) -> str
    """
    # Duplicate string
    s = str(duplicates)
    s = Pad_Str(s, COPY_DIGITS, "0")
    # SB
    sb = unique_id + frag_name + "__" + s + direction
    return sb



def Report_Metrics(fragments, reads, bases_forward, errors_forward,
            bases_reverse, errors_reverse, cumulative_score, cumulative_copies):
    """
    Print a report into the command line interface of the results of running
    this program
    
    @fragments
            (int)
            The total number of fragments processed.
    @reads
            (int)
            The total number of reads generated.
    @bases_forward
            (int)
            The total number of nucleotides generated for forward reads.
    @errors_forward
            (int)
            The total number of errors in the forward reads.
    @bases_reverse
            (int)
            The total number of nucleotides generated for reverse reads.
    @errors_reverse
            (int)
            The total number of errors in the reverse reads.
    @cumulative_score
            (int)
            The cumulative total of the Phred scores of all the nucleotides
            generated.
    @cumulative_copies
            (int)
            The cumulative count of the number of copies.
    
    Report_Metrics(int,int,int,int,int,int) -> None
    """
    # Can potentially be expanded to include more metrics in the future
    # Paired
    if bases_reverse > 0: reads_ = reads/2
    else: reads_ = reads
    # Calculations
    avg_f = float(bases_forward)/reads_
    avg_f_e = float(errors_forward)/reads_
    avg_r = float(bases_reverse)/reads_
    avg_r_e = float(errors_reverse)/reads_
    total_b = bases_forward + bases_reverse
    avg_score = float(cumulative_score)/total_b
    avg_copies = float(cumulative_copies)/fragments
    # Strings
    str_frags = str(fragments) + "   "
    str_reads = str(reads) + "   "
    str_f = str(avg_f) + "0"
    str_f_e = str(avg_f_e) + "0"
    str_r = str(avg_r) + "0"
    str_r_e = str(avg_r_e) + "0"
    str_avg_score = str(avg_score) + "0"
    str_avg_copies = str(avg_copies) + "0"
    # Padding and formatting
    str_f = Trim_Percentage_Str(str_f, 2)
    str_f_e = Trim_Percentage_Str(str_f_e, 2)
    str_r = Trim_Percentage_Str(str_r, 2)
    str_r_e = Trim_Percentage_Str(str_r_e, 2)
    str_avg_score = Trim_Percentage_Str(str_avg_score, 2)
    str_avg_copies = Trim_Percentage_Str(str_avg_copies, 2)
    max_size = max([len(str_frags), len(str_reads), len(str_f), len(str_r),
            len(str_avg_score), len(str_avg_copies)])
    str_frags = Pad_Str(str_frags, max_size, " ", 0)
    str_reads = Pad_Str(str_reads, max_size, " ", 0)
    str_f = Pad_Str(str_f, max_size, " ", 0)
    str_f_e = Pad_Str(str_f_e, max_size, " ", 0)
    str_r = Pad_Str(str_r, max_size, " ", 0)
    str_r_e = Pad_Str(str_r_e, max_size, " ", 0)
    str_avg_score = Pad_Str(str_avg_score, max_size, " ", 0)
    str_avg_copies = Pad_Str(str_avg_copies, max_size, " ", 0)
    # Print
    PRINT.printM(STR__metrics.format(F = str_frags, R = str_reads, L1 = str_f,
            E1 = str_f_e, L2 = str_r, E2 = str_r_e, Q = str_avg_score,
            D = str_avg_copies))



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Generate_Reads(raw_command_line_input):
    """
    Parse the command line input and call the Generate_Reads function
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
    
    # Initial validation (Redundant in current version)
    if len(inputs) < 1:
        PRINT.printE(STR__insufficient_inputs)
        PRINT.printE(STR__use_help)
        return 1
    
    # Validate mandatory inputs
    path_in = inputs.pop(0)
    valid = Validate_Read_Path(path_in)
    if valid == 1:
        PRINT.printE(STR__IO_error_read.format(f = path_in))
        PRINT.printE(STR__use_help)
        return 1
    
    # Set up rest of the parsing
    path_out_r1 = Generate_Default_Output_File_Path_From_Folder(path_in,
            FILEMOD__FASTQ_1)
    path_out_r2 = Generate_Default_Output_File_Path_From_Folder(path_in,
            FILEMOD__FASTQ_2)
    phred = DEFAULT__phred
    len_1 = DEFAULT__read_1_len
    len_2 = DEFAULT__read_2_len
    avg_quality = DEFAULT__avg_quality
    quality_dist = DEFAULT__quality_dist
    quality_param = DEFAULT__quality_param
    avg_dupes = DEFAULT__avg_dupes
    dupes_dist = DEFAULT__dupes_dist
    dupes_param = DEFAULT__dupes_param
    min_dupes = DEFAULT__min_dupes
    max_dupes = DEFAULT__max_dupes
    avg_trunc = DEFAULT__avg_trunc
    trunc_dist = DEFAULT__trunc_dist
    trunc_param = DEFAULT__trunc_param
    threads = DEFAULT__threads
    unique_id_mod = DEFAULT__STR__unique_id_mod
    
    # Validate optional inputs (except output path)
    while inputs:
        arg = inputs.pop(0)
        
        # Confirm valid flag
        if arg in ["-p", "-x", "-u"]: # Second argument
            try:
                arg2 = inputs.pop(0)
            except:
                PRINT.printE(STR__insufficient_inputs)
                PRINT.printE(STR__use_help)
                return 1
        elif arg in ["-o", "-r", "-m"]: # Second and third arguments
            try:
                arg2 = inputs.pop(0)
                arg3 = inputs.pop(0)
            except:
                PRINT.printE(STR__insufficient_inputs)
                PRINT.printE(STR__use_help)
                return 1
        elif arg in ["-q", "-d", "-t"]: # Second, third, and fourth arguments
            try:
                arg2 = inputs.pop(0)
                arg3 = inputs.pop(0)
                arg4 = inputs.pop(0)
            except:
                PRINT.printE(STR__insufficient_inputs)
                PRINT.printE(STR__use_help)
                return 1
        else: # Invalid
            arg = Strip_X(arg)
            PRINT.printE(STR__invalid_argument.format(s = arg))
            PRINT.printE(STR__use_help)
            return 1
        
        # Individual validation
        if arg == "-o": # Output files - Actual validation done later
            path_out_r1 = arg2
            path_out_r2 = arg3
        elif arg == "-r":
            len_1 = Validate_Int_NonNeg(arg2)
            len_2 = Validate_Int_NonNeg(arg3)
            if len_1 == -1 or len_2 == -1 or ( len_1 == 0 and len_2 == 0 ):
                PRINT.printE(STR__invalid_lengths.format(s1=arg2, s2=arg3))
                return 1
        elif arg == "-p":
            phred = arg2
        elif arg == "-m":
            flag = False
            min_dupes = Validate_Int_NonNeg(arg2)
            max_dupes = Validate_Int_Positive(arg3)
            if min_dupes == -1:
                flag = True
                PRINT.printE(STR__invalid_min_dupe.format(s = arg2))
            if max_dupes == -1:
                flag = True
                PRINT.printE(STR__invalid_max_dupe.format(s = arg3))
            if flag: return 1
        elif arg == "-x":
            threads = Validate_Int_Positive(arg2)
            if threads == -1:
                PRINT.printE(STR__invalid_threads.format(s = arg2))
                return 1
        elif arg == "-u":
            unique_id_mod = arg2
        else:
            # Determine type
            if arg == "-q": dist = "quality score"
            if arg == "-d": dist = "duplicate copy number"
            if arg == "-t": dist = "truncation length"
            
            # Validate
            avg = Validate_Number(arg2)
            params = Validate_Dist_Params(arg3, arg4)
            if avg == None:
                PRINT.printE(STR__invalid_avg.format(s=dist, m=arg2))
                return 1
            if not params:
                PRINT.printE(STR__invalid_params.format(s=dist, d=arg3, p=arg4))
                return 1
            if avg == 0 and params[0] == DIST.GAMMA:
                PRINT.printE(STR__invalid_params.format(s=dist, d=arg3, p=arg4))
                return 1
            
            # Type specific
            if arg == "-q":
                avg_quality = avg
                quality_dist, quality_param = params
            if arg == "-d":
                avg_dupes = avg
                dupes_dist, dupes_param = params
            if arg == "-t":
                avg_trunc = avg
                trunc_dist, trunc_param = params
    
    # Validate phred
    if phred in LIST__phred33: phred = DICT__scores_to_chars__phred33
    elif phred in LIST__phred64: phred = DICT__scores_to_chars__phred64
    else:
        PRINT.printE(STR__invalid_phred.format(s = phred))
        return 1
    
    # Validate output path
    if len_1:
        valid_out_1 = Validate_Write_Path(path_out_r1)
        if valid_out_1 == 2: return 0
        if valid_out_1 == 3:
            PRINT.printE(STR__IO_error_write_forbid)
            return 1
        if valid_out_1 == 4:
            PRINT.printE(STR__IO_error_write_unable)
            return 1
    if len_2:
        valid_out_2 = Validate_Write_Path(path_out_r2)
        if valid_out_2 == 2: return 0
        if valid_out_2 == 3:
            PRINT.printE(STR__IO_error_write_forbid)
            return 1
        if valid_out_2 == 4:
            PRINT.printE(STR__IO_error_write_unable)
            return 1
    
    # Run program
    exit_state = Generate_Reads(path_in, [path_out_r1, path_out_r2], phred,
            [len_1, len_2], [avg_quality, quality_dist, quality_param],
            [avg_dupes, dupes_dist, dupes_param], [min_dupes, max_dupes],
            [avg_trunc, trunc_dist, trunc_param], threads, unique_id_mod)
    
    # Exit
    if exit_state == 0: return 0
    else:
        if exit_state == 1: PRINT.printE(STR__input_invalid)
        if exit_state == 2: PRINT.printE(STR__output_invalid)
        if exit_state == 3: PRINT.printE(STR__generation_invalid)
        PRINT.printE(STR__use_help)
        return 1



def Validate_Dist_Params(method, param):
    """
    Validates the statistical distribution parameters; [method] needs to be text
    indicating a valid distribution, and [param] needs to specify valid
    parameters for said distribution, and will depend on [method].
    
    Return a list containing a pseudo-enum int and a second variable if the
    parameters are valid.
    Return an empty list if the parameters are invalid.
    
    Valid values for [method] include "Normal", "Gamma", and "Uniform", and all
    capitalization variants of these strings.
    
    Regarding param:
        
        For a normal distribtions, [param] is the standard deviation, a
        non-negative number.
        
        For a gamma distribution, [param] is the ratio between alpha and beta.
        The greater it's value, the greater the ratio between the alpha and beta
        values, and the more skwewed the data becomes. For negative [param]
        values, the distribution is flip-shifted.
        
        For a uniform distribution, [param] is how far away from the average the
        distribution range goes.
    
    Validate_Dist_Params(str, str) -> list<*>
    """
    dist = DICT__dists.get(method, 0)
    if dist == 1: # Normal
        param = Validate_Float_NonNeg(param)
        if param == -1: return []
    elif dist == 2: # Gamma
        param = Validate_Float_NonZero(param)
        if param == 0: return []
    elif dist == 3: # Uniform
        param = Validate_Int_NonNeg(param)
        if param == -1: return []
    else:
        return []
    return [dist, param]

def Validate_Write_Path(filepath):
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




# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Generate_Reads(sys.argv)


