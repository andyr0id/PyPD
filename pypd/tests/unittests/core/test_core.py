"""

Test the creation of the main object

    >>> from pypd import PD
    >>> pd = PD()
    >>> pd
    <PD object>

Test changing the channels

    >>> pd.setChannels(8, 8)
    >>> pd.getChannels()
    (8, 8)
    >>> pd.setChannels(1, 1)
    >>> pd.getChannels()
    (1, 1)

Test setting the DSP state

    >>> pd.isPlaying()
    False
    >>> pd.play()
    >>> pd.isPlaying()
    True
    >>> pd.stop()
    >>> pd.isPlaying()
    False

Open / close patch

    >>> dz = pd.openPatch('sin.pd')
    >>> dz
    1003
    >>> pd.closePatch(dz)

Run a basic patch

    >>> pd.setChannels(1, 1)
    >>> dz = pd.openPatch('sin.pd')
    >>> pd.play()
    >>> inbuf = getBuffer(pd)
    >>> out = pd.process(inbuf)
    >>> out[:10]
    array('h', [32767, 32750, 32702, 32621, 32509, 32364, 32188, 31981, 31741, 31471])

"""

from pypd.tests import runModuleTestSuite
import array

def getBuffer(pd, inbuf=True):
    outch, inch = pd.getChannels()
    if inbuf:
        ch = inch
    else:
        ch = outch
    return array.array(pd.getTypecode(),
        '\x00\x00' * ch * pd.getBlocksize() * pd.ticksPerBuffer)

if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))