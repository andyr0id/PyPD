"""

Test MIDI events

    >>> from pypd import PD
    >>> pd = PD(numOutChannels=1)
    >>> dz = pd.openPatch('midisynth.pd', '../../../../patches')
    >>> pd.play()
    >>> x, a, s, r = testMidiIn(pd)
    >>> x[:16]
    array('h', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    >>> a[:16]
    array('h', [0, -3, -7, -10, -13, -16, -19, -22, -25, -27, -30, -32, -34, -36, -37, -39])
    >>> s[:16]
    array('h', [2648, -2605, -2552, -2499, -2446, -2393, -2340, -2287, -2234, -2181, -2128, -2075, -2022, -1969, -1916, -1863])
    >>> r[-16:]
    array('h', [-3, -3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, 0])
    >>> pd.closePatch(dz)
    >>> dz = pd.openPatch('midisend.pd', '../../../../patches')
    >>> testMidiOut(pd)
    (60, 0, 0)
    (60, 127, 0)


"""

from pypd import PDMidiIn, PDMidiOut
from pypd.utils import getBuffer
from pypd.tests import runModuleTestSuite

def testMidiIn(pd):
    midiIn = PDMidiIn()
    inbuf = getBuffer(pd)

    # should be slience as there's no event
    out1 = pd.process(inbuf)[:]

    # trigger a noteOn
    midiIn.noteOn(69)
    # catch the start of the envelope
    out2 = pd.process(inbuf)[:]
    # process a bit of time
    for i in xrange(int(1 * pd.getSampleRate())):
        out3 = pd.process(inbuf)[:]
    # trigger a noteOff
    midiIn.noteOff(69)
    # catch the end of the envelope
    for i in xrange(int(0.01012 * pd.getSampleRate())):
        out4 = pd.process(inbuf)[:]

    return out1, out2, out3, out4

def noteCallback(num, vel, ch):
    print(num, vel, ch)

def testMidiOut(pd):
    midiOut = PDMidiOut()
    midiOut.noteOn(noteCallback)
    midiOut.noteOff(noteCallback)
    inbuf = getBuffer(pd)

    # process a bit of time
    for i in xrange(512):
        out = pd.process(inbuf)[:]

if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))