# chat_client.py
# Simple TCP/IP chat client

import argparse
import select
import socket
import sys

def chat_client():
    """Creates a TCP/IP socket for connection to the chat server.
    Usage example:
    python chat_client.py 192.168.0.1 9009
    The server should be launched on IP address: 192.168.0.1 and port: 9009.
    """
    parser = argparse.ArgumentParser(description='TCP chat client.')
    parser.add_argument('host', nargs='?', default='localhost', \
                         help='host name or IP address of the server')
    parser.add_argument('port', nargs='?', default='9009', help='port to connect')
    args = parser.parse_args()
    # Host name or IP address
    host = args.host
    # Connection port
    port = int(args.port)
    # Create a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect.')
        sys.exit()

    print('Connected to remote host. You can start sending messages.')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list of sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list,\
                                                                   [], [])

        for sock in read_sockets:
            if sock == s:
                # Incoming message from remote server, s
                message = sock.recv(4096)
                if not message:
                    print('\nDisconnected from chat server.')
                    sys.exit()
                else:
                    # Print message
                    sys.stdout.write(message)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

            else:
                # User entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Me] ')
                sys.stdout.flush()

if __name__ == "__main__":
    chat_client()
