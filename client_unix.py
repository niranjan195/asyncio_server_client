'''
Implements Unix Socket to communicate to the server
'''
from test_server import Client

# Unix socket path name
UNIX_PATHNAME = '/home/niranjan/server.socket'


def run_client():
    '''
    Function to run the Unix client socket
    '''
    client = Client(pathname=UNIX_PATHNAME)
    count = 0
    while count != 15:
        data = str(count) + "UNIX"
        # data = input("Enter data")
        count += 1
        print("Sending data", data)
        client.send(data)
        data = client.receive()
        print("Received data", data)
    client.close()


if __name__ == "__main__":
    run_client()
