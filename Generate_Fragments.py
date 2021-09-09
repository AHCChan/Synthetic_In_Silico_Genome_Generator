HELP_DOC = """
FRAGMENT GENERATOR
(version 1.0)
by Angelo Chan

This is a program for generating DNA fragment sequences based on a template,
typically a genome.

In the context of a synthetic genome, this program will be used to generate
fragments from the genome, mimicking the DNA fragmentation process. Afterwards,
smaller sequences will be generated from the fragments, mimicking the NGS DNA
sequencing process.

The expected input is a folder containing one or more FASTA files. The fragments
will be output into a single FASTA file.



BACKGROUND INFO:

In whole genome next-gen sequencing protocols, the genome is fragmented into
smaller DNA fragments. However, with many sequencing technologies and protocols,
only the ends of the fragments are sequenced into reads.

Therefore, to achieve a desired level of coverage with a reads library, users
will typically need to generate a fragment library with a higher level of
coverage.

The formula is as follows:

    FRAG_COVERAGE = READ_COVERAGE * ( READ_SIZE / FRAG_SIZE)
        
        READ_SIZE is the size (bp) of the read(s) generated by the sequencer

        FRAG_SIZE is the size (bp) of the fragments generated here
        
        ( READ_SIZE / FRAG_SIZE ) calculates the average percentage of a
        fragment which will be sequenced.
        
        READ_COVERAGE is desired final average coverage level per nucleotide
        
        FRAG_COVERAGE is calculated from all of the above factors and is used to
        calculate the probability of a fragment being generated at each location



USAGE:
    
    python27 Generate_Fragments.py <input_folder> [-o <output_filepath] [-d
            <depth_of_coverage>] [-c N|G|U <stdev>|<alpha_mod>|<max_dist>] [-r
            <read_length>] [-l <avg_frag_len>] [-f N|G|U
            <stdev>|<alpha_mod>|<max_dist>] [-m <method> [method_sup]...]



MANDATORY:
    
    input_folder
        
        The filepath of the input folder containing the FASTA file(s) from
        which the DNA fragments will be generated.

OPTIONAL:
    
    output_filepath
        
        (DEFAULT path generation available)
        
        The filepath of the output file where resultant FASTA files will be
        output into.
    
    depth_of_coverage
        
        (DEFAULT: 10)
        
        The average number of times a nucleotide will be "sequenced". If no
        read length is specified, or if a read length of -1 is specified, then
        it is assumed that each fragment is sequenced completely, without
        overlap.
        
        If a gamma distribution is used, the actual resulting depth of coverage
        will be lower than this.
    
    read_length
        
        (DEFAULT: -1)
        
        The number of nucleotides covered by each read or read-pair.
    
    avg_frag_len
        
        (DEFAULT: 500)
        
        The average length of the fragments to be produced.
    
    N|G|U
        
        (DEFAULT (-c): G)
        (DEFAULT (-f): N)
        
        The probasbility distribution used to generate fragments and determine
        fragment length.
            
            N   Normal variate distribution
            G   Gama variate distribution
            U   Uniform distribution
    
    stdev
        
        (Only applies if a Normal Variate distribution was specified)
        (DEFAULT: 50)
        
        The standard deviation of the normal distribution.
    
    alpha_mod
        
        (Only applies if a Gamma Variate distribution was specified)
        (DEFAULT: 1)
        
        The skewness factor of the Gamma distribution.
        
        The magnitude of @alpha_mod determines how unskewed the distribution is.
        As @alpha_mod approaches infinity, the resulting gamma distribution will
        begin to resemble a normal distribution. As @alpha approaches 0, the
        resulting gamma distribution will become increasingly skewed.
        
        It is known that, for a Gamma Distribution:
            
            Alpha * Beta ~= Desired_Average
        
        The Beta is automatically calculated such that:
            
            Alpha = Beta * Alpha_Mod
        
        A gamma variate distribution is right-tailed, with most values
        clustered to the left of the mean.
        
        A negative alpha may be specified to obtain a flipped and shifted
        gamma variate distribution, which will be left-tailed, with most values
        clusterd to the right of the mean. Please note that this is an
        unorthodox method. A better method should be implemented and used if
        users need a high fidelity left-tailed distribution.
        
    max_dist
        
        (Only applies if a Uniform distribution was specified)
        (DEFAULT: <depth_of_coverage>)
        
        The furthest away from the specified average which a randomly generated
        value can be. Cannot exceed the average. If @max_dist equals or exceeds
        the average, then the uniform distribution range will be from 0 to
        double whatever the average is.
        
        Ex. If it is specified that the average fragment length is 500 and that
        the fragments are to follow a uniform distribution with a @max_dist of
        50, then all fragment lengths will be between 450 and 550 in length.
    
    (-c)
        
        Used to signify that the following parameters pertain to the probability
        distribution of read/fragment coverage.
        Ex. "-c G 1.0" signifies that the coverage of nucleotides follows a
        gamma variate distribution with an Alpha of 1.0. (The average coverage
        is specified using the "-d" flag.)
    
    (-f)
        
        Used to signify that the following parameters pertain to the probability
        distribution of fragment sizes.
        Ex. "-c N 50" signifies that the fragment sizes follow a normal
        distribution, with a standard deviation of 50. (The average read length
        is specified using the "-r" flag.)
    
    method
        
        (DEFAULT: ALL)
        Method of deciding where fragments can be generated. Fragments generated
        using restriction enzymes will only occur at certain locations, while
        fragments generated using sonication can start or begin at any
        nucleotide.
    
    method_sup
        
        Supplementary inputs, as required, for deciding where fragments can be
        generated. Currently not reelvant because the only method implemented
        does not require any additional inputs.



EXAMPLES SCENARIO EXPLANATION:
    
    1:
    An almost bare minimum use case. (Specifying the output path is not
    mandatory, but it is good practice to do so.)
    
    2:
    The "fragments" will be pair-end sequenced with 2x75 reads, hence "-r 150".
    Since only 150 of the 500 bp will be sequenced, more fragments will be
    generated to ensure that the final coverage levels will be the 10. (Default
    depth of coverage)
    
    3:
    The "fragments" were generated by hydrolysis with an average length of 400,
    and a modestly left skew. (Gamma variate distribution with an Alpha of 1)
    
    4:
    Some parts of the genome were less accessible during the fragmentation and
    amplification procedure, so coverage is heavily skewed. Some parts of the
    genome have very deep coverage, while other parts have very little. Note
    that this probability distribution has been done on a base-pair level rather
    than a loci level, and is thus, not a good imitation of the biological
    phenomenon described.
    
    5:
    The sonication and subsequent size selection steps were carried out poorly,
    resulting in a normally distributed, but broadly distributed range of
    fragment sizes. (Standard deviation of 200)
    
    6:
    The "fragments" are uniformly distributed in size, between 500bp and 600bp.
    The average is specified as 550, while the maximum distance is specified as
    50 to achieve this outcome.
    
    7:
    The "fragments" are all exactly 800bp in size. To achieve this, the average
    is specified as 800, and the distribution of fragment sizes is specified as
    a normal distribution with a standard deviation of 0.

EXAMPLES:
    
    python27 Generate_Fragments.py Path/GenomeFolder -o Output.fa
    
    python27 Generate_Fragments.py Path/GenomeFolder -r 150
    
    python27 Generate_Fragments.py Path/GenomeFolder -l 400 -f G 1
    
    python27 Generate_Fragments.py Path/GenomeFolder -c G 0.1
    
    python27 Generate_Fragments.py Path/GenomeFolder -f N 200
    
    ----------------------------------------------------------------------------
    
    python27 Generate_Fragments.py Path/GenomeFolder -l 550 -f U 50
    
    python27 Generate_Fragments.py Path/GenomeFolder -l 800 -f N 0

USAGE:
    
    python27 Generate_Fragments.py <input_folder> [-o <output_filepath] [-d
            <depth_of_coverage>] [-c N|G|U <stdev>|<alpha_mod>|<max_dist>] [-r
            <read_length>] [-l <avg_frag_len>] [-f N|G|U
            <stdev>|<alpha_mod>|<max_dist>] [-m <method> [method_sup]...]
"""

