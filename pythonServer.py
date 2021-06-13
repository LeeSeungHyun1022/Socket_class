
from socket import *

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('',port))
sock.listen(1)
print("Wating for clients...")

c_sock, (r_host, r_port) = sock.accept()
print('connected by', r_host, r_port)

while True:
    data = c_sock.recv(BUFSIZE)
    if not data or data.decode() == "a":
        print("연결종료")
        break;

    print("Received message: ", data.decode())

    c_sock.send(data)


c_sock.close()
