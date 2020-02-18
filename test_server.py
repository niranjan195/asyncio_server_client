import asyncio, socket


class Server:
    """
    Asynchronous Server using asyncio module using sockets
    """

    def create_unix_socket(self,pathname):
        '''
        Creates unix socket
        '''

        self.socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        try:
            self.socket.bind(pathname)
            self.socket.listen(1)
            self.socket.setblocking(False)
        except Exception as e:
            print (e)

    def create_stream_socket(self,host,port):
        '''
        Creates TCP Stream socket
        '''

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.socket.bind((host,port))
            self.socket.listen(1)
            self.socket.setblocking(False)
        except Exception as e:
            print (e)

    async def accept(self,loop):
        '''
        Establishes connection with the client
        '''

        client, addr = await loop.sock_accept(self.socket)
        return client, addr    

    async def recv(self, client, loop):
        '''
        Handles data receiving in asynchronous manner
        '''

        data = None
        while data != "quit":
            try:
                data = (await loop.sock_recv(client, 255)).decode('utf8')
                if not data:
                    break
                await self.send(client,loop,data)
                print ("Data recieved is", data)
            except Exception as e:
                print ("Connection closed by the client")
                break
        self.close_client(client)
    
    async def send(self, client, loop, data):
        '''
        Sends data to the client
        '''

        try:
            await loop.sock_sendall(client, data.encode('utf8'))
        except:
            self.close_client(client)

    def close_client(self,client):
        '''
        Close the client connection
        '''

        print ("Closing connection with the client")
        client.close()


class Client:
    """
    Class for client socket    
    """

    def connect_stream_socket(self,host,port):
        '''
        Initalises connection to the server as TCP stream socket
        '''

        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address = (host, port)
        self.client_socket.connect(server_address)

    def connect_unix_socket(self,pathname):
        '''
        Initialises connection to the server as UNIX stream socket
        '''
        self.client_socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.client_socket.connect(pathname)

    def send(self,data):
        '''
        Sends the request to the server
        '''
        
        try:
            self.client_socket.send(data.encode())
        except:
            print ("Cannot send data to the server")
            self.close()

    def recv(self,size=1024):
        '''
        Receives the response from the server
        '''

        data = self.client_socket.recv(size)
        return data

    def close(self):
        '''
        Closes the connection with the server
        '''
    
        print ("Closing connection with the Server")
        self.client_socket.close()
