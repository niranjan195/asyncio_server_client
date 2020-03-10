'''
Implements Tcp Socket to communicate to the server
'''
from test_server import Client


def run_client():
    '''
    Function to run the Tcp client socket
    '''
    tcp_client = Client(host="localhost", port=9000)
    count = 0
    while count != 15:
        data = str(count) + "tcp"
        # data = input("Enter data")
        count += 1
        print("Sending data", data)
        tcp_client.send(data)
        data = tcp_client.receive()
        print("Received data", data)
    tcp_client.close()


if __name__ == "__main__":
    run_client()
