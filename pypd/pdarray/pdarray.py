import pylibpd as pd
from array import array

class PDArray(array):
    def __new__(cls, name):
        size = pd.libpd_arraysize(name)
        if size < 0:
            raise ValueError('"%s" is not a valid array' %name)
        a = array.__new__(cls, 'f', range(size))
        a.__name = name
        pd.libpd_read_array(a, name, 0, size)
        return a

    def getName(self):
        return self.__name

    def copy(self, buf, send=True):
        self[:] = buf
        if send:
            self.send()

    def send(self):
        return pd.libpd_write_array(self.__name, 0, self, len(self))
        