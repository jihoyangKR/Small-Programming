## 서버 소켓 세팅

```python
from socket import *

serverSock = socket(AF_INET, SOCK_STREAM) # socket 객체 생성
serverSock.bind(('', 8080)) # 생성한 소켓 bind
serverSock.listen(1) # listen

connectionSock, addr = serverSock.accept() #accept
```

- socket 객체 생성 : 두 가지 인자를 입력한다. 첫번째는 어드레스 패밀리(AF: Address Family), 두 번째는 소켓 타입
  - 어드레스 패밀리는 주소 체계에 해단한다. AF_INET은 IPv4, AF_INET6는 IPv6를 의미한다.
- 소켓 bind : 클라이언트를 만들 때는 불필요하나 서버를 운용할 때는 반드시 필요하다. 생성된 소켓의 번호와 실제 어드레스 패밀리를 연결해주는 역할
  - 함수 내에서 **튜플**을 입력. 입력된 인자는 어드레스 패밀리가 된다. 앞부분은 ip, 뒷부분은 포트로 (ip, port)형식으로 구성된 한 쌍의 튜플이 어드레스 패밀리가 되는 셈이다.
  - 주소가 빈 문자열인 이유는 AF_INET에서 `''`는 **INADDR_ANY**를 의미한다. 즉, 모든 인터페이스와 연결하고 싶다면 빈 문자열을 넣으면 된다.
  - 즉 위의 bind는 8080번 포트에서 모든 인터페이스에게 연결하도록 한다. 라는 의미이다.
- listen
  - 상대방의 접속을 기다리는 단계
  - listen 역시 서버소켓애서만 쓸 일이 없다. listen()안의 인자는 해당 소켓이 총 몇개의 동시 접속을 허용할 것이냐를 의미한다. 인자를 입력하지 않으면 파이썬이 자의적으로 판단해서 임의의 숫자로 listen한다.
- accept
  - 소켓에 누군가가 접속하여 연결되었을 때에 비로소 결과값이 return 되는 함수이다. 즉 코드 내에 accept()가 있더라도, 누군가가 접속할 때 까지 프로그램이 여기에서 멈춰 있게 되는 것이다.
  - 상대방이 접속함으로써 accept()가 실행되면 return 값으로 새로운 소켓과 상대방의 AF를 전달해주게 된다.
  - 서버에 접속한 상대방과 데이터를 주고받기 위해서는 accept()를 통해 생성된 connectionSock이라는 소켓을 이용한다. 

## 클라이언트 소켓 세팅

```python
from socket import *
clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))
```

bind와 listen, accept과정 대신 connect가 추가된다. 클라이언트에서 서버에 접속하기 위해서는 connet()만 실행해 주면 된다. AF가 인자로 들어가고, 호스트 주소와 포트 번호로 구성된 튜플이 요구된다. 127.0.0.1은 자기 자신을 의미하므로 위으 AF는 자기 자신에게 8080 포트로 연결하라는 의미이다.

## 소켓 송수신

서버 소켓에서는 connectionsSock을 이용해서 데이터를 주고받고 클라이언트는 clientSock을 이용한다.

bind()로 서버를 구성한 소켓으로는 데이터를 주고 받지 않는다.

### 소켓으로 데이터를 주고 받는 방법

send()와 recv()를 이용한다. 함수명으로 알 수 있듯 send()는 보내고 recv()는 받는 메소드이다.

소켓을 통해 "안녕"을 보내고 싶다면

```python
msg = '안녕'
connectionSock.sed(msg.encode('utf-8'))
```

문자열을 전송할 때 encode()가 들어간다. 파이썬 문자열의 encode()메소드는 문자열을 byte로 변환해 주는 메소드이다. 파이썬 내부에서 다뤄지는 문자열은 파이썬에서 생성된 객체이고, 이를 바로 트랜스포트에 그대로 싣는 것은 불가능하다. 그러므로 적절한 인코딩을 해서 보내야만 한다. 인코딩을 하지 않고 보내면 에러가 발생한다.

