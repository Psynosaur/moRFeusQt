import socket


class GqRX(object):
    # Constants
    BUFFER_SIZE = 1024
    TCP_PORT = 7356

    def __init__(self, addr):
        self.addr = addr

    def send(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.addr, self.TCP_PORT))
            s.send(str.encode(msg))
            data = s.recv(self.BUFFER_SIZE)
            return data
        except Exception as e:
            print("GQRX at %s:%d. says %s" % (self.addr, self.TCP_PORT, e))
        finally:
            s.close()






