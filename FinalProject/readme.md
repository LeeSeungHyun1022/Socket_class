#201744090 이승현 TCPIP
>개요
>>TCPIP 기말 프로젝트로 채팅프로그램 구현

>목적
>>ip와 port만 알고 있다면 연결 후 채팅이 되도록 구현

>설계 및 기능
>>1.클라이언트가 서버에 연결 되어야한다
>>
   ![1](https://user-images.githubusercontent.com/70618998/121803536-1ded4780-cc7d-11eb-9792-21f309ab4a83.png)
>>
>>2.서버에 접속된 클라이언트들끼리 메시지를 주고받을 수 있어야한다
>>
   ![2](https://user-images.githubusercontent.com/70618998/121803603-6c024b00-cc7d-11eb-832a-c4f183690e7c.png)
>>

>기능 및 차이점
>>3.move모드와 chat모드를 따로 나눠 설계한다
>>>move모드 : wasd를 눌렀을때 좌표를 이동시키고 이동시킨 좌표를 move모드에 있는 클라이언트들에게 전송
>>>
>>>chat모드 : text를 전송했을때 chat모드에 있는 클라이언트들에게 전송
>>>>chat->move 채팅창에 /moveMode입력
>>>>
>>>>move->chat q pressed

![3](https://user-images.githubusercontent.com/70618998/121803823-40cc2b80-cc7e-11eb-804e-aadc0ebdb5ce.png)

>>4.위 move모드와 chat모드를 따로 나누어 