---

상대방에게서 온 메시지를 확인하려면

```python
msg = connectionSock.recv(1024)
print(msg.decode('utf-8'))
```

recv()를 실행하면 소켓에 메시지가 실제로 수신될 때 까지 파이썬 코드는 대기하게 된다. 인자로는 수신할 바이트의 크기를 지정할 수 있다. 위의 코드는 소켓에서 1024바이트 만큼을 가져오겠다는 의미이다. 만일 소켓에 도착한 데이터가 1024바이트보다 많다면, 다시 recv(1024)를 실행할 때 전에 미쳐 가져오지 못했던 것들을 마저 가져온다.

send()에서 문자열을 인코딩해서 보냈기 때문에 recv()를 할 때는 데이터를 바이트로 수신하기 때문에 문자열로 활용하기 위해 decode()를 사용해 디코딩을 한다.

소켓에서 주고받는 데이터는 바이트이므로, 문자열이 아닌 이미지 파일이나 동영상 파일을 읽어 1024바이트 단위로 전송을 해도 실제 상대방 컴퓨터에 파일을 전송할 수 있다.



## 예시 코드

### server

```python
from socket import *

serverSock = socket(AF_INET, SOCK_STREAM) 
serverSock.bind(('', 8080))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()


print(str(addr),'에서 접속이 확인되었습니다.')

data = connectionSock.recv(1024)
print('받은 데이터: ', data.decode('utf-8'))

connectionSock.send('I am server.'.encode('utf-8'))
print('메시지를 보냈습니다.')
```

### client

```python
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))

print('연결 되었습니다.')
clientSock.send('I am a client'.encode('utf-8'))

print('메시지를 전송했습니다.')

data = clientSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))
```



## 실제 채팅 구현하기

- 메시지를 한 번만 주고 받는게 아니라, 계속해서 주고 받게 하고
- 보내는 메시지도 사용자가 직접 입력

server

```python
from socket import *

port = 8080

severSock = socket(AF_INET, SOCK_STREAM)
severSock.bind(('', port))
severSock.listen(1)

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = severSock.accept()

print(str(addr), '에서 접속되었습니다.')

while True:
    sendData = input('>>>')
    connectionSock.send(sendData.encode('utf-8'))

    recvData = connectionSock.recv(1024)
    print('상대방 : ', recvData.decode('utf-8'))
```

client

```python
from socket import *

port = 8080

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

print('접속 완료')

while True:
    recvData = clientSock.recv(1024)
    print('상대방: ', recvData.decode('utf-8'))

    sendData = input('>>>')
    clientSock.send(sendData.encode('utf-8'))
```



이 코드들의 문제점

- 전체 코드에서 while문 안에서 보내고 받는것을 한번에 써두니 보기 불편하다. 이를 해결하기 위해 보내기 기능과 받기 기능을 함수로 따로 분리시키자.

  ```python
  #Server
  from socket import *
  
  def send(sock):
      sendData = input('>>>')
      sock.send(sendData.encode('utf-8'))
  
  def receive(sock):
      recvData = sock.recv(1024)
      print('상대방 : ', recvData.decode('utf-8'))
  
  port = 8080
  
  severSock = socket(AF_INET, SOCK_STREAM)
  severSock.bind(('', port))
  severSock.listen(1)
  
  print('%d번 포트로 접속 대기중...'%port)
  
  connectionSock, addr = severSock.accept()
  
  print(str(addr), '에서 접속되었습니다.')
  
  while True:
      send(connectionSock)
  
      receive(connectionSock)
  
  # Client
  from socket import *
  
  def send(sock):
      sendData = input('>>>')
      sock.send(sendData.encode('utf-8'))
  
  def receive(sock):
      recvData = sock.recv(1024)
      print('상대방 : ', recvData.decode('utf-8'))
  
  port = 8080
  
  clientSock = socket(AF_INET, SOCK_STREAM)
  clientSock.connect(('127.0.0.1', port))
  
  print('접속 완료')
  
  while True:
      recvData = clientSock.recv(1024)
      print('상대방: ', recvData.decode('utf-8'))
  
      sendData = input('>>>')
      clientSock.send(sendData.encode('utf-8'))
  ```

