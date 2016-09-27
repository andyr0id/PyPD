import os

def getPatchesDir():
    d = os.path.dirname(os.path.realpath(__file__))
    return d[:d.index('pypd/pypd/')] + 'pypd/patches/'