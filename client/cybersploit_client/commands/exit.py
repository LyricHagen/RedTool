from ..commands import Command

class ExitCommand(Command): 
    """
    Exit the CLI.
    """

    def do_command(self, lines: str):
        print(f"Found input: {lines}")
        print("Exiting CLI")
        return True 

command = ExitCommand # Assign the class you created to the variable called command for the system to find the command!
