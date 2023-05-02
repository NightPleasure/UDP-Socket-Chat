import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('', 40404))

try:
    nickname = input("Enter your nickname: ")
except KeyboardInterrupt:
    print("\nExiting program...")
    exit()

nickname_map = {}


def receive_messages():
    while True:
        try:
            data, address = sock.recvfrom(40404)
            message = data.decode()

            if ':' in message:
                nickname, message = message.split(':', 1)
                nickname_map[address] = nickname.strip()

            nickname = nickname_map.get(address, str(address))
            if message.startswith("(privat) "):
                print("{}({}): {}".format(nickname, address, message.strip()))
            else:
                print("{}({}): {}".format(nickname, address, message.strip()))
        except socket.error as e:
            print("Error receiving message: {}".format(e))


receiver_thread = threading.Thread(target=receive_messages).start()

while True:
    try:
        message = input("Enter your message: \n")

        if message.startswith('/pm '):
            parts = message.split(' ')
            if len(parts) == 3:
                ip = parts[1].strip()
                message = "(privat) {}: {}".format(nickname, parts[2].strip())
                try:
                    sock.sendto(message.encode(), (ip, 40404))
                    print("Sent private message to {}".format(ip))
                except socket.error as e:
                    print("Error sending private message: {}".format(e))
            else:
                print("Invalid private message format. Usage: /pm IP_ADDRESS MESSAGE")
        else:
            message = "{}: {}".format(nickname, message)
            try:
                sock.sendto(message.encode(), ('<broadcast>', 40404))
            except socket.error as e:
                print("Error sending message: {}".format(e))
    except KeyboardInterrupt:
        print("\nExiting program...")
        exit()
