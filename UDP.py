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

def send_private_message():
    while True:
        input_string = input('')
        if input_string.startswith('/pm'):
            inputs = input_string.split(' ')
            recipient_nickname = inputs[1]
            message = ' '.join(inputs[2:])
            for address, nickname in nickname_map.items():
                if nickname == recipient_nickname:
                    message = "{} (private): {}".format(nickname, message)
                    sock.sendto(message.encode(), (address[0], 1234))
                    break
        else:
            message = "{}: {}".format(nickname, input_string)
            sock.sendto(message.encode(), ('<broadcast>', 1234))

receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()

sender_thread = threading.Thread(target=send_private_message)
sender_thread.daemon = True
sender_thread.start()

while True:
    pass
