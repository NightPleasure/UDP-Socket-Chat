import socket
import threading

HOST = '127.0.0.1'
PORT = 40404

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', 0))
    print("..........::::::::::Conexiune realizata::::::::::..........")
    name = input("\n- Cum te numesti?: ")
    print("\n---------------------------CHAT----------------------------\n")
    client.sendto(name.encode('utf-8'), (HOST, PORT))

except Exception as e:
    print("A aparut o eroare la conectarea catre server:", e)
    exit()


def send_info():
    while True:
        try:
            message = input()
            client.sendto(message.encode('utf-8'), (HOST, PORT))

        except Exception as e:
            print("A aparut o eroare la transmiterea datelor catre server:", e)
            exit()


def receive_info():
    while True:
        try:
            message, server_address = client.recvfrom(1024)
            print(message.decode('utf-8'))
        except Exception as e:
            print("A aparut o eroare la primirea datelor de catre server:", e)
            exit()


send_thread = threading.Thread(target=send_info).start()
receive_thread = threading.Thread(target=receive_info).start()
