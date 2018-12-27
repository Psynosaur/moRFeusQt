import socket


class GqRX(object):
    # Constants
    BUFFER_SIZE = 1024
    TCP_PORT = 7356

    def __init__(self, addr):
        self.addr = addr

    def IsThere(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.addr, self.TCP_PORT))
            return s
        except OSError or IOError:
            return False

    def SetFreq(self, msg)-> bool:
        tcp = self.IsThere()
        if tcp:
            tcp.send(str.encode('F ' + msg))
            tcp.close()
            return True
        else:
            return False

    def GetStrength(self) -> bytes:
        tcp = self.IsThere()
        if tcp:
            tcp.send(str.encode('l STRENGTH'))
            data = tcp.recv(self.BUFFER_SIZE)
            tcp.close()
            return data








