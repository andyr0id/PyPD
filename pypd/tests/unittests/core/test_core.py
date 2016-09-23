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

    >>> dz = pd.openPatch('sin.pd', '../../../../patches')
    >>> dz
    1003
    >>> pd.closePatch(dz)

Run a basic patch

    >>> pd.setChannels(1, 1)
    >>> dz = pd.openPatch('sin.pd', '../../../../patches')
    >>> pd.play()
    >>> from pypd.utils import getBuffer
    >>> inbuf = getBuffer(pd)
    >>> out = pd.process(inbuf)
    >>> out[:10]
    array('h', [0, -1026, -2052, -3076, -4097, -5114, -6126, -7131, -8130, -9121])
    >>> pd.stop()
    >>> pd.closePatch(dz)

"""

from pypd.tests import runModuleTestSuite

if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))