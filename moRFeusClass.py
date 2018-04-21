# I have not bothered to implement the get Functions from the moRFeus tool, since it doesn't really serve a purpose
# since there seems to be a LED screen, ya know. . .

class moRFeus(object):
    # Constants
    LOmax        = 5400000000                                                       # Local Oscillator max (5400MHz)
    LOmin        = 85000000                                                         # Local Oscillator min (85Mhz)
    mil          = 1000000                                                          # Saves some zero's here and there
    # Byte Arrays known to the moRFeus device
    # readReg      = [0, 114, 0, 0, 0, 0, 0, 0, 0, 190, 250, 0, 0, 96, 0, 0, 0]       # heh?
    setGen       = [0, 119, 130, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # Generator mode
    setMix       = [0, 119, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # Mixer mode
    biasOn       = [0, 119, 132, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # BiasTee on
    biasOff      = [0, 119, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # BiasTee off
    whiteNoise   = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]   # setFrequency to 5400 000 000 Hz
    setCurrent   = [0, 119, 131, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]          # setCurrent bytearray template

    setCur       = bytearray(setCurrent)                                            # we declare it a bytearray for manipulation of setCur[x]
                                                                                    # with our custom 8byte current array
    setFrequency = [0, 119, 129, 0, 0, 0, 1, 65, 221, 118, 0, 96, 0, 0, 2, 31, 0]   # setFrequency bytearray template
    setFreq      = bytearray(setFrequency)                                          # we declare it a bytearray for manipulation of setFreq[x]
