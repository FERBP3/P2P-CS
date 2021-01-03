import socket
import sys
import random
import threading

class Server:
    def __init__(self, server_port, p2p_port):
        self.server_port = server_port
        self.p2p_port = p2p_port
        self.p2p_conn = None
        self.client_conn = None

    def conf(self):
        self.p2p_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p2p_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.p2p_conn.connect(('localhost', self.p2p_port))
        print("Se conectó con un nodo")

    def espera_como_servidor(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', self.server_port))
        sock.listen(1)
        print("Esperando al cliente en ", self.server_port)
        self.client_conn, addr = sock.accept()
        print("Conectado al cliente")
        while True:
            try:
                data = self.client_conn.recv(1024).decode("utf-8")
                if not data:
                    break
                if data.startswith("@exit"):
                    self.client_conn.sendall("@exit".encode())
                    self.client_conn.close()
                    self.p2p_conn.sendall(data.encode())
                    break
                print(data)
                self.p2p_conn.sendall(data.encode())
            except Exception as e:
                pass
                #print(e)

    def escucha_p2p(self):
        while True:
            try:
                data = self.p2p_conn.recv(1024).decode("utf-8")
                if self.client_conn is not None:
                    self.client_conn.sendall(data.encode())
                if len(data) == 0:
                    print("conexion terminada")
                    break
                #print(data)
            except Exception as e:
                #print(e)
                break

server_port = int(sys.argv[1])
p2p_port = int(sys.argv[random.randint(2, 3)])
my_server = Server(server_port, p2p_port)
my_server.conf()
threading.Thread(target=my_server.espera_como_servidor).start()
threading.Thread(target=my_server.escucha_p2p).start()
