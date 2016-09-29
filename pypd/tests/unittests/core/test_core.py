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

    >>> pd.isDSPOn()
    False
    >>> pd.dspOn()
    >>> pd.isDSPOn()
    True
    >>> pd.dspOff()
    >>> pd.isDSPOn()
    False

Open / close patch

    >>> patchesDir = getPatchesDir()
    >>> dz = pd.openPatch('sin.pd', patchesDir)
    >>> isinstance(dz, int)
    True
    >>> pd.closePatch(dz)

Run a basic patch

    >>> pd.setChannels(1, 1)
    >>> dz = pd.openPatch('sin.pd', patchesDir)
    >>> pd.dspOn()
    >>> from pypd.utils import getBuffer
    >>> inbuf = getBuffer(pd)
    >>> out = pd.process(inbuf)
    >>> out[:10]
    array('h', [0, -1026, -2052, -3076, -4097, -5114, -6126, -7131, -8130, -9121])
    >>> pd.dspOff()
    >>> pd.closePatch(dz)
    >>> pd.release()

"""

from pypd.tests import runModuleTestSuite
from pypd.tests.testutils import getPatchesDir

if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))