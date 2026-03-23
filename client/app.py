PROJECT_NAME = "cybersploit_client" 

from cmd import Cmd
import importlib
commands = importlib.import_module(f"{PROJECT_NAME}.commands") 
import sys
import readline


def add_command(cmd_name, func, docstring, cmd):
    """Add a new command to the cmdclass."""
    setattr(cmd, "do_" + cmd_name, func)
    setattr(cmd, "help_" + cmd_name, lambda self: print(docstring))


class CustomCommand(Cmd):

    def parse_args(provided_args, expected_args=""):
        return provided_args.split(" ")

    def __init__(self):
        super().__init__()
        self.prompt = "> "

if __name__ == "__main__":
    all_commands = commands.__all__
    for command in all_commands:
        module: commands.Command = importlib.import_module(
            f"{PROJECT_NAME}.commands.{command}"
        ).command
        add_command(
            command, getattr(module, "do_command"), module.__doc__, CustomCommand
        )

    exit_module = importlib.import_module(f"{PROJECT_NAME}.commands.exit").command
    add_command(
        "EOF", getattr(exit_module, "do_command"), exit_module.__doc__, CustomCommand
    )

    main_shell = CustomCommand()

    main_shell.cmdloop()
