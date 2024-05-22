import socket
from datetime import datetime

# Socket custom class

MSGLEN = 255

class Socket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try: 
            self.sock.connect((host, port))
            print("[{}] New connection to {}:{}".format(datetime.now(), host, port))
            return True
        except:
            print("ERROR: Unable to etablish connection to {}:{}".format(host, port))
            return False

    def accept(self):
        try: 
            connection, address = self.sock.accept()
            return (Socket(connection), address)
        except Exception as exception:
            print(exception)
            return False

    def send(self, msg):
        self.sock.sendall(msg)
        # totalsent = 0
        # while totalsent < MSGLEN:
        #     sent = self.sock.send(msg[totalsent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     totalsent = totalsent + sent

    def handle(self, callback):
        socketAddr, socketPort = self.sock.getpeername()
        print("[{}] New connection etablished with client {}:{}".format(datetime.now(), socketAddr, socketPort))

        try:
            data = self.sock.recv(1024) # message length is limited to 1024 bytes
            return callback(data.decode('utf8'))
        except Exception as exception:
            print(exception)
            return False

        # chunks = []
        # bytes_recd = 0
        # while bytes_recd < MSGLEN:
        #     chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
        #     if chunk == b'':
        #         raise RuntimeError("socket connection broken")
        #     chunks.append(chunk)
        #     bytes_recd = bytes_recd + len(chunk)
        # return b''.join(chunks)

    def close(self):
        remoteAddr, remotePort = self.sock.getpeername()
        print("[{}] Etablished connection closed with server {}:{}".format(datetime.now(), remoteAddr, remotePort))
        self.sock.close()