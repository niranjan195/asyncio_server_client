'''
Asynchronous Server which listens to unix socket, TCP and UDP sockets using
event loops
'''

import asyncio
import socket
from concurrent.futures import CancelledError


class UDPProtocol:
    '''
    Udp Protocol to receive data from UDP sockets
    '''

    def __init__(self, callback, on_con_lost):
        self.transport = None
        self.callback = callback
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        '''
        Creates new transport for UDP data transfers
        '''
        self.transport = transport

    def datagram_received(self, data, addr):
        """
        UDP protocol for receiving  UDP datagram
        Called Whenever a data is to be received
        """
        self.callback(data, addr, transport=self.transport)

    def connection_lost(self, exc):
        try:
            self.on_con_lost.set_result(True)
        except Exception:
            pass


class Server:
    """
    Asynchronous Server using asyncio module using sockets
    """

    def __init__(self, host="localhost", port=9000, pathname=None):
        self.server_unix_socket = None
        self.server_tcp_socket = None
        self.host = host
        self.port = port
        self.client = None
        self.addr = None
        self.tcp_task = None
        self.unix_task = None
        self.count = 0
        try:
            self.create_stream_socket()
            if pathname:
                self.create_unix_socket(pathname)
        except FileNotFoundError:
            print("File %s not found" % (pathname))
        except OSError:
            print("Address %s already in use" % (pathname))
        except TypeError as exc:
            print(exc)
        except Exception as exc:
            print(exc)
        finally:
            print("Server listening for TCP and UDP sockets on",
                  (self.host, self.port))
            print("Server listening for Unix sockets on", pathname)

    def create_unix_socket(self, pathname):
        '''
        Creates unix socket
        '''
        try:
            self.server_unix_socket = socket.socket(
                socket.AF_UNIX, socket.SOCK_STREAM)
            self.server_unix_socket.bind(pathname)
            self.server_unix_socket.listen(10)
            self.server_unix_socket.setblocking(False)
        except socket.error as err:
            print(err)
        except Exception as exc:
            print(exc)

    def create_stream_socket(self):
        '''
        Creates TCP Stream socket
        '''
        try:
            self.server_tcp_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.server_tcp_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_tcp_socket.bind((self.host, self.port))
            self.server_tcp_socket.listen(10)
            self.server_tcp_socket.setblocking(False)
        except socket.error as exc:
            print(exc)
        except Exception as exc:
            print(exc)

    async def accept_unix_connection(self, loop, unix_socket):
        '''
        Establishes connection with the unix socket
        '''
        # print("Accept unix connection")
        self.client, self.addr = await loop.sock_accept(unix_socket)
        print("Accepted UNIX connection")
        # self.udp_task.cancel()
        self.tcp_task.cancel()
        self.unix_task.cancel()

    async def accept_tcp_connection(self, loop, tcp_socket):
        '''
        Establishes connection with the tcp socket
        '''
        self.client, self.addr = await loop.sock_accept(tcp_socket)
        print("Accepted TCP connection")
        self.unix_task.cancel()
        self.tcp_task.cancel()

    async def udp_connection(self, loop, callback):
        on_con_lost = loop.create_future()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPProtocol(callback, on_con_lost), local_addr=(self.host, self.port))
        try:
            await on_con_lost
        finally:
            transport.close()

    async def accept(self, loop, callback):
        '''
        Establishes connection with the client
        '''
        tasks = []
        if self.server_unix_socket:
            self.unix_task = loop.create_task(self.accept_unix_connection(
                loop, self.server_unix_socket))
            tasks.append(self.unix_task)
        self.tcp_task = loop.create_task(self.accept_tcp_connection(
            loop, self.server_tcp_socket))
        if self.count == 0:
            self.udp_task = loop.create_task(
                self.udp_connection(loop, callback))
        self.count += 1
        tasks.append(self.udp_task)
        tasks.append(self.tcp_task)
        try:
            await asyncio.gather(*tasks)
        except CancelledError:
            pass
        return self.client, self.addr

    async def recv(self, loop, client, addr, size=4096, callback=None):
        '''
        Handles data receiving in asynchronous manner
        '''
        while True:
            try:
                data = (await loop.sock_recv(client, size))
                if not data:
                    break
                if callback:
                    callback(data, addr, client_sock=client)
            except AttributeError as err:
                print(err)
            except Exception as e:
                print("Client closed connection", e)
                client.close()

    async def send(self, loop, client, data):
        '''
        Sends data to the client
        '''
        try:
            await loop.sock_sendall(client, data.encode('utf8'))
        except Exception as e:
            print(e)
            self.close_client(client)

    def close_client(self, client):
        '''
        Close the client connection
        '''

        print("Closing connection with the client")
        client.close()


class Client:
    """
    Class for client socket
    """

    def __init__(self, host="localhost", port=9000, pathname=None):
        self.client_socket = None
        if pathname:
            self.connect_unix_socket(pathname)
        else:
            self.connect_stream_socket(host, port)

    def connect_stream_socket(self, host, port):
        '''
        Initalises connection to the server as TCP stream socket
        '''

        try:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
        except socket.error as err:
            print(err)

    def connect_unix_socket(self, pathname):
        '''
        Initialises connection to the server as UNIX stream socket
        '''

        try:
            self.client_socket = socket.socket(
                socket.AF_UNIX, socket.SOCK_STREAM)
            self.client_socket.connect(pathname)
        except socket.error as err:
            print(err)

    def send(self, data):
        '''
        Sends the request to the server
        '''

        try:
            data = data.encode()
            self.client_socket.send(data)
        except AttributeError as err:
            print(err)
        except Exception as e:
            print("Cannot send data to the server", e)
            self.close()

    def receive(self, size=4096):
        '''
        Receives the response from the server
        '''

        try:
            data = self.client_socket.recv(size)
            return data
        except socket.error as err:
            print(err)
        except Exception as e:
            print(e)

    def close(self):
        '''
        Closes the connection with the server
        '''

        print("Closing connection with the Server")
        self.client_socket.close()
