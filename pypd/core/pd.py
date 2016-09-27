import array
import pylibpd as pd
from pypd.utils import getBuffer, getRawBuffer

process_functions = {
    'h': pd.libpd_process_short,
    'f': pd.libpd_process_float,
    'd': pd.libpd_process_double,
}

class PD(object):
    def __init__(self,
            numOutChannels=2, numInChannels=0,
            sampleRate=44100, ticksPerBuffer=1,
            typecode='h'):

        self.setChannels(numOutChannels, numInChannels, False)
        self.setSampleRate(sampleRate, False)
        self.ticksPerBuffer = ticksPerBuffer
        self.setTypecode(typecode, False)
        self.__blocksize = pd.libpd_blocksize()
        self.__dspState = 0
        self.init()
        super(PD, self).__init__()

    def __str__(self):
        return '<PD object>'

    def __repr__(self):
        return str(self)

    def setChannels(self, numOutChannels, numInChannels, reinit=True):
        self.__outChannels = numOutChannels
        self.__inChannels = numInChannels
        if reinit:
            self.init()

    def getChannels(self):
        return (self.__outChannels, self.__inChannels)

    def setSampleRate(self, sampleRate, reinit=True):
        self.__sampleRate = sampleRate
        if reinit:
            self.init()

    def getSampleRate(self):
        return self.__sampleRate

    def setTypecode(self, typecode, reinit=True):
        global process_functions
        if typecode not in process_functions:
            raise ValueError('%s not a valid format' % typecode)
        self.__typecode = typecode
        if reinit:
            self.init()

    def getTypecode(self):
        return self.__typecode

    def setDSPState(self, state=1):
        self.__dspState = state
        pd.libpd_compute_audio(state)

    def getDSPState(self, state=1):
        return self.__dspState

    def getBlocksize(self):
        return self.__blocksize

    def init(self):
        self.initBuffers()
        self.initAudio()

    def initBuffers(self):
        self.__outbuf = getBuffer(self, 'output')
        self.__rawOutbuf = getRawBuffer(self, 'output')

    def initAudio(self):
        return pd.libpd_init_audio(self.__inChannels, self.__outChannels, self.__sampleRate)

    def openPatch(self, patch, dir = '.'):
        return pd.libpd_open_patch(patch, dir)

    def closePatch(self, dz):
        return pd.libpd_close_patch(dz)

    def play(self):
        self.setDSPState(1)

    def stop(self):
        self.setDSPState(0)

    def isPlaying(self):
        return self.__dspState == 1

    def process(self, inbuf):
        global process_functions
        process_functions[self.__typecode](self.ticksPerBuffer, inbuf, self.__outbuf)
        return self.__outbuf

    def processRaw(self, inbuf):
        pd.libpd_process_raw(inbuf, self.__rawOutbuf)
        return self.__rawOutbuf

    def release(self):
        pd.libpd_release()

