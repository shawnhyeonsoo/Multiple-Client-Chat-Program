import socket
import argparse
import threading
import time

host = "127.0.0.1"
port = 4000
user_list = {}
notice_flag = 0
room_list = []
room_user = {}
user_room = {}

def msg_func(msg):
    print(msg)
    for con in user_list.values():
        try:
            con.send(msg.encode('utf-8'))
        except:
            print("연결이 비 정상적으로 종료된 소켓 발견")


def handle_receive(client_socket, addr, user):
    msg = "---- %s has entered. ----"%user
    msg_func(msg)
    while 1:
        data = client_socket.recv(1024)
        string = data.decode('utf-8')

        if "/exit" in string:
            msg = "---- %s has exited ----"%user
            #유저 목록에서 방금 종료한 유저의 정보를 삭제
            del user_list[user]
            msg_func(msg)
            break

        elif "/ls" in string:
            if len(room_list) == 0:
                try:
                    client_socket.send("no room created".encode('utf-8'))
                #msg_func(msg)
                except:
                    print('NO WAY')
            
            else:
                try:
                    client_socket.send('---ROOM LIST---\n'.encode('utf-8'))
                    for i in room_list:
                        msg = i
                        client_socket.send(msg.encode('utf-8'))
                        client_socket.send('\n'.encode('utf-8'))
                except:
                    print('No WAY')
        

        elif "/create" in string:
            string_list = list(string.split())
            room_name = string_list[1]
            room_list.append(room_name)
            room_user[room_name] = set()
            room_user[room_name].add(client_socket)
            user_room[client_socket] = set()
            user_room[client_socket].add(room_name)
            msg = 'Room created'
            print(client_socket)
            try:
                client_socket.send(msg.encode('utf-8'))
            except:
                print('No WAY')


        #elif "/join" in string:
                
        else:
            string = "%s : %s"%(user, string)
            msg_func(string)
    client_socket.close()



def handle_notice(client_socket, addr, user):
    pass



def accept_func():
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(5)

    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            server_socket.close()
            print("Keyboard interrupt")
            break
        user = client_socket.recv(1024).decode('utf-8')
        user_list[user] = client_socket

        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
        notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr, user))
        notice_thread.daemon = True
        notice_thread.start()

        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,user))
        receive_thread.daemon = True
        receive_thread.start()


if __name__ == '__main__':
    #parser와 관련된 메서드 정리된 블로그 : https://docs.python.org/ko/3/library/argparse.html
    #description - 인자 도움말 전에 표시할 텍스트 (기본값: none)
    #help - 인자가 하는 일에 대한 간단한 설명.
    parser = argparse.ArgumentParser(description="\nJoo's server\n-p port\n")
    parser.add_argument('-p', help="port")

    args = parser.parse_args()
    try:
        port = int(args.p)
    except:
        pass
    accept_func()
