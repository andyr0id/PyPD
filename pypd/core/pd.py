import array
import pylibpd as pd
from pypd.utils import getBuffer, getRawBuffer

process_functions = {
    'h': pd.libpd_process_short,
    'f': pd.libpd_process_float,
    'd': pd.libpd_process_double,
}

class PD(object):
    """The PD object is an Object-oriented wrapper around many common libpd functions.
    
    Attributes:
        ticksPerBuffer (int): how many blocks to process per call to the process() method
    """
    def __init__(self,
            numOutChannels=2, numInChannels=0,
            sampleRate=44100, ticksPerBuffer=1,
            typecode='h'):
        """Creates a new PD object. There is really only the need to do this once
        as you can't have multiple libpds running at once.
        
        Args:
            numOutChannels (int, optional): Number of output channels (defaults: 2)
            numInChannels (int, optional): Number of input channels (default: 1)
            sampleRate (int, optional): PD sample rate in Hz (default: 44100)
            ticksPerBuffer (int, optional): how many blocks to process per call to the process() method
            typecode (str, optional): h, f, or d. See array.array for what these mean.
        """
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
        """Set the input and output channels
        
        Args:
            numOutChannels (int): Number of output channels
            numInChannels (int): Number of input channel
            reinit (bool, optional): If True (the default), reinitialises libpd
        
        Returns:
            TYPE: Description
        """
        self.__outChannels = numOutChannels
        self.__inChannels = numInChannels
        if reinit:
            self.init()

    def getChannels(self):
        """Returns the number of inputs, outputs
        
        Returns:
            tuple: (out, in)
        """
        return (self.__outChannels, self.__inChannels)

    def setSampleRate(self, sampleRate, reinit=True):
        """Set the libpd sample rate
        
        Args:
            sampleRate (int): PD sample rate in Hz
            reinit (bool, optional): If True (the default), reinitialises libpd
        """
        self.__sampleRate = sampleRate
        if reinit:
            self.init()

    def getSampleRate(self):
        """Get the current sample rate
        
        Returns:
            int: PD sample rate in Hz
        """
        return self.__sampleRate

    def setTypecode(self, typecode, reinit=True):
        """Sets the type of data used by the libpd process.
        See array.array for what the typecodes mean.
        
        Args:
            typecode (str): h, f, or d
            reinit (bool, optional): If True (the default), reinitialises libpd
        
        Raises:
            ValueError: only certain formats are supported
        """
        global process_functions
        if typecode not in process_functions:
            raise ValueError('%s not a valid format' % typecode)
        self.__typecode = typecode
        if reinit:
            self.init()

    def getTypecode(self):
        """Get the current data format used by PD
        
        Returns:
            str
        """
        return self.__typecode

    def setDSPState(self, state=1):
        """Sets the current libpd DSP state
        
        Args:
            state (int, optional): 1 = on, 0 = off
        """
        self.__dspState = state
        pd.libpd_compute_audio(state)

    def getDSPState(self):
        """Returns the current DSP state
        
        Returns:
            int: 1 = on, 0 = off
        """
        return self.__dspState

    def getBlocksize(self):
        """Returns the current blocksize used by libpd
        
        Returns:
            int: Default blocksize is 64
        """
        return self.__blocksize

    def init(self):
        """Initialises libpd
        """
        self.initBuffers()
        self.initAudio()

    def initBuffers(self):
        """Initilises input/output buffers
        """
        self.__outbuf = getBuffer(self, 'output')
        self.__rawOutbuf = getRawBuffer(self, 'output')

    def initAudio(self):
        """Initialises the libpd audio params
        """
        return pd.libpd_init_audio(self.__inChannels, self.__outChannels, self.__sampleRate)

    def openPatch(self, patch, dir = '.'):
        """Open a PD patch and return $0
        
        Args:
            patch (str): The file path to the patch
            dir (str, optional): The directory the patch is in
        
        Returns:
            int: $0 value for this patch
        """
        return pd.libpd_open_patch(patch, dir)

    def closePatch(self, dz):
        """Close the specified PD patch
        
        Args:
            dz (int): The ID of the patch to close
        
        Returns:
            int: status message
        """
        return pd.libpd_close_patch(dz)

    def dspOn(self):
        """Turn the DSP on
        """
        self.setDSPState(1)

    def dspOff(self):
        """Turn the DSP off
        """
        self.setDSPState(0)

    def isDSPOn(self):
        """
        
        Returns:
            boolean: True is the DSP is on
        """
        return self.__dspState == 1

    def process(self, inbuf):
        """Process ticksPerBuffer worth of data
        
        Args:
            inbuf (array): The input array buffer
        
        Returns:
            array: The output buffer
        """
        global process_functions
        process_functions[self.__typecode](self.ticksPerBuffer, inbuf, self.__outbuf)
        return self.__outbuf

    def processRaw(self, inbuf):
        """Process and return a raw output. Faster than process(), 
        but the output is slightly more difficult to work with
        
        Args:
            inbuf (array): The input buffer to process
        
        Returns:
            array: The raw output buffer
        """
        pd.libpd_process_raw(inbuf, self.__rawOutbuf)
        return self.__rawOutbuf

    def release(self):
        """Cleanup libpd
        """
        pd.libpd_release()