- 송수신을 순서 상관없이 동시에 할 수 있도록 하기

  - 스레드(Thread)를 활용해야 한다.

    - 프로세스 내부에서 병렬 처리를 하기 위해, 프로세스의 소스코드 내부에서 특정 함수만 따로 뽑아내어 분신을 생선하는 것이다.
    - 즉, 원래라면 하나의 절차를 따르며 해야하는 일들도, 스레드를 생성해서 돌릴 경우에는 동시 다발적으로 일을 할 수 있다.
    - 파이썬에서 스레드를 생성하기 위해서는 theading을 불러와야 한다.

    ```python
    import threading
    
    def send(sock):
        while True:
            sendData = input('>>>')
            sock.send(sendData.encode('utf-8'))
    
    def receive(sock):
        while True:
            recvData = sock.recv(1024)
            print('상대방 :', recvData.decode('utf-8'))
    
    sender = threading.Thread(target=send, args=(connectionSock,))
    receiver = threading.Thread(target=receive, args=(connectionSock,))
    
    sender.start()
    receiver.start()
    ```

    send()와 recieve()를 while True로 감싼다.

    스레드를` threading.Thread()`로 생성할 수 있다. `import threading`이 아닌 `from threading import *`를 썼다면 그냥 `Thread()`만 적으면 된다.

    Thread() 생성자는 여러 인자를 받지만 여기에선 target과 args만 보면 된다. target은 실제로 스레드가 실행할 함수를 입력하고, 그 함수에 입력할 인자를 args에 입력하면 된다.

    주의해야 할 점은, args는 튜플과 같이 interable한 변수만 입력될 수 있다. 문제는 인자가 하나일 경우, (var)처럼 괄호로 감싸기만 하면 파이썬 인터프리터는 이를 튜플이 아닌 그냥 var로 인식하므로 (var, )과 같이 콤마를 사용해야 튜플로 인식한다.

    생성된 스레드는 start()를 실행했을 때 일을 시작한다. 생성된 스레드는 본인의 일을 전부 끝내면 알아서 사라진다. 하지만 지속적인 채팅을 하게 만들어야 하므로 while True가 들어간 것이다. 이로서 sender와 receiver는 프로세스가 종료되지 않는 한은 계속 실행될 것이다.

    프로세스 역시 계속해서 돌아가야 하므로

    ```python
    while True:
        pass
    ```

    를 걸어주면 프로그램을 강제종료를 하지 않는 이상 꺼지지 않는다. 하지만 이럴 경우 파이썬은 이 코드를 1초에 어마어마한 연산을 반복하기 때문에 각 while문 마다 쉬는 시간을 주면 된다. 

    ```python
    import time
    while True:
        time.sleep(1)
        pass
    ```

    time의 sleep()함수는 입력된 인자만큼 대기하는 함수이다. 단위는 초이므로 위의 코드는 1초씩 쉬고 다음 while문을 호출하는 것을 반복한다.



최종 코드

server

```python
from socket import *
import threading
import time


def send(sock):
    while True:
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('상대방 :', recvData.decode('utf-8'))


port = 8081

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속되었습니다.')

sender = threading.Thread(target=send, args=(connectionSock,))
receiver = threading.Thread(target=receive, args=(connectionSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
```

client

```python
from socket import *
import threading
import time


def send(sock):
    while True:
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('상대방 :', recvData.decode('utf-8'))


port = 8081

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', port))

print('접속 완료')

sender = threading.Thread(target=send, args=(clientSock,))
receiver = threading.Thread(target=receive, args=(clientSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
```



이제 마지막 문제는 자기가 입력하는 도중 상대방이 전송하면 자신의 말이 끊긴다는 문제가 있다.

허나 이는 콘솔에서 실행하는 특성상 어쩔 수 없는듯 하다.