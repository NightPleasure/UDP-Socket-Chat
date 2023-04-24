import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('', 1234))

# Store the user's nickname
nickname = input("Enter your nickname: ")

# Store a mapping of addresses to nicknames
nickname_map = {}


def receive_messages():
    while True:
        data, address = sock.recvfrom(1024)
        message = data.decode()

        # Extract the nickname from the message (if present)
        if ':' in message:
            nickname, message = message.split(':', 1)
            nickname_map[address] = nickname.strip()

        # Print the message with the sender's nickname (if available)
        nickname = nickname_map.get(address, str(address))
        print("{}: {}".format(nickname, message.strip()))


receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()

while True:
    message = input("\nEnter your message: ")

    if message.startswith('@'):
        # Private message
        parts = message.split(' ', 1)
        if len(parts) < 2:
            print('Usage: @<nickname> <message>')
            continue

        nickname, message = parts
        message = "{} (private): {}".format(nickname, message)
        for address, name in nickname_map.items():
            if name == nickname:
                sock.sendto(message.encode(), address)
                break
        else:
            print('No user with nickname {} found'.format(nickname))
            continue

    else:
        # Broadcast message
        message = "{}: {}".format(nickname, message)
        sock.sendto(message.encode(), ('<broadcast>', 1234))
