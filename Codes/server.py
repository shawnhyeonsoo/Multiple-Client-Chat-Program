import socket
import threading
import time
import sys

host = "127.0.0.1" 
port = 4000
user_list = {}
notice_flag = 0
room_list = []
room_user = {}
user_room = {}
user_log = []
socket_name = []
room_namelist = {}
real_user_list= []

def msg_send(client_socket,addr, msg):     # to send to clients in the same chat room
    room = user_room[client_socket]
    for con in room_user[room]:
        if con == client_socket:
            pass
        else:
            try:
                con.send(msg.encode('utf-8'))
            except:
                print('abnormal connection')



def msg_func(msg):                  #to send to clients in the server
    for con in user_list.values():
        try:
            con.send(msg.encode('utf-8'))
        except:
            pass


def handle_receive(client_socket, addr): #handles different commands from the client
    user_room[client_socket] = ''
    print("New client has been conencted")
    while 1:
        data = client_socket.recv(1024)
        string = data.decode('utf-8')

        if "/exit" in string:
            msg = "---- %s has exited ----"%user
            del user_list[user]
            msg_func(msg)
            break

        elif "/ls" in string:
            if len(room_list) == 0:
                try:
                    client_socket.send("no room created".encode('utf-8'))
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
            if user_room[client_socket] != '':   # if the client socket already has a room
                try:
                    client_socket.send("Cannot Create: client is already in a chat room".encode('utf-8'))
                except:
                    pass
            else:
                string_list = list(string.split())
                room_name = string_list[1]
                if len(string_list) >= 3:
                    user= string_list[2]
                else:
                    user = "Unknown"
                real_user_list.append(client_socket)
                room_list.append(room_name)
                room_user[room_name] = set()
                room_user[room_name].add(client_socket)
                user_room[client_socket]= room_name
                user_list[user] = client_socket
                room_namelist[room_name] = set()
                room_namelist[room_name].add(user)
                msg = 'Room created'
                try:
                    client_socket.send(msg.encode('utf-8'))
                except:
                    print('No WAY')


        elif "/join" in string:
            if user_room[client_socket] != '':
                try:
                    client_socket.send("Cannot join: client is already in a chat room".encode('utf-8'))
                except:
                    pass
            else:
                string_list = list(string.split())
                room_name = string_list[1]
                if len(string_list) >= 3:
                    user= string_list[2]
                else:
                    user= "Unknown"

                real_user_list.append(client_socket)
                room_user[room_name].add(client_socket)
                user_room[client_socket]= room_name
                user_list[user] = client_socket
                room_namelist[room_name].add(user)
                msg = "----%s has entered----"%user
                try:
                    msg_send(client_socket,addr,msg)
                except:
                    print('NO WAY')
        
        elif "/whisper" in string:
            string_list = list(string.split())
            target = string_list[1]
            message = "(whisper from)%s :  "%user + " ".join(string_list[2:])
            if target in room_namelist[user_room[client_socket]]:
                try:
                    user_list[target].send(message.encode('utf-8'))
                except:
                    pass
            else:
                    client_socket.send("Target not in this room".encode('utf-8'))

        else:
            if user_room[client_socket] != '':
                string = "%s : %s"%(user, string)
                msg_send(client_socket, addr, string)
            else:
                try:
                    client_socket.send('inappropriate command; not participated in any room'.encode('utf-8'))
                except:
                    pass
    client_socket.close()



def handle_notice(client_socket, addr):
    pass


def server_input():     #inputs handled by the server e.g. kill
    while True:
        keyin = input()
        if keyin == '/ls':
            print('---Room List---')
            for i in room_list:
                print(i)
        elif '/kill' in keyin:
            keyin_str = list(keyin.split())
            room_name = keyin_str[1]
            for con in room_user[room_name]:
                try:
                    con.send('Room has been killed'.encode('utf-8'))
                    user_room[con] = ''
                except:
                    pass
            print("%s is killed"%room_name)
            del room_user[room_name]
            room_list.remove(room_name)
        elif "/exit" in keyin:
            for con in real_user_list:
                con.close()
                break
        else:
            print("Inappropriate Command\n")



def accept_func():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while 1:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            server_socket.close()
            print("Keyboard interrupt")
            break

        user_list[client_socket] = client_socket
        notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr,))
        notice_thread.daemon = True
        notice_thread.start()

        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,))
        receive_thread.daemon = True
        receive_thread.start()


if __name__ == '__main__':
    server_thread = threading.Thread(target=server_input, args = ())
    server_thread.daemon = True
    server_thread.start()
    accept_func()
    server_thread.start()
