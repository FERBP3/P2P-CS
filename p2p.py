import socket
import sys
import os

class P2P:

    def __init__(self, server_port, client_port):
        self.socket_servidor = None
        self.addr = ['localhost', server_port]
        self.client_conn = []
        self.server_conn = []
        self.data = None
        #self.dao = DICT_DAO()

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
            new_client, _ = self.socket_servidor.accept()
            if len(self.server_conn) == 1:
                self.envia("@cancel_accept", 0)
                print("Enviando cancelación al otro nodo")
                self.socket_servidor.close()
            self.server_conn.append(new_client)
            print("{}: Nueva conexión".format(self.addr[1]))
        except:
            print("cerrando hilo")
            sys.exit(0)

    def escucha(self, pos):
        while True:
            try:
                data = self.server_conn[pos].recv(1024).decode("utf-8")
                print("Se recibió de {}: {}".format(pos, data))

                if data == "@cancel_accept":
                    self.socket_servidor.shutdown(socket.SHUT_WR)
                    self.socket_servidor.close()
                    print("conexión cerrada.")
                if len(data) == 0:
                    print("Error, no se recibieron datos -> pos: {}".format(pos))
                    break
            except Exception as e:
                print("Error en escucha: ",e)
                break

    # Se le envía la información al cliente o al par
    def envia(self, datos, client):
        try:
            if client:
                self.client_conn[1].sendall(datos.encode())
            else:
                self.client_conn[0].sendall(datos.encode())
        except Exception as e:
            print("Error en enviar: ",e)

    def exec_command(command):
        pass
        '''
        res, err = self.dao.exec_command(command)
        if err is not None:
            res, err = self.envia(command, 
        return res, err
        '''
