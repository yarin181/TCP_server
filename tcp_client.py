import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.2.4', 12349))
s.send(b'yarin')
data = s.recv(100)
print("Server sent: ", data.decode())
s.send(b'318229143')
data = s.recv(100)
print("Server sent: ", data.decode())
s.close()