NAME = "Generate_Fragments.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

FILEMOD__FASTA = ".fa"

# For name string
ID_SIZE = 15
STR__forward = "F"
STR__reverse = "R"




# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"
    
DEFAULT__depth = 10
DEFAULT__read_len = -1
DEFAULT__frag_len = 500
DEFAULT__cov_dist = 1 # DIST.GAMMA = 1. Alter this if the DIST enum is altered
DEFAULT__cov_num = 1
DEFAULT__frag_dist = 0 # DIST.NORMAL = 0. Alter this if the DIST enum is altered
DEFAULT__frag_num = 50
DEFAULT__method = 0



# Imported Modules #############################################################

import sys
import os

import random as Random



import _Controlled_Print as PRINT
import NSeq_Match as N_SEQ
from _Command_Line_Parser import *

from Chr_FASTA_File_Reader import *



# Enums ########################################################################

class DIST: # For Distribution
    NORMAL=0 # If this is changed, sync relevant defaults
    GAMMA=1
    UNIFORM=2

class METHOD:
    ALL=0



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python "\
"Generate_Fragments.py -h"



STR__invalid_dist = """
ERROR: Invalid statistical distirbution: {s}
Please specify one of:
    NORMAL
    GAMMA
    UNIFORM"""



STR__metrics = """
Total fragments generated: {C}
Average fragment size:     {A}"""

