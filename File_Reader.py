"""
FILE READER
(version 1.0)
by Angelo Chan

This module contains a Class designed to be the base class on which
type-specific file readers are to be based.
"""

# Lists ########################################################################

LIST__newline = ["\n", "\r", "\n\r", "\r\n"]



# Classes ######################################################################

class File_Reader:
    """
    The File Reader is a generic file reader designed to be extended to specific
    file types.
    
    Designed for the following use:
        
        f = File_Reader()
        f.Open("F:/Filepath.h")
        while not f.End():
            f.Read(
            # Your code
            current_element = f.Get()
        f.Close()
    
    Methods and factors which require rewriting in all subclasses:
        
        self.empty_element
        
        self._MSG__object_type
        self._MSG__units_of_measure
        
        self.Copy_Element(element)
        self._get_next_element() OR self._read()
        self.Is_Empty_Element(element)
        self.Get_Size() # If used
    """
    
    # Minor Configurations #####################################################
    
    empty_element = None # Change this
    
    # Minor Configurations #####################################################
    
    _CONFIG__print_errors = True
    _CONFIG__print_progress = True
    _CONFIG__print_metrics = True

    # Strings ##################################################################
    
    _MSG__invalid_file_path = "Invalid file path."
    
    _MSG__unspecified_file_path = "No file path has been specified."
    
    _MSG__open_file_fail = "No file was opened."
    
    _MSG__new_path_fail = "The formerly set file path will be used instead."
    
    _MSG__new_path_set = "The file path has been set to \"{PATH}\"."
    
    _MSG__unexpected_error = "An unexpected error occurred."
    
    _MSG__file_opened_message = "File \"{F}\" was successfully opened."
    
    _MSG__file_closed_message = "The currently opened file has been closed."
    
    _MSG__same_file_path = "The new file path is the same as the currently "\
            "stored one."
    
    _MSG__EOF_reached = "The end of file has been reached."
    
    _MSG__EOF_reached_already = "The end of file has been reached already."
    
    _MSG__init_message = "Preparing File Reader..." # Overwrite this
    
    _MSG__method_not_implemented = "WARNING: A critical method has not been "\
            "implemented."
    
    # Constructor & Destructor #################################################
    
    def __init__(self, file_path="", auto_open=False):
        """
    `   Creates a File Reader object. The filepath will be tested if a
        filepath is supplied.
        """
        self.printP(self._MSG__init_message)
        self.size = 0
        self.current_index = -1
        self.file_path = ""
        self.file_opened = False
        self.file = False
        self.current_element = self.next_element = self.empty_element
        self.EOF = True
        if file_path:
            self.Set_New_Path(file_path)
            if auto_open: self.Open()
    
    def __del__(self):
        """
        Destructor code ensures files are closed after use.
        """
        if self.file_opened: self.Close()
    
    # Property Methods #########################################################
    
    def __len__(self):
        """
        Return the number of elements in the file. Exactly what constitutes an
        depends entirely on the file format.
        """
        if self.file_path:
            return self.Get_Size()
        self.printE(self._MSG__unspecified_file_path)
        return 0
    
    def __str__(self):
        """
        Return a string representation of the currently selected file.
        """
        sb = ("<{T} Object> - ".format(T = self._MSG__object_type) +
                ["CLOSED", "OPENED"][self.file_opened] + "\n\t")
        if self.file_path: sb += "PATH:\t\"{P}\"".format(P = self.file_path)
        else: sb += "(No File Path specified.)"
        sb += "\n\tSIZE:\t{S} {E}".format(S = self.Get_Size(),
                E = self._MSG__units_of_measure)
        return sb
     
    def Get_Size(self):
        """
        Return the number of elements in the file. Exactly what constitutes an
        element depends entirely on the file format.
        """
        if self.size != 0: return self.size
        if self.file_path:
            count = 0
            f = open(self.file_path, "U")
            for line in f: count += 1
            f.close()
            return count
        return 0
    
    def Copy_Element(self, element):
        """
        Return a copy of [element] which can be modified without affecting the
        original.
        """
        print(self._MSG__method_not_implemented)
        return element

    def End(self):
        """
        Return True if the end of file has been reached.
        Return False otherwise.
        """
        return self.EOF
    
    def Get_Extension(self, file_path=""):
        """
        Return the file extension of the specified file. Use the stored file
        name if no file path was specified.\
        Return an empty string if no extension could be found.
        """
        if not file_path: file_path = self.file_path
        rightmost_period = file_path.rfind(".")
        if rightmost_period == -1: return ""
        rightmost_fslash = file_path.rfind("/")
        rightmost_bslash = file_path.rfind("\\")
        rightmost_slash = max([rightmost_fslash, rightmost_bslash])
        if rightmost_period < rightmost_slash: return ""
        return file_path[rightmost_period+1:]
    
    
    
    # File I/O Methods #########################################################
    
    def __set_path(self, file_path):
        """
        Set the stored file path to the given path if the file specified can be
        found and opened.
        """
        try:
            f = open(file_path, "U")
            f.close()
            self.file_path = file_path
            return 0
        except:
            self.printE(self._MSG__invalid_file_path)
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
                self.file = open(self.file_path, "U")
                self.__new()
                self.printP(self._MSG__file_opened_message.format(
                        F=self.file_path))
        else: self.printP(self._MSG__same_file_path)
    
    def __new(self):
        """
        Reset the state indicators when a new file is opened.
        """
        self.file_opened = True
        self.EOF = False
        self.next_element = self.Copy_Element(self.empty_element)
        self.Reset_Index()
        self.Read_Header()
        self.Read()
    
    def Close(self):
        """
        Close the object's file if the file is open. Do nothing if the object
        does not have a file open.
        """
        if self.file_opened:
            self.printP(self._MSG__file_closed_message)
            self.size = 0
            self.current_index = -1
            self.file.close()
    
    def State(self):
        """
        Print the string representation of this object.
        """
        print(self.__str__())
    
    def Reset(self):
        """
        Sends the reading pointer back to the start of the file.
        """
        temp = self.file_path
        self.file_path = False
        self.Open(temp)
    
    def IsClosed(self):
        """
        Return whether or not the file is closed. If there is no file, this will
        also return True.
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
    
    # Content Reading Methods ##################################################
    
    def Get(self):
        """
        Get() <==> Get_Current()
        """
        return self.Get_Current()
    
    def Get_Current(self):
        """
        Return a copy of the current element.
        """
        return self.Copy_Element(self.current_element)
    
    def Get_Current_SOFT(self):
        """
        Return the current element directly. Allows the current element to be
        modified by external code. Caution is advised.
        """
        return self.current_element

    def Next(self):
        """
        Next() <==> Read()
        """
        self.Read()
    
    def Read_Header(self):
        """
        A one-off file reading procedure for dealing with file headers and the
        like.

        May not be relevant to all files.
        """
        pass
    
    def Read(self, number=1):
        """
        Set the stored element to the next element in the file, or to the
        element [number] places down the track if [number] is given and greater
        than 0.
        """
        if not self.EOF:
            while not self.EOF and number > 0:
                self._read()
                number -= 1
        else:
            self.printP(self._MSG__EOF_reached_already)
    
    def _read(self):
        """
        Pushes the buffered element to become the "current" one. A copy of the
        "current" element can be accessed and used by the user. The next
        element is then read and buffered.

        When a file is first open, and the Read() method (and by extension,
        this method has only been implicitly called once, and not yet been
        explicitly called, then the very first element of file will be read into
        the "next" buffer, but the "current" element will be empty. Only after
        Read() has been explicitly called will there be a "current" element to
        access.
        
        The EOF flag is not set to True when the last element of the file is
        read into the buffer. It is only set to True when the last element of
        the file is pushed to the "current" element and no new element can be
        found for the buffer. Users will still be able to access the last
        element of the file since it will be the "current" element.
        """
        self.current_element = self.next_element
        self.next_element = self._get_next_element()
        if self.Is_Empty_Element(self.next_element):
            self.next_element = self.empty_element
            self.EOF = True
            self.printP(self._MSG__EOF_reached)
        else:
            self.current_index += 1
    
    def _get_next_element(self):
        """
        STUB. Please add code for your implementation.
        """
        print(self._MSG__method_not_implemented)
        return self.empty_element()
    
    def Is_Empty_Element(self, element):
        """
        STUB. Possibly modify code for your implementation.
        """
        print(self._MSG__method_not_implemented)
        if element == self.empty_element:
            return True
        return False
    
    def Reset_Index(self):
        """
        STUB. Possibly modify code for your implementation.
        """
        self.current_index = -1
    
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


