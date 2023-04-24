import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('', 1234))

# Store a mapping of addresses to nicknames
nickname_list = {}


def receive_messages():
    while True:
        data, address = sock.recvfrom(1024)
        message = data.decode()

        # Extract the nickname from the message (if present)
        if ':' in message:
            nickname, message = message.split(':', 1)
            nickname_list[address] = nickname.strip()

        # Print the message with the sender's nickname (if available)
        nickname = nickname_list.get(address, str(address))
        print("{}: {}".format(nickname, message.strip()))


receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()

while True:
    message = input("\nEnter your message: ")
    nickname = input("Enter your nickname: ")

    # Send the message with the nickname as a prefix
    message = "{}: {}".format(nickname, message)
    sock.sendto(message.encode(), ('<broadcast>', 1234))
