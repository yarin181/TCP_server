import socket
import sys 
import os

""" _summary_ 
    this class stands for the relevant data that sends from the user which is it , the path of the file 
    and the connection state.
"""
class ClientData:
    def __init__(self,data_array):
        #on this location theres the path of the file.
        self._path = ClientData.find_path(data_array)
        #gets the connection state from find_connection func.
        self._connection = ClientData.find_connection(data_array)

    """_summary_
            this function get data array and return the sate of the connection 
            label.
        Args:
            data_array (_type_): string array
            array of the client data.
        Returns:
            _type_: string
            the connection state 
    """
    @staticmethod    
    def find_connection(data_array):
        for data in data_array:
            #only if the label length is grater than 12 it could be the connection
            #label and than ensure its the right one by name.
            #finlay return the connection state string.
            if (len(data) > 12 and data[:10] == "Connection"):
                return data[12:]
    
    @staticmethod
    def find_path(data_array):
        if (data_array[0])[4:-9] == "/":
            return "/index.html"
        else:
            return (data_array[0])[4:-9]

"""_summary_
        This function arrange the inserted data in a http format for sending to the user.
    Args:
        status_number int:
        200 - the file is found
        404 - file not found 
        301 - the client asked for file in the name of "redirected"
    
        status  string :
        OK - file found .
        Not Found - the file not founded.
        Moved Permanently - the client asked for file in the name of "redirected"

        connection_status string: 
        "keep-alive" or "close" 

        content_length int: 
        the content length

    returns an appropriate string.
"""
def format_message_to_the_client(status_number,status,connection_status,content_length):
    if (status_number == 200):
        return "HTTP/1.1 {} {} \r\nConnection: {}\r\nContent-Length: {}\r\n\r\n".format(status_number,status,connection_status,content_length)
    if (status_number == 404):
        return "HTTP/1.1 {} {} \r\nConnection: {}\r\n\r\n".format(status_number,status,connection_status)
    if (status_number == 301):
        return "HTTP/1.1 {} {} \r\nConnection: {}\r\nLocation: {}\r\n\r\n".format(status_number,status,connection_status,content_length)


def main():
    
    if len(sys.argv) != 2:
        server.close()
        sys.exit(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(sys.argv[1])))
    server.listen(5)

    while True:
        client_socket, client_address = server.accept()
        #if the client won't send date within a second a timeoutError will raise.
        client_socket.settimeout(1)

        while True:
            try:
                data = client_socket.recv(4096).decode()
                splitted_data = data.split("\r\n")
            except TimeoutError:
                #debug message
                #print('Client disconnected(timeout)', client_address)
                break
            if (len(data) == 0):
                break

            # print the request
            print(data)

            clientData  = ClientData(splitted_data)
            isFile = os.path.isfile("files"+clientData._path)

            #debug messages
            #print("path:", "_",clientData._path,"_")
            #print("connection:","_",clientData._Connection,"_")
            #print(isFile)
            
            if(clientData._path == "/redirect"):
                client_socket.send((format_message_to_the_client(301,"Moved Permanently","close","/result.html")).encode())
                break
            elif isFile:
                filepath = "files" + clientData._path
                f = open("files"+clientData._path,"rb")
                client_socket.send((format_message_to_the_client(200,"OK",clientData._connection,os.stat(filepath).st_size)).encode())
                client_socket.sendfile(f)
            else:
                client_socket.send((format_message_to_the_client(404,"Not Found","close",0)).encode())
                break
            if(clientData._connection == "close"):
                # debug message
                #print('Client disconnected')
                break

        client_socket.close()

if __name__ == "__main__":
    main()