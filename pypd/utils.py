import array

def getBuffer(pd, buftype='input'):
    outch, inch = pd.getChannels()
    if buftype == 'input':
        ch = inch
    else:
        ch = outch
    return array.array(pd.getTypecode(),
        '\x00\x00' * ch * pd.getBlocksize() * pd.ticksPerBuffer)

def getRawBuffer(pd, buftype='input'):
    outch, inch = pd.getChannels()
    if buftype == 'input':
        ch = inch
    else:
        ch = outch
    return array.array('f',
        '\x00\x00' * ch * pd.getBlocksize())