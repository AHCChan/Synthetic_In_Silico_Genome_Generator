"""
FILE READER
(version 1.0)
by Angelo Chan

This module contains a Class designed to be the base class on which
type-specific file writers are to be based.
"""

# Imported Modules #############################################################

import os



# Lists ########################################################################

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]



# Classes ######################################################################

class File_Writer:
    """
    The File Reader is a generic file reader designed to be extended to specific
    file types.
    
    Methods and factors which require rewriting in all subclasses:
        
        self._MSG__object_type
        
        self.Write()
    """
    
    # Major Configurations #####################################################
    
    _CONFIG__overwrite_prevent = True # Completely prevent overwritting
    #                                    existing files
    _CONFIG__overwrite_confirm = True # Check to confirm overwritting existing
    #                                    files
    
    # Minor Configurations #####################################################
    
    _CONFIG__print_errors = True
    _CONFIG__print_progress = True
    _CONFIG__print_metrics = True

    EOL = "\n"

    # Strings ##################################################################
    
    _MSG__invalid_string = "\nInvalid string:\n\t{S}\mOld NEWLINE character "\
            "will be used."
    
    _PROMPT__confirm_overwrite = "\nFile already exists:\n\t{F}\nDo you wish "\
            "to overwrite it? (y/n):"

    _MSG__overwrite_forbid = "\nERROR: You specified an output file which "\
            "already exists and the administrator\nfor this program has "\
            "forbidden all overwrites. Please specify a different\noutput file"\
            ", move the currently existing file, or configure the underlying\n"\
            "File Writer module."
    _MSG__overwrite_accept = "\nWARNING: Existing files will be overwritten."
    _MSG__overwrite_decline = "\nThe user has opted not to overwrite existing "\
        "files.\nThe program will now terminate."
    
    _MSG__unspecified_file_path = "No file path has been specified."
    
    _MSG__open_file_fail = "No file was opened."
    
    _MSG__new_path_fail = "The formerly set file path will be used instead."
    
    _MSG__new_path_set = "The file path has been set to \"{PATH}\"."
    
    _MSG__unexpected_error = "An unexpected error occurred."
    
    _MSG__file_opened_message = "File \"{F}\" was successfully opened."
    
    _MSG__file_closed_message = "The currently opened file has been closed."
    
    _MSG__same_file_path = "The new file path is the same as the currently "\
            "stored one."
    
    _MSG__init_message = "Preparing File Writer..." # Overwrite this
    
    _MSG__method_not_implemented = "WARNING: A critical method has not been "\
            "implemented."
    
    # Constructor & Destructor #################################################
    
    def __init__(self, file_path="", auto_open=False):
        """
    `   Creates a File Writer object. The filepath will be tested if a
        filepath is supplied.
        """
        self.printP(self._MSG__init_message)
        self.file_path = ""
        self.file_opened = False
        self.file = False
        if file_path:
            self.Set_New_Path(file_path)
            if auto_open: self.Open()
    
    def __del__(self):
        """
        Destructor code ensures files are closed after use.
        """
        if self.file_opened: self.Close()
    
    
    
    # Parameter Configuration Methods ##########################################
        
    def Overwrite_Forbid(self):
        """
        Set the program parameters such that overwriting existing files is
        strictly forbidden.
        """
        self._CONFIG__overwrite_prevent = True
        self._CONFIG__overwrite_confirm = True
        
    def Overwrite_Confirm(self):
        """
        Set the program parameters such that users are asked if they wish to
        overwrite existing files.
        """
        self._CONFIG__overwrite_prevent = False
        self._CONFIG__overwrite_confirm = True
        
    def Overwrite_Allow(self):
        """
        Set the program parameters such that overwriting existing files is
        automatically permitted.
        """
        self._CONFIG__overwrite_prevent = False
        self._CONFIG__overwrite_confirm = False
        
    def Set_Newline(self, string):
        """
        Change what to use as a newline character
        """
        if type(string) == str:
            self.EOL = string
        else:
            self.printE(self._MSG__invalid_string)
    
    
    
    # Property Methods #########################################################
        
    def __str__(self):
        """
        Return a string representation of the currently selected file.
        """
        sb = ("<{T} Object> - ".format(T = self._MSG__object_type) +
                ["CLOSED", "OPENED"][self.file_opened] + "\n\t")
        if self.file_path: sb += "PATH:\t\"{P}\"".format(P = self.file_path)
        else: sb += "(No File Path specified.)"
        return sb
    
    
    
    # File I/O Methods #########################################################
    
    def __set_path(self, file_path):
        """
        Set the stored file path to the given path if the file specified can be
        found and opened.
        """
        # Existing file
        valid = os.path.isfile(file_path)    
        if valid:
            if self._CONFIG__overwrite_prevent:
                self.printE(self._MSG__overwrite_forbid)
                return 1
            elif self._CONFIG__overwrite_confirm:
                confirm = raw_input(self._PROMPT__confirm_overwrite.format(
                        F = file_path))
                if confirm not in LIST__yes:
                    self.printE(self._MSG__overwrite_decline)
                    return 1
            self.printM(self._MSG__overwrite_accept)
            self.file_path = file_path
        # Attempt to create
        try:
            f = open(file_path, "w")
            f.close()
            os.remove(file_path)
            self.file_path = file_path
            return 0
        except Exception as e:
            self.printE(e)
        return 1
    
    def Set_New_Path(self, new_path=""):
        """
        Set a new stored file path if the path is specified and can be found and
        opened.
        """
        if new_path:
            i = self.__set_path(new_path)
            if i == 0:
                self.printP(self._MSG__new_path_set.format(PATH = new_path))
            elif i == 1:
                self.printE(self._MSG__new_path_fail)
            else:
                self.printE(self._MSG__unexpected_error)
    
    def Open(self, new_path=""):
        """
        Attempts to open a file. If a file path is not specified, the stored
        file path will be used instead.
        """
        if new_path != self.file_path:
            self.Set_New_Path(new_path)
            if not self.file_path:
                self.printE(self._MSG__unspecified_file_path)
                self.printE(self._MSG__open_file_fail)
            else:
                if self.file_opened: self.Close()
                self.file = open(self.file_path, "w")
                self.__new()
                self.printP(self._MSG__file_opened_message.format(
                        F=self.file_path))
        else: self.printP(self._MSG__same_file_path)
    
    def __new(self):
        """
        Reset the state indicators when a new file is opened.
        """
        self.file_opened = True
    
    def Close(self):
        """
        Close the object's file if the file is open. Do nothing if the object
        does not have a file open.
        """
        if self.file_opened:
            self.printP(self._MSG__file_closed_message)
            self.file.close()
    
    def State(self):
        """
        Print the string representation of this object.
        """
        print(self.__str__())
    
    def Reset(self):
        """
        Attempt to wipe the file and start over again.
        """
        temp = self.file_path
        self.file_path = False
        self.Open(temp)
    
    def IsClosed(self):
        """
        Return whether or not the file is closed. If there is no file, return
        True.
        """
        if type(self.file) == file: return self.file.closed
        return True
    
    def IsOpen(self):
        """
        Return whether or not the file is open. If there is no file, return
        True.
        """
        if type(self.file) == file: return not self.file.closed
        return False
    
    
    
    # File Writing Methods #####################################################
    
    def Write(self, string):
        """
        STUB. Please add code for your implementation.
        """
        print(self._MSG__method_not_implemented)

    def Newline(self):
        """
        STUB. Please add code for your implementation.
        """
        print(self._MSG__method_not_implemented)
    
    
    
    # Controlled Print Methods #################################################
    
    def printE(self, string):
        """
        Print the given string if the class variable for printing error
        messages is set to True.
        """
        if self._CONFIG__print_errors: print(string)
    
    def printP(self, string):
        """
        Print the given string if the class variable for printing progress
        updates is set to True.
        """
        if self._CONFIG__print_progress: print(string)
    
    def printM(self, string):
        """
        Print the given string if the class variable for printing metrics
        reports is set to True.
        """
        if self._CONFIG__print_metrics: print(string)
    
    def Toggle_Printing_E(self, toggle_to=None):
        """
        Toggle whether or not error messages are printed. It is possible to
        specify what state to set the configuration to.
        """
        if type(toggle_to) != bool:
            self._CONFIG__print_errors = not self._CONFIG__print_errors
        else: self._CONFIG__print_errors = toggle_to
    
    def Toggle_Printing_P(self, toggle_to=None):
        """
        Toggle whether or not progress updates are printed. It is possible to
        specify what state to set the configuration to.
        """
        if type(toggle_to) != bool:
            self._CONFIG__print_progress = not self._CONFIG__print_progress
        else: self._CONFIG__print_progress = toggle_to
    
    def Toggle_Printing_M(self, toggle_to=None):
        """
        Toggle whether or not metrics reports are printed. It is possible to
        specify what state to set the configuration to.
        """
        if type(toggle_to) != bool:
            self._CONFIG__print_metrics = not self._CONFIG__print_metrics
        else: self._CONFIG__print_metrics = toggle_to
    
    def Enable_All_Messages(self):
        """
        Make the file reader print all error messages, updates, and metrics.
        """
        self._CONFIG__print_errors = True
        self._CONFIG__print_progress = True
        self._CONFIG__print_metrics = True
    
    def Disable_All_Messages(self):
        """
        Make the file reader not print any error messages, updates, or metrics.
        """
        self._CONFIG__print_errors = False
        self._CONFIG__print_progress = False
        self._CONFIG__print_metrics = False


