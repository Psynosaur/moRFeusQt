import socket

"""
    http://gqrx.dk/doc/remote-control#more-162
    
    These are the commands used in this applications
    
     f - Get frequency [Hz]
     F - Set frequency [Hz]
     m - Get demodulator mode
     M - Set demodulator mode (OFF, RAW, AM, FM, WFM, WFM_ST,WFM_ST_OIRT, LSB, USB, CW, CWL, CWU)
     l STRENGTH - Get signal strength [dBFS]
     l SQL - Get squelch threshold [dBFS]
     L SQL <sql> - Set squelch threshold to <sql> [dBFS]
     q - Close connection ( Documentation says 'c ' this in incorrect )
     
     Responses :
         RPRT 0 - Command successful
         RPRT 1 - Command failed
"""


class GqRX(object):
    # Constants
    BUFFER_SIZE = 1024
    TCP_PORT = 7356

    def __init__(self, a):
        self.__Address = a

    @property
    def Address(self):
        return self.__Address

    @Address.setter
    def Address(self, val):
        pass

    def IsConnected(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(0.25)
            s.connect((self.Address, self.TCP_PORT))
            return s
        except IOError:
            return False

    def Close(self):
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('q '))
            tcp.close()

    def GetStrength(self) -> bytes:
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('l STRENGTH'))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data

    def GetFreq(self):
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('f '))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def GetSQL(self):
        tcp = self.IsConnected()
        if tcp:

            tcp.send(str.encode('l SQL'))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def GetAudioRec(self):
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('u RECORD'))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def GetMod(self):
        tcp = self.IsConnected()
        if tcp:
            tcp.send(str.encode('m '))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def SetFreq(self, msg) -> bool:
        tcp = self.IsConnected()
        message = 'F ' + msg
        if tcp:
            tcp.send(str.encode(message))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def SetSQL(self, msg) -> bool:
        tcp = self.IsConnected()
        message = 'L SQL ' + msg + '\n'
        if tcp:
            tcp.send(str.encode(message))
            print(message)
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False

    def SetMod(self, mod, bw) -> bool:
        tcp = self.IsConnected()
        message = 'M ' + (mod + '\n' + bw + '\n')
        if tcp:
            tcp.send(str.encode(message))
            print(message)
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data
        else:
            return False


