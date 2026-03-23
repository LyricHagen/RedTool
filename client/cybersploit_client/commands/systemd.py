from ..commands import Command
from ..util.net import print_default_command_output

class Systemd(Command):
    """
    Install a systemd service on the target machine to persist the payload.
    """

    def do_command(self, lines: str):
        print_default_command_output("systemd_persist")

command = Systemd