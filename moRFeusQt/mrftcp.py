import socket

'''
    http://gqrx.dk/doc/remote-control#more-162
    
     f - Get frequency [Hz]
     F - Set frequency [Hz]
     m - Get demodulator mode
     M - Set demodulator mode (OFF, RAW, AM, FM, WFM, WFM_ST,WFM_ST_OIRT, LSB, USB, CW, CWL, CWU)
     l STRENGTH - Get signal strength [dBFS]
     l SQL - Get squelch threshold [dBFS]
     L SQL <sql> - Set squelch threshold to <sql> [dBFS]
     u RECORD - Get status of audio recorder
     U RECORD <status> - Set status of audio recorder to <status>
     c - Close connection
     AOS - Acquisition of signal (AOS) event, start audio recording
     LOS - Loss of signal (LOS) event, stop audio recording
     \dump_state - Dump state (only usable for compatibility)

'''

class GqRX(object):
    # Constants
    BUFFER_SIZE = 1024
    TCP_PORT = 7356

    def __init__(self, addr):
        self.addr = addr

    def IsConnected(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.addr, self.TCP_PORT))
            return s
        except IOError:
            return False

    def Close(self):
        tcp = self.IsConnected()
        tcp.send(str.encode('c'))

    def GetStrength(self) -> bytes:
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('l STRENGTH'))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data

    def SetFreq(self, msg)-> bool:
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('F ' + msg))
            tcp.close()
            return True
        else:
            return False










