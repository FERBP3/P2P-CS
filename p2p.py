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
                    print("{} : Error, no se recibieron datos -> pos: {}".format(self.addr[1], pos))
                    break
                elif not data.startswith("@"):
                    self.envia("Comando no válido", 1)
                elif data.startswith("@exit"):
                    print("{} : cerrando conexiones".format(self.addr[1]))
                    self.server_conn[0].shutdown(socket.SHUT_RDWR)
                    self.server_conn[0].close()
                    self.server_conn[1].shutdown(socket.SHUT_RDWR)
                    self.server_conn[1].close()
                    self.client_conn[0].shutdown(socket.SHUT_RDWR)
                    self.client_conn[0].close()
                    print("conexiones del nodo principal cerradas")
                    break
                else:
                    self.exec_command(data)
            except Exception as e:
                if e.errno == 57:
                    print("error 57 volviendo al loop")
                    self.socket_servidor.close()
                    continue
                else:
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
            print(res)
            if command[1].startswith("@list"):
                self.envia("@p2pA @list {}".format(res), 0)
            else:
                self.envia("@p2pA {}".format(res), 0)
        elif command.startswith("@p2pA"):
            res = command.split(" ", 1)
            if res[1].startswith("@list"):
                some_words = res[1].split(" ", 1)[1]
                other_words = self.dao.exec_command("@list")
                all_words = "{} {}".format(some_words, other_words)
                self.envia(all_words, 1)
            else:
                self.envia(res[1], 1)
        elif command.startswith("@list"):
            if len(self.server_conn) > 1:
                self.envia("@p2pR {}".format(command), 0)
        else:
            res = self.dao.exec_command(command)
            print(res)
            if res.startswith("RangeError"):
                self.envia("@p2pR {}".format(command), 0)
            else:
                self.envia(res, 1)
