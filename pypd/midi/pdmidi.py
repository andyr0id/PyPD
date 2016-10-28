import pylibpd as pd

class PDMidiIn(object):
    """Send MIDI messages in to libpd
    
    Attributes:
        channel (int): The MIDI channel to send on
    """
    def __init__(self, ch=0):
        self.channel = ch
        super(PDMidiIn, self).__init__()

    def noteOn(self, num, vel=127, ch=None):
        """Sends a MIDI noteOn message
        
        Args:
            num (float): MIDI note number (can be fractional)
            vel (int, optional): MIDI velocity
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_noteon(ch, num, vel)

    def noteOff(self, num, ch=None):
        """Sends a MID noteOff message (a noteOn with velocity 0)
        
        Args:
            num (float): MIDI note number (can be fractional)
            ch (int, optional): Sends on a different channel
        
        Returns:
            TYPE: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_noteon(ch, num, 0)

    def cc(self, num, val, ch=None):
        """Sends a MIDI ControlChange message
        
        Args:
            num (int): MIDI CC number
            val (int): MIDI CC value
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_controlchange(ch, num, val)

    def program(self, val, ch=None):
        """Sends a MIDI Program message
        
        Args:
            val (int): MIDI Program value
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_programchange(ch, val)

    def bend(self, val, ch=None):
        """Sends a MIDI pitch Bend message
        
        Args:
            val (int): MIDI bend value
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_pitchbend(ch, val)

    def touch(self, val, ch=None):
        """Sends a MIDI after touch message
        
        Args:
            val (int): MIDI after touch value
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_aftertouch(ch, val)

    def polytouch(self, num, val, ch=None):
        """Sends a MIDI poly after touch message
        
        Args:
            num (int): MIDI poly after touch number
            val (int): MIDI poly after touch value
            ch (int, optional): Sends on a different channel
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        if ch is None:
            ch = self.channel
        return pd.libpd_polyaftertouch(ch, num, val)

    def byte(self, port, val):
        """Sends a MIDI byte to a specific port
        
        Args:
            port (int): The port to send to
            val (int): The byte to send
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        return pd.libpd_midibyte(port, val)

    def sysex(self, port, val):
        """Sends a System Exclusive message
        
        Args:
            port (int): The port to send to
            val (int): The byte to send
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        return pd.libpd_sysex(port, val)

    def sysrt(self, port, val):
        """Sends a system raltime message.
        
        Args:
            port (int): The port to send to
            val (int): The rt value
        
        Returns:
            int: returns a nonzero error code if a parameter is out of range.
            If all parameters are within range, it will send the event to Pd and return 0
        """
        return pd.libpd_sysrealtime(port, val)

class PDMidiOut(object):
    """Receives messages from PD. Several callbacks can be set for the events.
    
    Attributes:
        channel (int): The MIDI channel to listen to
    """
    def __init__(self, ch=None):
        """Create a new MIDI listener
        
        Args:
            ch (int, optional): The MIDI channel to listen to
        """
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
        pd.libpd_set_programchange_callback(lambda *s: self.__callback2('program', *s))
        pd.libpd_set_pitchbend_callback(lambda *s: self.__callback2('bend', *s))
        pd.libpd_set_aftertouch_callback(lambda *s: self.__callback2('touch', *s))
        pd.libpd_set_polyaftertouch_callback(lambda *s: self.__callback('polytouch', *s))
        pd.libpd_set_midibyte_callback(lambda *s: self.__callback2('byte', *s))
        super(PDMidiOut, self).__init__()

    def __note(self, ch, num, vel):
        if self.channel is None or self.channel == ch:
            if vel > 0:
                for fn in self.__callbacks['noteOn']:
                    fn(num, vel, ch)
            else:
                for fn in self.__callbacks['noteOff']:
                    fn(num, vel, ch)

    def __callback(self, name, ch, num, val):
        if self.channel is None or self.channel == ch:
            for fn in self.__callbacks[name]:
                fn(num, val, ch)

    def __callback2(self, name, ch, val):
        if self.channel is None or self.channel == ch:
            for fn in self.__callbacks[name]:
                fn(val, ch)

    def addCallback(self, name, fn):
        """Add a generic callback for most messages
        
        Args:
            name (str): The callback to listen to (noteOn, noteOff, cc, program, bend, touch, polytouch, or byte)
            fn (function): The callback function
            TYPE: Description
        """
        if name in self.__callbacks:
            self.__callbacks[name].append(fn)

    def noteOn(self, fn):
        """Add a noteOn callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: num, vel, ch
        """
        self.addCallback('noteOn', fn)

    def noteOff(self, fn):
        """Add a noteOff callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: num, vel, ch
        """
        self.addCallback('noteOff', fn)

    def cc(self, fn):
        """Add a CC callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: num, val, ch
        """
        self.addCallback('cc', fn)

    def program(self, fn):
        """Add a Program change callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: val, ch
        """
        self.addCallback('program', fn)

    def bend(self, fn):
        """Add a pitch bend callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: val, ch
        """
        self.addCallback('bend', fn)

    def touch(self, fn):
        """Add an after touch callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: val, ch
        """
        self.addCallback('touch', fn)

    def polytouch(self, fn):
        """Add a poly after touch callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: num, val, ch
        """
        self.addCallback('polytouch', fn)

    def byte(self, fn):
        """Add a MIDI byte callback.
        
        Args:
            fn (function): The callback function. The args for the callback are: byte, port
        """
        self.addCallback('byte', fn)
