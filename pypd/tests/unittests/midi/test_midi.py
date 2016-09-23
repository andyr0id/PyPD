"""

Test MIDI events

    >>> from pypd import PD
    >>> pd = PD(numOutChannels=1)
    >>> dz = pd.openPatch('midisynth.pd', '../../../../patches')
    >>> pd.play()
    >>> x, a, s, r = testMIDIEvents(pd)
    >>> x[:16]
    array('h', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    >>> a[:16]
    array('h', [0, -3, -7, -10, -13, -16, -19, -22, -25, -27, -30, -32, -34, -36, -37, -39])
    >>> s[:16]
    array('h', [2648, -2605, -2552, -2499, -2446, -2393, -2340, -2287, -2234, -2181, -2128, -2075, -2022, -1969, -1916, -1863])
    >>> r[-16:]
    array('h', [-3, -3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, 0])


"""

from pypd import PDMidiIn
from pypd.utils import getBuffer
from pypd.tests import runModuleTestSuite

def testMIDIEvents(pd):
    midi = PDMidiIn()

    inbuf = getBuffer(pd)

    # should be slience as there's no event
    out1 = pd.process(inbuf)[:]

    # trigger a noteOn
    midi.noteOn(69)
    # catch the start of the envelope
    out2 = pd.process(inbuf)[:]
    # process a bit of time
    for i in xrange(int(1 * pd.getSampleRate())):
        out3 = pd.process(inbuf)[:]
    # trigger a noteOff
    midi.noteOff(69)
    # catch the end of the envelope
    for i in xrange(int(0.01012 * pd.getSampleRate())):
        out4 = pd.process(inbuf)[:]

    return out1, out2, out3, out4


if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))