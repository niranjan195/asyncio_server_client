from test_server import Server
import sys, asyncio
UNIX_PATHNAME = "/home/niranjan/Desktop/server.socket"


if len(sys.argv) != 3:
    print ("usage: test_server.py host port")
    sys.exit(1)
try:
    host = sys.argv[1]
    port = int(sys.argv[2])
except:
    pass

s = Server()
# s.create_stream_socket(host,port)
s.create_unix_socket(UNIX_PATHNAME)
loop = asyncio.get_event_loop()
try:
    while True:
        client, addr = loop.run_until_complete(s.accept(loop))
        print ("Connected to ", addr)
        data = "Hello to" + str(addr) + '\n'
        loop.create_task(s.recv(client,loop))
        # loop.create_task(s.send(client,loop,data))
except Exception as e:
    print (e)
