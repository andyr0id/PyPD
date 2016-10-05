"""

Test sending and receiving arrays

    >>> from pypd import PD
    >>> pd = PD(numOutChannels=1)
    >>> patchesDir = getPatchesDir()
    >>> dz = pd.openPatch('array.pd', patchesDir)
    >>> from pypd.pdarray import PDArray
    >>> a = PDArray('array1')

Test array name set correctly

    >>> a.getName()
    'array1'

Test array length set correctly

    >>> len(a)
    64

Test array content set correctly

    >>> a[:5]
    array('f', [0.0428570993244648, 0.0857141986489296, 0.21428599953651428, 0.2571429908275604, 0.2857140004634857])

Test array copying

    >>> buf = array.array('f', map(lambda x : x / 64.0, range(len(a))))
    >>> a[:] = buf
    >>> a == buf
    True

Test array was sent to PD

    >>> c = PDArray('array1')
    >>> c == buf
    True
    >>> pd.release()

"""

import array
from pypd.tests import runModuleTestSuite
from pypd.tests.testutils import getPatchesDir


if __name__ == '__main__':
    runModuleTestSuite(__import__('__main__'))