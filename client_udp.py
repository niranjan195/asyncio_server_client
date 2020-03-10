'''
Implements UDP Socket to communicate to the server
'''
import socket


SERVER_ADDRESS = ('localhost', 9000)


def run_client():
    '''
    Function to run the UDP client socket
    '''
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count = 0
    while count != 15:
        message = str(count) + "udp"
        # message = input("Enter data")
        count += 1
        udp_socket.sendto(message.encode(), SERVER_ADDRESS)
        data, server = udp_socket.recvfrom(1024)
        print("Data recevied from", server, " is ", data)
    udp_socket.close()


if __name__ == "__main__":
    run_client()