STR__GenFrags_begin = "\nRunning Generate_Random_Chromosomes..."

STR__GenFrags_complete = "\nGenerate_Random_Chromosomes successfully finished."



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

LIST__all = ["A", "a", "ALL", "All", "all"]



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

def Generate_Fragments(path_in, path_out, depth_settings, read_len,
            frag_settings, method_settings):
    """
    Generate a series of DNA fragments from the DNA templates in a folder of
    FASTA files.
    
    @path_in
            (str - dirpath)
            The filepath of the folder containing the FASTA file(s) containing
            the original DNA templates which the fragments are based on.
    @path_out
            (str - dirpath)
            The file to which the output is written.
    @depth_settings
            ([int, int, float])
            The "depth of coverage" settings.
            A list containing the following three variables:
                1)  (int)
                    The average depth of coverage for the DNA templates by the
                    reads which will be generated using the fragments.
                2)  (int) - Pseudo ENUM
                    An int which signifies which statistical distribution to
                    use when determining the likelihood of a fragment (and thus
                    coverage) being generated at any particular location:
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
                            calculated such at A*B=Average_Depth. If a negative
                            value is provided, the distribution used will change
                            to a flip-shifted gamma distribution.
                        UNIFORM DISTRIBUTION:
                            (Only relevant for fragment lenth settings)
                            This variable is the difference between the mean of
                            the distribution, and either the upper or lower
                            limits of the distribution range.
    @read_len
            (int)
            The intended total length of the reads which will be generated by
            the fragments. If 0 or -1, this will indicate that the fragments
            will be sequenced in their entirety without overlapping reads.
    @frag_settings
            ([int, int, float])
            The "fragment length" settings.
            A list containing the following three variables:
                1)  (int)
                    The average length of the fragments to be generated.
                2)  (int) - Pseudo ENUM
                    An int which signifies which statistical distribution to
                    use when determining the length of a fragment when one is
                    generated:
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
                            This variable is the alpha value of the
                            distribution. The beta value is automatically
                            calculated such at A*B=1. If a negative value is
                            provided, the distribution used will change to a
                            flip-shifted gamma distribution.
                        UNIFORM DISTRIBUTION:
                            This variable is the difference between the mean of
                            the distribution, and either the upper or lower
                            limits of the distribution range.
    @method_settings
            ([int, *...])
            The "method for determining fragment starts and ends" settings.
            A list of variables containing all settings relevant to determining
            where fragments can start and end. The first variable is as follows:
                (int) - Pseudo ENUM
                An int which signifies where fragments can start and end. 
                    0: All
            What other variables are required depend on the first integer:
                ALL:
                    No other variables are necessary.
    
    Return a value of 0 if the function runs successfully.
    Return a value of 1 if there is a problem accessing the data or if there are
            no valid FASTA files in the input folder.
    Return a value of 2 if there is a problem with the output file.
    Return a value of 3 if there is a problem during the fragment generation
            process.
    
    Generate_Fragments(str, str, [int, int, float], int, [int, int, float],
            [int, *...]) -> int
    """
    # Setup reporting
    outcomes = [] # Outcomes are added after each input file is processed
    # Setup the I/O
    paths_in = Get_Files_W_Extensions(path_in, LIST__FASTA)
    if not paths_in: return 1
    try:
        o = open(path_out, "w")
    except:
        return 2
    # Main loop
    PRINT.printP(STR__GenFrags_begin)
    for path in paths_in:
        outcome = Generate_Fragments__FILE(path, o, depth_settings,
                read_len, frag_settings, method_settings)
        if outcome: outcomes.append(outcome)
        else:
            o.close()
            return 3
    # Finish up
    o.close()
    PRINT.printP(STR__GenFrags_complete)
    # Reporting
    Report_Metrics(outcomes)
    # Wrap up
    return 0

