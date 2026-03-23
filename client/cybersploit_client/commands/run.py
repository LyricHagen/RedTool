from ..commands import Command
from ..util.config import DEFAULT_IP, DEFAULT_PORT
import socket
import argparse
import shlex
import json
import base64

class NoExitArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise argparse.ArgumentError(None, message)

def receive_until_delimiter(sock, delimiter=b'\0'):
    buffer = b''
    while True:
        chunk = sock.recv(1) # Read 1 byte at a time
        if not chunk or chunk == delimiter:
            break
        buffer += chunk
    return buffer

def process_lines(lines: str):
    parser = NoExitArgumentParser(description="Runs a command on a specified host and returns the output.")
    parser.add_argument("--ip", "-i", type=str, default=DEFAULT_IP, help="The destination IP address (default: %(default)s).")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, help="The destination port (default: %(default)s).")
    parser.add_argument("--type", "-t", choices=["python", "linux", "bash"], help="Type of command: Python or Linux/Bash (interchangeable).")
    parser.add_argument("command", type=str, help="The command to send, including its arguments, if applicable.")
    #TODO: allow multi-line commands..?


    arguments = shlex.split(lines)
    try:
        args = parser.parse_args(arguments)
    except argparse.ArgumentError as e:
        print(f"Argument error: {e}")
        return

    dst_ip = args.ip
    dst_port = args.port
    type = args.type
    data_to_send = args.command

    packet_dict = {"type": type, "command": data_to_send}

    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((dst_ip, dst_port))
    #TODO: handle socket.gaierror: [Errno -2] Name or service not known
    #TODO: handle rejected connection 

    # Send data to server
    json_packet = json.dumps(packet_dict)
    client_socket.send(json_packet.encode())

    # Receive server response
    raw_b64_response = receive_until_delimiter(client_socket)

    client_socket.close()


    if not raw_b64_response:
        print("No response received from server.")
        return

    try:
        #Parse the JSON response
        json_string = base64.b64decode(raw_b64_response).decode('utf-8')
        response_dict = json.loads(json_string)
        
        output = response_dict.get("output", "")
        encoding = response_dict.get("encoding", "text")

        print("Data received from server -->")
        
        if encoding == "base64":
            decoded_data = base64.b64decode(output)
            print(f"[Binary Data Received: {len(decoded_data)} bytes]")
            print(decoded_data) 
        else: #Standard text output
            print(output)

    except json.JSONDecodeError:
        print("Error: Could not decode JSON from server. Check the server output.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # End copied code

class Run(Command): 
    """Return the output of a Linux or Python command run on a remote machine"""
    
    def do_command(self, lines: str, *args):
        process_lines(lines)

command = Run
