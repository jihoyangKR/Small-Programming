from socket import *

serverSock = socket(AF_INET, SOCK_STREAM) # socket 객체 생성, 두가지 인자 입력(어드레스 패밀리(AF), 소켓 타입
serverSock.bind(('', 8080))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()


print(str(addr),'에서 접속이 확인되었습니다.')

data = connectionSock.recv(1024)
print('받은 데이터: ', data.decode('utf-8'))

connectionSock.send('I am server.'.encode('utf-8'))
print('메시지를 보냈습니다.')