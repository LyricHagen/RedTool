from ..commands import Command 
from ..util.net import print_default_command_output

class Cron(Command):
    """
    Edit the crontab on the target machine to continuously install our server.py file.
    """
    
    def do_command(self, lines: str):
        print_default_command_output("crontabbb")


command = Cron 
