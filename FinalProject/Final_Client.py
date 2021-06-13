import threading, socket
import keyboard
import time

isConnect = False
moveMode = False

def sendMsg(soc):
    global isConnect
    while True:
        if(not isConnect):  #아이디를 만들어야 다음으로 넘어감
            msg = input()
            soc.sendall(msg.encode(encoding='utf-8'))
            time.sleep(0.5)
            continue

        if(moveMode):       #무브모드로 wasd를 받아 좌표 이동
            if keyboard.is_pressed("q"):
                msg = '/chatMode'
                soc.sendall(msg.encode(encoding='utf-8'))
            msg = ''
            if keyboard.is_pressed("w"):
                msg += 'w'
            if keyboard.is_pressed(
                    "a"):
                msg += 'a'
            if keyboard.is_pressed("s"):
                msg += 's'
            if keyboard.is_pressed("d"):
                msg += 'd'
            soc.sendall(msg.encode(encoding='utf-8'))
            time.sleep(0.3)
            continue
        else:
            msg = input('채팅 내용:')
            soc.sendall(msg.encode(encoding='utf-8'))
            time.sleep(0.5)

        if msg == '/exit':
            break
    print('클라이언트 메시지 입력 쓰레드 종료')

def recvMsg(soc):
    while True:
        data = soc.recv(1024)
        msg = data.decode()

        global moveMode

        if msg == 'id':
            print('사용할 아이디 : ', end='')
            continue
        elif msg == '실패':
            print('중복된 아이디 입니다.')
            continue
        elif msg == '성공':
            global isConnect
            isConnect = True
            print('접속 성공')
            continue
        elif msg == '/moveMode':
            moveMode = True
            print('무브 모드')
            continue
        elif msg == '/chatMode':
            moveMode = False
            print('채팅모드')
            continue
        else:
            print(msg)
            continue

        if msg == '/exit':
            break

    soc.close()
    print('클라이언트 리시브 쓰레드 종료')
    exit()
    quit()

class Client:
    ip = 'localhost'
    port = 8081

    def __init__(self):
        self.client = None

    def conn(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((Client.ip, Client.port))

    def run(self):

        self.conn()
        t1 = threading.Thread(target=recvMsg, args=(self.client,))
        t1.start()
        t2 = threading.Thread(target=sendMsg, args=(self.client,))
        t2.start()

def main():
    c = Client()
    c.run()

main()
