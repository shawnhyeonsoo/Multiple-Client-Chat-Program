import socket
import argparse
import threading

def handle_receive(client_socket):
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("disconnected")
            break
        data = data.decode('utf-8')
        print(data)

def handle_send(client_socket):
    while 1:
        data = input()
        client_socket.send(data.encode('utf-8'))
        if data == "/exit":
            break
    client_socket.close()


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 4000))
    receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    receive_thread.join()
