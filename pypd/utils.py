import array

def getBuffer(pd, buftype='input'):
    """Creates an array suitable for libpd IO
    
    Args:
        pd (PD): The PD object
        buftype (str, optional): input or output
    
    Returns:
        array: The created buffer
    """
    outch, inch = pd.getChannels()
    if buftype == 'input':
        ch = inch
    else:
        ch = outch
    return array.array(pd.getTypecode(),
        '\x00\x00' * ch * pd.getBlocksize() * pd.ticksPerBuffer)

def getRawBuffer(pd, buftype='input'):
    """Creates a raw array suitable to libpd IO
    
    Args:
        pd (PD): The PD object
        buftype (str, optional): input or output
    
    Returns:
        array: The created buffer
    """
    outch, inch = pd.getChannels()
    if buftype == 'input':
        ch = inch
    else:
        ch = outch
    return array.array('f',
        '\x00\x00' * ch * pd.getBlocksize())