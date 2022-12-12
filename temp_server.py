import os
import socket
import sys
import os.path
from os import path

BUFFER_SIZE = 1024
NUMBER_OF_CLIENTS = 5


def handle_client(data, client_socket):
    """
    handle_client function responsible for sending the client the answer he is waiting for.
    treats redirect and an error separately.
    param data- request from client
    param client_socket- the socket to communicate with current client
    returns: True if the connection needs to stay alive, False otherwise
    """
    connection = ""
    keep_alive = False
    first_line = data.partition("\r\n")[0]
    my_path = "files" + first_line.split(" ")[1]
    # handles with scenario that there is redirect
    if my_path == "files/redirect":
        client_socket.send(
            "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n".encode())
        return keep_alive
    # checks if the file exists
    if path.exists(my_path):
        length = os.stat(my_path).st_size
        # finds the line with the connection word
        for line in data.split("\r\n"):
            if "Connection:" in line:
                connection = line.split(" ")[1]
                break
        if connection == "keep-alive":
            keep_alive = True
        message = f"HTTP/1.1 200 OK\r\nConnection: {connection}\r\nContent-Length: {length}\r\n\r\n"
        # handles with scenario that there is a /
        if my_path[-1:] == "/":
            my_path += "index.html"
        file = open(my_path, "rb")
        binary = file.read()
        file.close()
    else:
        client_socket.send("HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode())
        return keep_alive
    # sends complete message to client
    client_socket.send(message.encode() + binary)
    return keep_alive


def main():
    """
    main function responsible for opening a listening socket.
    gets the requests from the clients connected to the socket and handles them.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(sys.argv[1])))
    server.listen(NUMBER_OF_CLIENTS)
    while True:
        close_connection = False
        client_socket, client_address = server.accept()
        data = ""
        while True and not close_connection:
            client_socket.settimeout(1)
            # receives data from client. if there is a timeout we close the socket
            try:
                received = client_socket.recv(BUFFER_SIZE).decode()
                # closes the socket when received an empty message
                if not len(received):
                    client_socket.close()
                    break
                data += received
                # separates between a couple of messages that entered the data variable together
                while "\r\n\r\n" in data:
                    messages_parts = data.partition("\r\n\r\n")
                    print(messages_parts[0])
                    print()
                    if not handle_client(messages_parts[0], client_socket):
                        client_socket.close()
                        close_connection = True
                        break
                    data = messages_parts[2]
            except socket.timeout as e:
                client_socket.close()
                break


if __name__ == '__main__':
    main()