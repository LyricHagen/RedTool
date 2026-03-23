from ..commands import Command 
from ..util.net import print_default_command_output

class SUIDPrivesc(Command):
    """
    Performs privilege escalation via an executable with misconfigured SUID bit.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("suid_privesc")


command = SUIDPrivesc 