from abc import ABC

__all__ = [
    "exit",
    "port_scan",
    "run",
    "suid_scan",
    "privesc",
    "whoami",
    "cron",
    "struct",
    "tomcat",
    "ftp",
    "shellshock",
    "suid_privesc",
    "play_audio",
    "screenshot",
    "etc_privesc",
    "systemd"
]


class Command(ABC):
    """A command that does something"""

    def do_command(self, lines: str, *args):
        raise NotImplementedError()
