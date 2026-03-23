from ..commands import Command 
from ..util.net import print_default_command_output

class Privesc(Command):
    """
    Attempt to re-execute server.py with root privileges by prompting user for credentials.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("custompwdhere")


command = Privesc 
