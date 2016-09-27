import pylibpd as pd

class PDMidiIn(object):
    def __init__(self, ch=0):
        self.channel = ch
        super(PDMidiIn, self).__init__()

    def noteOn(self, num, vel=127, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_noteon(ch, num, vel)

    def noteOff(self, num, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_noteon(ch, num, 0)

    def cc(self, num, val, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_controlchange(ch, num, val)

    def program(self, val, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_programchange(ch, val)

    def bend(self, val, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_pitchbend(ch, val)

    def touch(self, val, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_aftertouch(ch, val)

    def polytouch(self, num, val, ch=None):
        if ch is None:
            ch = self.channel
        return pd.libpd_polyaftertouch(ch, num, val)

    def byte(self, port, val):
        return pd.libpd_midibyte(port, val)

    def sysex(self, port, val):
        return pd.libpd_sysex(port, val)

    def sysrt(self, port, val):
        return pd.libpd_sysrealtime(port, val)

class PDMidiOut(object):
    def __init__(self, ch=None):
        self.channel = ch
        self.__callbacks = {
            'noteOn': [],
            'noteOff': [],
            'cc': [],
            'program': [],
            'bend': [],
            'touch': [],
            'polytouch': [],
            'byte': [],
        }
        pd.libpd_set_noteon_callback(lambda *s: self.__note(*s))
        pd.libpd_set_controlchange_callback(lambda *s: self.__callback('cc', *s))
        pd.libpd_set_programchange_callback(lambda *s: self.__callback('program', *s))
        pd.libpd_set_pitchbend_callback(lambda *s: self.__callback('bend', *s))
        pd.libpd_set_aftertouch_callback(lambda *s: self.__callback('touch', *s))
        pd.libpd_set_polyaftertouch_callback(lambda *s: self.__callback('polytouch', *s))
        pd.libpd_set_midibyte_callback(lambda *s: self.__byte(*s))
        super(PDMidiOut, self).__init__()

    def __note(self, ch, num, vel):
        if self.channel is None or self.channel == ch:
            if vel > 0:
                for fn in self.__callbacks['noteOn']:
                    fn(num, vel, ch)
            else:
                for fn in self.__callbacks['noteOff']:
                    fn(num, vel, ch)

    def __callback(self, name, ch, num, vel):
        if self.channel is None or self.channel == ch:
            for fn in self.__callbacks[name]:
                fn(num, vel, ch)

    def __byte(self, port, val):
        for fn in self.__callbacks['byte']:
            fn(num, vel, ch)

    def addCallback(self, name, fn):
        if name in self.__callbacks:
            self.__callbacks[name].append(fn)

    def noteOn(self, fn):
        self.addCallback('noteOn', fn)

    def noteOff(self, fn):
        self.addCallback('noteOff', fn)

    def cc(self, fn):
        self.addCallback('cc', fn)

    def program(self, fn):
        self.addCallback('program', fn)

    def bend(self, fn):
        self.addCallback('bend', fn)

    def touch(self, fn):
        self.addCallback('touch', fn)

    def polytouch(self, fn):
        self.addCallback('polytouch', fn)

    def byte(self, fn):
        self.addCallback('byte', fn)






        