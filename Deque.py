"""
DEQUE
(version 1.0)
by Angelo Chan

A simple implementation of Deque.

Originally intended as a time-efficient buffer system for storing data for data
reading systems.
"""

# Imported Modules #############################################################

import random as Random



# Classes ######################################################################

class Deque():
    """
    A simple Deque implementation.
    """
    
    # Constructor & Destructor #################################################
    
    def __init__(self, size, blanks=""):
        """
    `   Initializes the Deque object.
        """
        self._current_index = -1
        self._size = size
        self._blanks = blanks
        self._data = [blanks] * size
    
    # Property Methods #########################################################
    
    def __len__(self):
        """
        Return the number of non-blank data values in the Deque.
        """
        count = 0
        for i in self._data:
            if i != self._blanks: count += 1
        return count
    
    def Size(self):
        """Return the size of the Deque."""
        return self._size

    def Max(self):
        """Return the size of the Deque."""
        return self._size

    def Get_Size(self):
        """Return the size of the Deque."""
        return self._size

    def Max_Size(self):
        """Return the size of the Deque."""
        return self._size
    
    def __str__(self):
        """
        Return a string representation of the Deque.
        """
        sb = "DEQUE OBJECT:\n\tCurrent index: "
        sb += str(self._current_index)
        sb += "\n"
        sb += str(self._data)
        return sb
    
    def __repr__(self):
        """
        Return a string representation of the Deque.
        """
        return self.__str__()
    
    
    
    # Index Methods ############################################################
    
    def Get_Index(self):
        """Return the current index."""
        return self._current_index
    
    def Shift_Index(self, change):
        """Increase or decrease the current index by the specified amount."""
        self._current_index += change
        while self._current_index < 0:
            self._current_index += self._size
        while self._current_index >= self._size:
            self._current_index -= self._size
    
    # Data Methods #############################################################
    
    def Add(self, value):
        """Return the current index."""
        self.Shift_Index(1)
        self._data[self._current_index] = value

    def Poll(self, number):
        """
        Return the last [number] of inserted values.
        
        Poll(int) -> list<X>
        """
        # Initial index calculations
        size = self._size
        start = self._current_index
        end = start - number
        #
        if end >= 0:
            return self._data[start:end:-1]
        else:
            end = -end
            lb = self._data[start::-1]
            while end > size:
                lb += self._data[-1::-1]
                end -= size
            end = size - end
            lb += self._data[-1:end:-1]
            return lb

    def PollR(self, number):
        """
        Return the last [number] of inserted values, in reversed order.
        
        PollR(int) -> list<X>
        """
        return self.Poll(number)[::-1]


