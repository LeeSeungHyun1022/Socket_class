import socket

table = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five',\
        '6':'six', '7':'seven', '8':'eight', '9':'nine', '10':'ten'}

s=socket.socket()
address = ("", 2500)
s.bind(address)
s.listen(1)
print('waiting...')
c_socket, c_addr = s.accept()
print("Connection from ", c_addr)

while True:
    data = c_socket.recv(1024).decode()
    
    if data == "q" or data == "Q":
        s.close()
        break;

    try:
        resp = table[data]
    except:
        c_socket.send('Try agin'.encode())
    else:
        c_socket.send(resp.encode())
