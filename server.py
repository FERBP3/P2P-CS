import socket
import sys
import random

port = int(sys.argv[random.randint(1, 2)])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))
print("Conectado al puerto {}. Mandando mensaje...".format(port))

try:
    while True:
        mensaje = input()
        sock.sendall(mensaje.encode())
except Exception as e:
    print(e)
