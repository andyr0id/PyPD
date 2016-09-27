import pylibpd as pd

class PDIn(object):
    def __init__(self):
        super(PDIn, self).__init__()

    def bang(self, dest):
        return pd.libpd_bang(dest)

    def float(self, dest, val):
        return pd.libpd_float(dest, val)

    def symbol(self, dest, val):
        return pd.libpd_symbol(dest, val)

    def list(self, dest, val):
        return pd.libpd_list(dest, *val)

    def message(self, dest, sym, *args):
        return pd.libpd_message(dest, sym, *args)

class PDOut(object):
    def __init__(self):
        self.__callbacks = {
            'print': [],
            'bang': [],
            'float': [],
            'symbol': [],
            'list': [],
            'message': [],
        }
        pd.libpd_set_print_callback(lambda *s: self.__callback('print', *s))
        pd.libpd_set_bang_callback(lambda *s: self.__callback('bang', *s))
        pd.libpd_set_float_callback(lambda *s: self.__callback('float', *s))
        pd.libpd_set_symbol_callback(lambda *s: self.__callback('symbol', *s))
        pd.libpd_set_list_callback(lambda *s: self.__callback('list', *s))
        pd.libpd_set_message_callback(lambda *s: self.__callback('message', *s))
        super(PDOut, self).__init__()

    def __callback(self, name, *args):
        for fn in self.__callbacks[name]:
            fn(*args)

    def addCallback(self, name, fn):
        if name in self.__callbacks:
            self.__callbacks[name].append(fn)

    def subscribe(self, sym):
        pd.libpd_subscribe(sym)

    def unsubscribe(self, sym):
        pd.libpd_unsubscribe(sym)

    def prnt(self, fn):
        self.addCallback('print', fn)

    def bang(self, fn):
        self.addCallback('bang', fn)

    def float(self, fn):
        self.addCallback('float', fn)

    def symbol(self, fn):
        self.addCallback('symbol', fn)

    def list(self, fn):
        self.addCallback('list', fn)

    def message(self, fn):
        self.addCallback('message', fn)
        