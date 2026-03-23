import socket
from ..util.config import DEFAULT_PORT, DEFAULT_IP

def print_default_command_output(cmd, ip=DEFAULT_IP, port=DEFAULT_PORT):
    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    #TODO: handle socket.gaierror: [Errno -2] Name or service not known
    #TODO: handle rejected connection 

    # Send data to server and print response
    client_socket.send(cmd.encode())
    response = client_socket.recv(2048) # Can call multiple times to get more data
    if not response:
        print("No response from server.") 
    else:
        print(
            "Data received from server -->\n", response.decode()
        )  # Decode bytes to string before printing

    # Close socket
    client_socket.close()