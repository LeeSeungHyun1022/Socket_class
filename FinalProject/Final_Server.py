import threading, socket

class Room: #룸
    def __init__(self):
        self.clients = []#접속한 클라이언트 관리하는 방 생성
        self.MMclients = [] #moveMode
        self.CMclients = [] #chatMode

    def addClient(self, c): #추가     챗에서만 종료하도록 설정
        self.clients.append(c)
        self.CMclients.append(c)

    def delClent(self, c):  #삭제
        self.clients.remove(c)
        self.CMclients.remove(c)

    def ChangeMoveMode(self, c):    #chat -> move
        self.CMclients.remove(c)
        self.MMclients.append(c)

    def ChangeChatMode(self, c):    #move -> chat
        self.CMclients.append(c)
        self.MMclients.remove(c)

    def sendAllClients(self, msg):  #모든 클라이언트에 메세지 전송
        for c in self.CMclients:
            c.sendMsg(msg)

    def posSendAllClients(self, msg):
        for c in self.MMclients:
            c.sendMsg(msg)

class ChatClient:
    def __init__(self, id, soc, r):
        self.id = id
        self.soc = soc
        self.room = r
        self.moveMode = False
        self.x = 0
        self.y = 0

    def recvMsg(self):
        while True:
            data = self.soc.recv(1024)
            msg = data.decode()

            if not self.moveMode and msg == '/moveMode':
                self.sendMsg(msg)
                print(self.id,'님 무브모드 변경')
                self.room.ChangeMoveMode(self)
                self.moveMode = True
                continue

            if self.moveMode and msg == '/chatMode':
                self.sendMsg(msg)
                print(self.id,'님 채팅모드 변경')
                self.room.ChangeChatMode(self)
                self.moveMode = False
                continue

            if self.moveMode:
                moves = []
                moves = msg
                for move in moves:
                    if move == 'w':
                        self.y = self.y + 1
                    elif move == 'a':
                        self.x = self.x - 1
                    elif move == 's':
                        self.y = self.y - 1
                    elif move == 'd':
                        self.x = self.x + 1
                msg = '{0}님의 좌표 [{1},{2}]'.format(self.id, self.x, self.y)
                self.room.posSendAllClients(msg)
                continue

            if msg == '/exit':
                self.sendMsg(msg)
                print(self.id,'님 퇴장')
                break

            msg = self.id+': ' + msg
            self.room.sendAllClients(msg)
        self.room.sendAllClients(self.id + '님이 퇴장하셨습니다.')
        self.room.delClent(self)



    def sendMsg(self, msg):
        self.soc.sendall(msg.encode(encoding='utf-8'))

    def run(self):
        t = threading.Thread(target=self.recvMsg, args=())
        t.start()

class ServerMain:
    ip = 'localhost'
    port = 8081

    def __init__(self):
        self.room = Room()
        self.server_soc = None

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((ServerMain.ip, ServerMain.port))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('채팅 서버 시작')
        while True:
            c_soc, addr = self.server_soc.accept()
            print(addr)
            while True:
                msg = 'id'
                c_soc.sendall(msg.encode(encoding='utf-8'))
                msg = c_soc.recv(1024)
                id = msg.decode()

                for client in self.room.clients:
                    if client.id == id:
                        msg = '실패'
                        c_soc.sendall(msg.encode(encoding='utf-8'))

                if msg == '실패':
                    continue

                msg = '성공'
                c_soc.sendall(msg.encode(encoding='utf-8'))
                break

            cc = ChatClient(id, c_soc, self.room)
            self.room.addClient(cc)
            cc.run()
            print('클라이언트', id, '채팅 시작')

def main():
    server = ServerMain()
    server.run()

main()
