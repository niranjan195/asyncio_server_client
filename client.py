from test_server import Client
import sys
UNIX_PATHNAME="/home/niranjan/Desktop/server.socket"


if len(sys.argv) != 3:
    print ("Usage: client.py host port")
    sys.exit(1)
else:
    host = sys.argv[1]
    port = int(sys.argv[2])
    client = Client()

def main():
    # client.connect_stream_socket(host,port)
    client.connect_unix_socket(UNIX_PATHNAME)
    while True:
        data = input("Enter data: ")
        # data= "HEllo"
        client.send(data)
        data = client.recv()
        print (data)
    # client.send("quit")
    # client.close()
