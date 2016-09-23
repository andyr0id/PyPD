import pylibpd as pd

class PDMidiIn(object):
    def __init__(self):
        super(PDMidiIn, self).__init__()

    def noteOn(self, num, vel=127, ch=0):
        return pd.libpd_noteon(ch, num, vel)

    def noteOff(self, num, ch=0):
        return pd.libpd_noteon(ch, num, 0)

    def cc(self, num, val, ch=0):
        return pd.libpd_controlchange(ch, num, val)

    def program(self, val, ch=0):
        return pd.libpd_programchange(ch, val)

    def bend(self, val, ch=0):
        return pd.libpd_pitchbend(ch, val)

    def touch(self, val, ch=0):
        return pd.libpd_aftertouch(ch, val)

    def polytouch(self, num, val, ch=0):
        return pd.libpd_polyaftertouch(ch, num, val)

    def byte(self, port, val):
        return pd.libpd_midibyte(port, val)

    def sysex(self, port, val):
        return pd.libpd_sysex(port, val)

    def sysrt(self, port, val):
        return pd.libpd_sysrealtime(port, val)
        