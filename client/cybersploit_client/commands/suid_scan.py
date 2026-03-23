from ..commands import Command 
from ..util.net import print_default_command_output

class SUIDScan(Command):
    """
    Prints a list of all files in /usr/bin with SUID bits set that are likely misconfigured.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("suid")


command = SUIDScan 