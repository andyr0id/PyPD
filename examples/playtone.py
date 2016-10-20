import pyaudio
import sys
from pypd import PD
from pypd.utils import getBuffer

def main():
    # ticksPerBuffer affect the latency and stability
    tpb = 512
    # create a new PD object
    pd = PD(numOutChannels=1, ticksPerBuffer=tpb)
    # create an input buffer
    inbuf = getBuffer(pd)
    # get some info about PD
    outch, inch = pd.getChannels()
    bs = pd.getBlocksize()

    # create an audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = outch,
                    rate = pd.getSampleRate(),
                    output = True,
                    frames_per_buffer = bs * tpb)

    # open a patch and turn on the DSP
    pd.openPatch('sin.pd', '../patches/')
    pd.dspOn()

    # process some audio
    while 1:
        try:
            outbuf = pd.process(inbuf)
            stream.write(outbuf)
        except KeyboardInterrupt:
            break

    # tidy up the audio stream
    stream.close()
    p.terminate()

    # close PD
    pd.release()
    sys.exit()

if __name__ == '__main__':
    main()

