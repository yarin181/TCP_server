# TCP,HTTP Server in Python 💾

This is a simple HTTP server written in Python that serves static files from the `files` directory. The server listens for incoming connections and reads the client's request to get the requested file path. If the requested file is found, it is sent back to the client in HTTP format. If the file is not found, the server returns a 404 status code.

## Requirements

-   Python 3.9
-   Socket module

## How to Run

1.  Clone the repository to your local machine.
2.  Navigate to the project directory.
3.  Run the command `python3 http_server.py <port_number>` where `port_number` is the port you want to use for the server.
4.  Open a web browser and navigate to `http://localhost:[path]<port_number>` to see the server in action, by leaving the path empty you will get the home page , you can also insert a pathe from the files folder (e.g `c/Footube.html`).

## Code Explanation

The code begins by importing the necessary modules and defining some constants, including the buffer size and the request separator.

Next, a `ClientData` class is defined to hold the relevant data sent from the client, including the file path and connection state. This class includes two static methods for parsing the client data: `find_connection` and `find_path`.

A `format_message_to_the_client` function is defined to create the HTTP response message that will be sent back to the client. This function takes in a status code, status message, connection state, and content length, and returns the appropriate HTTP response message.

The `main` function is the entry point for the server. It starts by checking the command-line arguments to get the port number, creates a socket, binds it to the port, and listens for incoming connections.

When a connection is received, the server reads the client's request and parses it using the `ClientData` class. If the requested file is found, the server reads the file and sends it back to the client in HTTP format. If the file is not found, the server returns a 404 status code.

The server continues to read and respond to client requests until the connection is closed or a socket timeout exception is caught.
