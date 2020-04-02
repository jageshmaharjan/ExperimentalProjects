import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('0.0.0.0', 8081))

sock.send("Twenty two bytes to send")

sock.recv(4096)

sock.close()