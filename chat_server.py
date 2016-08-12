# chat_server.py
# Simple TCP chat server

import argparse
import select
import socket
import sys

SOCKET_LIST = []
RECV_BUFFER = 4096

def chat_server():
    """Creates a TCP/IP chat server.
    Usage example:
    python chat_server.py 192.168.0.1 9009
    and then run the clients:
    python chat_client.py 192.168.0.1 9009
    """
    parser = argparse.ArgumentParser(description='TCP chat server.')
    parser.add_argument('host', nargs='?', default='localhost', \
                         help='host name or IP address of the server')
    parser.add_argument('port', nargs='?', default='9009', help='port to connect')
    args = parser.parse_args()
    # Host name or IP address
    host = args.host
    # Connection port
    port = int(args.port)
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)
    # Add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    print("Chat server started on port " + str(port))

    while 1:

        # Get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            # A new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                broadcast(server_socket, sockfd, \
                          "[%s:%s] entered our chatting room\n" % addr)

            # A message from a client, not a new connection
            else:
                # Process data recieved from client
                try:
                    # Receiving data from the socket.
                    message = sock.recv(RECV_BUFFER)
                    if message:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + \
                                  str(sock.getpeername()) + '] ' + message)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # At this stage, no data means probably the connection
                        # has been broken
                        broadcast(server_socket, sock, \
                                  "Client (%s, %s) is offline\n" % addr)

                # exception
                except:
                    broadcast(server_socket, sock, \
                              "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()

# Broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # Send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # Broken socket connection
                socket.close()
                # Remove broken socket
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":
    sys.exit(chat_server())
