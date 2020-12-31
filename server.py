import socket
import sys
import random

port = int(sys.argv[random.randint(1,2)])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))
print("Conectando al puerto {}".format(port))

try:
    mensaje = input()
    sock.sendall(mensaje.encode())
except Exception as e:
    print(e)

try:
    data = sock.recv(1024).decode("utf-8")
    print(data)
except Exception as e:
    print(e)



'''
class Server:
    def __init__(self, port):
        self.port = port
        self.socket_servidor = None
        self.client_conn = None

    def conf(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def escucha(self):
        try:
            self.client_conn, _ = self.socket_servidor.accept()
        except Exception as e:
            print(e)
            return

        while True:
            try:
                data = self.client_conn.recv(1024).decode("utf-8")
                print(data)
            except Exception as e:
                print(e)

    def envia(self):
        try:
            while True:
                mensaje = input()
                self.client_conn.sendall(mensaje.encode())
        except Exception as e:
            print(e)

port = int(sys.argv[random.randint(1, 2)])
server_port = int(sys.argv[3])
my_server = Server(server_port)

'''

