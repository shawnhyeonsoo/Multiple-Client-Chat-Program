import socket
import argparse
import threading
#접속하고 싶은 ip와 port를 입력받는 클라이언트 코드를 작성해보자.
# 접속하고 싶은 포트를 입력한다.
port = 4000

def handle_receive(lient_socket):
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            break
        data = data.decode('utf-8')
        #if not user in data:
        print(data)

def handle_send(client_socket):
    while 1:
        data = input()
        client_socket.send(data.encode('utf-8'))
        if data == "/종료":
            break
    client_socket.close()


if __name__ == '__main__':
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect(("127.0.0.1", 4000))


    #client_socket.send(user.encode('utf-8'))

    receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    receive_thread.join()
