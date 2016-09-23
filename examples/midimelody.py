from pypd import PD, PDMidiIn
from pypd.utils import getBuffer
import pyaudio
import sys

def main():
    # ticksPerBuffer affect the latency and stability
    tpb = 512
    # create a new PD object
    pd = PD(numOutChannels=1, ticksPerBuffer=tpb)
    # open a patch
    dz = pd.openPatch('midisynth.pd', '../patches')
    # turn on the DSP
    pd.play()

    # create a MIDI channel to PD
    midi = PDMidiIn()
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
                    frames_per_buffer = outch * bs * tpb)

    # duration
    dur = 20
    # make a melody
    melody = [60, 62, 64, 65, 67, 65, 64, 62, 60]
    # play it!
    j = 0
    spt = pd.getSampleRate() / bs / tpb
    for i in xrange(int(dur * spt)):
        if i % spt == 0:
            # release last note
            if j > 0:
                midi.noteOff(melody[j-1])
            # trigger next note
            if j < len(melody):
                note = melody[j]
                midi.noteOn(note)
                j += 1
        outbuf = pd.process(inbuf)
        stream.write(outbuf)

    # tidy up the audio stream
    stream.close()
    p.terminate()

    # close PD
    pd.release()
    sys.exit()

if __name__ == '__main__':
    main()