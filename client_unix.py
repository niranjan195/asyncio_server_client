'''
Implements Unix Socket to communicate to the server
'''

from test_server import Client

# Unix socket path name
UNIX_PATHNAME = ''


def main():
    c = Client(pathname=UNIX_PATHNAME)
    count = 0
    while count != 15:
        data = input("Enter data")
        count += 1
        print("Sending data", data)
        c.send(data)
        data = c.receive()
        print("Received data", data)
    c.close()


main()
