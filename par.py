import p2p
import threading

class Pair:
    def __init__(self, ports):
        self.ports = ports
        self.nodes = [None, None]
        self.config_nodes()

    def config_nodes(self):
        self.nodes[0] = p2p.P2P(self.ports[0], self.ports[1], "^[a-mA-M]")
        self.nodes[1] = p2p.P2P(self.ports[1], self.ports[0], "^[m-zM-Z]")
        self.nodes[0].server_conf()
        self.nodes[1].server_conf()

    def connect_nodes(self):
        threading.Thread(target=self.nodes[0].espera_como_servidor).start()
        t1 = threading.Thread(target=self.nodes[1].conecta_como_cliente(self.ports[0]))
        t1.start()
        t1.join()
        threading.Thread(target=self.nodes[0].escucha, args=(0,)).start()
        print("Nodo 0 escuchando")

        threading.Thread(target=self.nodes[1].espera_como_servidor).start()
        t2 = threading.Thread(target=self.nodes[0].conecta_como_cliente(self.ports[1]))
        t2.start()
        t2.join()
        threading.Thread(target=self.nodes[1].escucha, args=(0,)).start()
        print("Nodo 1 escuchando")

    def start_nodes(self):
        self.connect_nodes()
        print("Esperando la conexión del servidor...")
        t1 = threading.Thread(target=self.nodes[0].espera_como_servidor)
        t1.start()
        t2 = threading.Thread(target=self.nodes[1].espera_como_servidor)
        t2.start()

        t1.join()
        t2.join()
        print("El nodo principal se ha establecido")

        if len(self.nodes[0].server_conn) > 1:
            threading.Thread(target=self.nodes[0].escucha, args=(1,)).start()
        else:
            threading.Thread(target=self.nodes[1].escucha, args=(1,)).start()

pair = Pair([8000, 8010, 8080])
pair.start_nodes()

