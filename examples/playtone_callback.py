import pyaudio
import sys
from pypd import PD
from pypd.utils import getBuffer

def main():
    # ticksPerBuffer affect the latency and stability
    tpb = 1
    # create a new PD object
    pd = PD(numOutChannels=1, ticksPerBuffer=tpb)
    # create an input buffer
    inbuf = getBuffer(pd)
    # get some info about PD
    outch, inch = pd.getChannels()
    bs = pd.getBlocksize()

    # open a patch and turn on the DSP
    pd.openPatch('sin.pd', '../patches/')
    pd.dspOn()

    # create a threaded audio stream
    def callback(in_data, frame_count, time_info, status):
        outbuf = pd.process(inbuf)
        return (outbuf, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = outch,
                    rate = pd.getSampleRate(),
                    output = True,
                    frames_per_buffer = outch * bs * tpb,
                    stream_callback = callback)

    # process some audio
    while 1:
        try:
            continue
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

