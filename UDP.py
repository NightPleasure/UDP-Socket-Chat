import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('localhost', 1234))
broadcast_address = '<broadcast>'

while True:
    message = input("Enter your message: ")
    sock.sendto(message.encode(), (broadcast_address, 1234))

    data, address = sock.recvfrom(1024)
    print("{}: {}".format(address, data.decode()))