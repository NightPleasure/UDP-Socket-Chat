import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 40404))

clients = {}


def server_send():
    server_message = input()
    for cl in clients:
        server.sendto(server_message.encode("utf-8"), clients[cl])


def handle_clients():
    while True:
        message, client_address = server.recvfrom(1024)
        message = message.decode('utf-8')

        if client_address in clients:
            if message == '/q':
                client_name = clients[client_address]
                del clients[client_address]
                print(f'{client_name} has left the chat')
            else:
                client_name = clients[client_address]
                print(f'{client_name}: {message}')
                for addr in clients:
                    if addr != client_address:
                        server.sendto(f'{client_name}: {message}'.encode('utf-8'), addr)
        else:
            clients[client_address] = message
            print(f'{message} has joined the chat')


handle_thread = threading.Thread(target=handle_clients()).start()