def Generate_Fragments__FILE(path_in, output, depth_settings, read_len,
            frag_settings, method_settings):
    """
    Generate a series of DNA fragments from the DNA template in the input file
    specified by [path_in].
    
    The per-input-file version of the Generate_Fragments() function.
    
    @path_in
            (str - dirpath)
            The filepath of the input file.
    @path_out
            (str - dirpath) OR
            (file)
            The filepath of the file to which the output is written, OR the file
            itself as a file object.
    @depth_settings
            ([int, int, float])
            The "depth of coverage" settings.
            See Generate_Fragments() documentation for details.
    @read_len
            (int)
            The intended total length of the reads which will be generated by
            the fragments. If 0 or -1, this will indicate that the fragments
            will be sequenced in their entirety without overlapping reads.
    @frag_settings
            ([int, int, float])
            The "fragment length" settings.
            See Generate_Fragments() documentation for details.
    @method_settings
            ([int, *...])
            The "method for determining fragment starts and ends" settings.
            See Generate_Fragments() documentation for details.
    
    Return a list containing the number of number of fragments generated and
    their total length.
    Return an empty list if an error occured.
    
    Generate_Fragments(str, str/file, [int, int, float], int, [int, int, float],
            [int, *...]) -> [int, int]
    """
    # Metrics setup
    count = 0
    total = 0
    
    # Unpack
    depth, depth_method, depth_param = depth_settings
    frag_len, frag_len_method, frag_len_param = frag_settings
    method = method_settings[0]
    
    # Calculations (utilization and probabilities)
    utilization = float(read_len)/frag_len
    bases_per_frag = frag_len * utilization
    if method == METHOD.ALL:
        prob = depth / bases_per_frag
        prob = prob / 2 # For both forward and reverse
    
    # Calculate (distribution parameters)
    if depth_method == DIST.GAMMA:
        if depth_param < 0:
            flag = True
            depth_param = -depth_param
        else: flag = False
        beta = (prob / depth_param) ** 0.5
        alpha = prob / beta
        depth_param = [alpha, beta, flag]
    elif depth_method == DIST.UNIFORM:
        depth_param = 0
        while prob > 1:
            depth_param = += 1
            prob -= 1
    
    if frag_len_method == DIST.GAMMA:
        if frag_len_param < 0:
            flag = True
            frag_len_param = -frag_len_param
        else: flag = False
        beta = (frag_len / frag_len_param) ** 0.5
        alpha = frag_len / beta
        frag_len_param = [alpha, beta, flag]
    elif frag_len_method == DIST.UNIFORM:
        lower = frag_len - frag_len_param
        upper = frag_len + frag_len_param
        frag_len_param = range(lower, upper+1)
        frag_len = 0
    
    # Calculations (maximum length)
    if frag_len_method == DIST.NORMAL: max_len = 5 * frag_len
    if frag_len_method == DIST.GAMMA: max_len = 5 * frag_len
    if frag_len_method == DIST.UNIFORM: max_len = 5 * frag_len + frag_len_param
    
    # I/O setup
    f = Chr_FASTA_Reader(path_in, True)
    if type(output) == str: o = open(output, "w")
    else: o = output
    
    # Setup
    current_index = 0
    counter = 0
    previous = []
    len_previous = 0
    unfinished_frags = [] # [goal, current, seq, name]
    
    # Main Loop
    while not f.End():
        f.Read()
        
        current_index += 1
        
        n = f.Get_Current()
        n_ = N_SEQ.Get_Complement(n)
        
        previous.append(n_)
        if len(previous) > max_len: previous.pop(0)
        else: len_previous += 1
        
        # Unfinished forward frags
        for list_ in unfinished_frags:
            list_[1] += 1
            list_[2] += n
            if list_[0] == list_[1]:
                count += 1
                total += list_[0]
                s = ">" + list_[3] + "\n" + list_[2] + "\n"
                o.write(s)
        for list_ in unfinished_frags:
            if list_[0] == list_[1]: unfinished_frags.remove(list_)
        
        # Calculate numbers
        forwards = Custom_Random_Distribution(prob, depth_method, depth_param)
        backwards = Custom_Random_Distribution(prob, depth_method, depth_param)
        
        # Individual frags
        while forwards > 0:
            counter += 1
            length = Custom_Random_Distribution(frag_len, frag_len_method,
                    frag_len_param)
            end = current_index + length
            name = Generate_Frag_Name(counter, current_index, STR__forward, end)
            unfinished_frags.append([length, 1, n, name])
            forwards -= 1
        
        while backwards > 0:
            length = Custom_Random_Distribution(frag_len, frag_len_method,
                    frag_len_param)
            end = current_index - length
            if end > 0:
                counter += 1
                count += 1
                total += length
                index = 0-length
                bases = previous[index:]
                seq = "".join(bases)
                name = Generate_Frag_Name(counter, current_index, STR__reverse,
                        end)
                s = ">" + name + "\n" + seq + "\n"
                o.write(s)
            backwards -= 1
    
    # Close file
    if type(output) == str: o.close()
    
    # Return
    return [count, total]

