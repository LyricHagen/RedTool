from ..commands import Command 
from ..util.net import print_default_command_output

class etc_privesc(Command):
    """
    Performs privilege escalation via editing the /etc/shadow file and deletes insecure-duck.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("etc_privesc")


command = etc_privesc 