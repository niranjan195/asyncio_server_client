'''
Implements asynchronous Server to handle multiple clients using event loops
'''


import os
import asyncio
from test_server import Server

# pathname for unix socket
UNIX_PATHNAME = "/home/niranjan/server.socket"


# if socket file exists delete it
if UNIX_PATHNAME and os.path.exists(UNIX_PATHNAME):
    print("File already exists. Removing it now")
    os.remove(UNIX_PATHNAME)
    print("File removed")


def handle_data(data, addr, client_sock=None, transport=None):
    '''
    Callback function to handle the data sent by the client.
    '''
    print("Received data from ", addr, " is ", data)
    client_data = str(addr) + " " + data.decode()
    print("Sending to ", addr, " data ", client_data)
    if client_sock:
        loop.create_task(server.send(loop, client_sock, client_data))
    elif transport:
        transport.sendto(client_data.encode(), addr)


def run():
    '''
    Function to start the async server
    '''
    while True:
        client, addr = loop.run_until_complete(
            server.accept(loop, handle_data))
        # print(client, addr)
        if client:
            loop.create_task(server.recv(
                loop, client, addr, handle_data))


if __name__ == "__main__":
    # pylint: disable=invalid-name
    server = Server(host="127.0.0.1", port=9000, pathname=UNIX_PATHNAME)
    loop = asyncio.get_event_loop()
    run()
