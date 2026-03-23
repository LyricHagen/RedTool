from ..commands import Command 
from ..util.net import print_default_command_output

class Whoami(Command):
    """
    Print output of running whoami on the target machine.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("whoami")


command = Whoami 