import pylibpd as pd
from array import array

class PDArray(array):
    """Allows manipulation of a PD array as a python array. Slicing and setting are suppoted.
    """
    def __new__(cls, name):
        size = pd.libpd_arraysize(name)
        if size < 0:
            raise ValueError('"%s" is not a valid array' %name)
        a = array.__new__(cls, 'f', range(size))
        a.__name = name
        pd.libpd_read_array(a, name, 0, size)
        return a

    def __setitem__(self, key, value):
        r = super(PDArray, self).__setitem__(key, value)
        self.send()
        return r

    def __setslice__(self, a, b, v):
        r = super(PDArray, self).__setslice__(a, b, v)
        self.send()
        return r

    def getName(self):
        return self.__name

    def send(self):
        return pd.libpd_write_array(self.__name, 0, self, len(self))
        