def Report_Metrics(outcomes):
    """
    Print a report into the command line interface of the total number of
    fragments generated, and the average length.
    
    @outcomes
            (list<[int,int]>)
            A list of sublists, each containing two integers, a fragment count,
            and the total number of basepairs in the fragments.
    
    Report_Metrics(list<[int,int]>) -> None
    """
    # Can potentially be expanded to include more metrics in the future
    # Get results
    count = 0
    total = 0
    for outcome in outcomes:
        count += outcome[0]
        total += outcome[1]
    if count: average = int((float(total)/count) + 0.5)
    else: average = 0
    # Strings
    str_count = str(count)
    str_average = str(average)
    # Padding and formatting
    max_size = max([len(str_count), len(str_average)])
    str_count = Pad_Str(str_count, max_size, " ", 0)
    str_average = Pad_Str(str_average, max_size, " ", 0)
    # Print
    PRINT.printM(STR__metrics.format(C = str_count, A = str_average))

def Custom_Random_Distribution(mean, method, param, must_positive=False):
    """
    Generate a random number.
    
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
            parameters will be (@mean+@param)
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
                    Gamma distribution, and a flag indicating whether to
                    flip-shift the result or not.
                UNIFORM:
                    (list/int)
                    If @mean is 0, then @param is a list of values, one of which
                    will be chosen at random with equal probability.
                    If @mean is not zero, then @param is the number to add
    @must_positive
            (bool)
            Whether or not to forcibly make
    
    Custom_Random_Distribution(int/float, int, *, bool) -> int/float
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
            if param[2]: r = -r + 2
        r = int(r+0.5)
    if must_positive:
        if r < 0: r = -r
    return r
    
def Generate_Frag_Name(counter, start, direction, end):
    """
    Generate a name for a DNA fragment based on how many fragments have already
    been generated, and the coordinates and directionality of the fragment.
    """
    sb = Pad_Str(str(counter), ID_SIZE, "0", 0)
    sb = sb + "__" + str(start) + "_" + direction + "_" + str(end)
    return sb

