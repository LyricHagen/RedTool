from ..commands import Command
import socket
import argparse
import shlex


def process_lines(lines: str):
    parser = argparse.ArgumentParser(description="Send data to a target IP and port.")
    parser.add_argument("--ip", "-i", type=str, default="0.0.0.0", help="The destination IP address (default: %(default)s).")
    parser.add_argument("--port", "-p", type=int, default="2956", help="The destination port (default: %(default)s).")
    parser.add_argument("data", type=str, help="The data to send.")


    arguments = shlex.split(lines)
    args = parser.parse_args(arguments)

    dst_ip = args.ip
    dst_port = args.port
    data_to_send = args.data

    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((dst_ip, dst_port))

    # Send data to server and print response
    client_socket.send(data_to_send.encode())
    response = client_socket.recv(2048) # Can call multiple times to get more data
    print(
        "Data received from server -->\n", response.decode()
    )  # Decode bytes to string before printing

    # Close socket
    client_socket.close()

class SendData(Command):
    """Send data over the socket"""
    
    def do_command(self, lines: str, *args):
        process_lines(lines)

command = SendData
