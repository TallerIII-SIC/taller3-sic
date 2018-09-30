class CircularList:
    """List which last node is connected with the first one."""

    def __init__(self, size):
        self.size = size
        self._data = list()

    def __len__(self):
        """Returns the number of elements in the list."""
        return len(self._data)

    def __getitem__(self, index):
        """Returns the element in the required index. If the index is
        greater or equal than the list size, it has a circular behavior."""
        if index < len(self.data):
            return self._data[index % self.size]
        else:
            return None

    def __delitem__(self, index):
        """Removes the element in the required index. If the index is
        greater or equal than the list size, it has a circular behavior."""
        del self._data[index % self.size]

    def __setitem__(self, index, value):
        """Sets an element in the required index. If the index is
        greater or equal than the list size, it has a circular behavior."""
        self._data[index % self.size] = value
        return self._data[index % self.size]

    def append(self, value):
        """Pushes an element in the back. Since the list is circular,
        when the list is full it removes the element in the top."""
        if len(self._data) == self.size:
            self._data.pop(0)

        self._data.append(value)

    def __repr__(self):
        """Returns an ASCII representation of the internal list."""
        return self._data.__repr__() 
