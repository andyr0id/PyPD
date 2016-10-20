from pypd import PD, PDMidiIn
from pypd.utils import getBuffer
import pyaudio
import sys
import time

def main():
    # ticksPerBuffer affect the latency and stability
    tpb = 1
    # create a new PD object
    pd = PD(numOutChannels=1, ticksPerBuffer=tpb)
    # open a patch
    dz = pd.openPatch('midisynth.pd', '../patches')
    # turn on the DSP
    pd.dspOn()

    # create a MIDI channel to PD
    midi = PDMidiIn()
    # create an input buffer
    inbuf = getBuffer(pd)

    # get some info about PD
    outch, inch = pd.getChannels()
    bs = pd.getBlocksize()

    # create a threaded audio stream
    def callback(in_data, frame_count, time_info, status):
        outbuf = pd.process(inbuf)
        return (outbuf, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = outch,
                    rate = pd.getSampleRate(),
                    output = True,
                    frames_per_buffer = bs * tpb,
                    stream_callback = callback)

    # note duration
    dur = 0.5
    # make a melody
    melody = [60, 62, 64, 65, 67, 65, 64, 62, 60]
    totalDur = dur * len(melody) + 1
    # play it!
    i = 0
    t = 0
    while t < totalDur:
        # release last note
        if i > 0:
            midi.noteOff(melody[i-1])
        # trigger next note
        if i < len(melody):
            note = melody[i]
            midi.noteOn(note)
            i += 1
        t += dur
        time.sleep(dur)

    # tidy up the audio stream
    stream.close()
    p.terminate()

    # close PD
    pd.release()
    sys.exit()

if __name__ == '__main__':
    main()