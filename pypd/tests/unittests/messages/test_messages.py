"""

Test sending and receiving messages

    >>> from pypd import PD
    >>> pd = PD(numOutChannels=1)
    >>> patchesDir = getPatchesDir()
    >>> dz = pd.openPatch('messages.pd', patchesDir)
    >>> testMessages(pd)
    print: print: 42
    <BLANKLINE>
    float: eggs 42.0
    print: print: symbol
    print:  
    print: hello
    print: 
    <BLANKLINE>
    symbol:
    ('eggs', 'hello')
    print: print: list
    print:  
    print: test
    print:  
    print: 1
    print:  
    print: foo
    print:  
    print: 2
    print: 
    <BLANKLINE>
    >>> pd.release()

"""

from pypd.messages import PDIn, PDOut
from pypd.tests import runModuleTestSuite
from pypd.tests.testutils import getPatchesDir

def printCallback(val):
    print('print: %s' % val)

def floatCallback(name, val):
    print('float: %s\t%r' % (name, val))

def listCallback(name, val):
    print('list: %s' % name)
    print(val)

def symCallback(*args):
    print('symbol:')
    print(args)

def messageCallback(*args):
    print('symbol:')
    print(args)

def testMessages(pd):
    pdIn = PDIn()
    pdOut = PDOut()
    pdOut.prnt(printCallback)
    pdOut.float(floatCallback)
    pdOut.list(listCallback)
    pdOut.symbol(symCallback)
    pdOut.message(messageCallback)
    pdOut.subscribe('eggs')

    pdIn.float('spam', 42)
    pdIn.symbol('spam', 'hello')
    pdIn.list('spam', ['test', 1, 'foo', 2])


if __name__ == '__main__':
    runModuleTestSuite(__import__('__main__'))