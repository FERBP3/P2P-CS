import socket
import sys
import os
import dict_dao

class P2P:

    def __init__(self, server_port, client_port, rango):
        self.socket_servidor = None
        self.addr = ['localhost', server_port]
        self.client_conn = []
        self.server_conn = []
        self.data = None
        self.dao = dict_dao.DICT_DAO(rango)

    def server_conf(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_servidor.bind((self.addr[0], self.addr[1]))
        self.socket_servidor.listen(1)
        print(":: Escuchando en el puerto {}".format(str(self.addr[1])))

    def conecta_como_cliente(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('localhost', port))
            print("Se ha conectado con el cliente: ", port)
            self.client_conn.append(sock)
        except Exception as e:
            print("Error al conectar con el cliente")
            return

    def espera_como_servidor(self):
        try:
            print("{} Esperando nueva conexión".format(self.addr[1]))
            new_client, client_addr = self.socket_servidor.accept()
            if len(self.server_conn) == 1:
                self.envia("@cancel_accept", 0)
            self.server_conn.append(new_client)
            print("{}: Nueva conexión {}".format(self.addr[1], client_addr))
        except:
            sys.exit(0)

    def escucha(self, pos):
        while True:
            try:
                data = self.server_conn[pos].recv(1024).decode("utf-8")
                print("{}: Se recibió de {}: {}".format(self.addr[1], pos, data))

                if data == "@cancel_accept":
                    self.socket_servidor.shutdown(socket.SHUT_RDWR)
                    self.socket_servidor.close()
                elif len(data) == 0:
                    print("Error, no se recibieron datos -> pos: {}".format(pos))
                    break
                else:
                    self.exec_command(data)
            except Exception as e:
                if e.errno == 57:
                    self.socket_servidor.close()
                    continue
                print("{} Error en escucha: {}, pos={}".format(self.addr[1], e, pos))
                break

    # Se le envía la información al cliente o al par
    def envia(self, datos, client):
        try:
            if client:
                print("mandando al servidor mensaje")
                self.server_conn[1].sendall(datos.encode())
            else:
                self.client_conn[0].sendall(datos.encode())
        except Exception as e:
            print("Error en enviar: {} {} {}".format(e, client, datos))

    def exec_command(self, command):
        print("entrando a exec_command")
        if command.startswith("@p2pR"):
            command = command.split(" ", 1)
            res = self.dao.exec_command(command[1])
            self.envia("@p2pA {}".format(res), 0)
        elif command.startswith("@p2pA"):
            res = command.split(" ", 1)
            self.envia(command[1], 1)
        else:
            res = self.dao.exec_command(command)
            if res.startswith("Error"):
                self.envia("@p2pR {}".format(command), 0)
            else:
                self.envia(res, 1)
