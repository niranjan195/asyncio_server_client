import socket


u1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 9000)

# message = b'HI SERVER'


def main():
    print("client set")
    count = 0
    while count != 15:
        # message = str(count) + "udp"
        message = input("Enter data")
        count += 1
        u1.sendto(message.encode(), server_address)
        data, server = u1.recvfrom(1024)
        print("Data recevied from server is ", data)
    u1.close()


main()
