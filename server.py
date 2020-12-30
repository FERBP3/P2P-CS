import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8010))
print("Conectado. Mandando mensaje...")

try:
    while True:
        mensaje = input()
        sock.sendall(mensaje.encode())
except Exception as e:
    print(e)

