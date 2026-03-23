from ..commands import Command 
from ..util.net import print_default_command_output

class SUIDPrivesc(Command):
    """
    Plays an audio on the target machine.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("playaudio")


command = SUIDPrivesc 