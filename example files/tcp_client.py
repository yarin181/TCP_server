import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('0.0.0.0', 12349))
s.send(b'yarin')
data = s.recv(100)
print("Server sent: ", data.decode())
s.send(b'999999999')
data = s.recv(100)
print("Server sent: ", data.decode())
s.close()