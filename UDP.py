import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('', 40404))

nickname = input("Enter your nickname: ")

nickname_map = {}


def receive_messages():
    while True:
        data, address = sock.recvfrom(40404)
        message = data.decode()

        if ':' in message:
            nickname, message = message.split(':', 1)
            nickname_map[address] = nickname.strip()

        nickname = nickname_map.get(address, str(address))
        print("{}: {}".format(nickname, message.strip()))


receiver_thread = threading.Thread(target=receive_messages).start()

while True:
    message = input("\nEnter your message: ")

    if message.startswith('/pm'):
        parts = message.split(':', 2)
        if len(parts) == 3:
            ip = parts[1].strip()
            message = "{}: {}".format(nickname, parts[2].strip())
            sock.sendto(message.encode(), (ip, 40404))
            print("Sent private message to {}".format(ip))
        else:
            print("Invalid private message format. Usage: /pm IP_ADDRESS: MESSAGE")
    else:
        message = "{}: {}".format(nickname, message)
        sock.sendto(message.encode(), ('<broadcast>', 40404))
