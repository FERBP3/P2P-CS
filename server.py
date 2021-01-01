import socket
import sys
import random
import threading

class Server:
    def __init__(self, port):
        self.port = port
        self.client_conn = None

    def conf(self):
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_conn.connect(('localhost', self.port))
        print("Se conectó con un nodo")

    def manda_mensaje(self):
        while True:
            try:
                mensaje = input()
                self.client_conn.sendall(mensaje.encode())
            except Exception as e:
                print(e)
                break

    def escucha(self):
        while True:
            try:
                data = self.client_conn.recv(1024).decode("utf-8")
                if len(data) == 0:
                    break
                print(data)
            except Exception as e:
                print(e)
                break

port = int(sys.argv[random.randint(1, 2)])
my_server = Server(port)
my_server.conf()
threading.Thread(target=my_server.manda_mensaje).start()
threading.Thread(target=my_server.escucha).start()
