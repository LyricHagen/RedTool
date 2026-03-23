from ..commands import Command 
from ..util.config import DEFAULT_IP
import subprocess
import shlex

class FTP(Command):
    """
    Spawn shell via vsftp exploit.
    """
    
    def do_command(self, lines: str):
        cmd_string = f"python3 cybersploit_client/vsftp_exploit.py {DEFAULT_IP}"
        args = shlex.split(cmd_string)
        subprocess.run(args) 
 

command = FTP 