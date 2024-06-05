from command_handlers.command_parameters import CommandParameters
from command_handlers.console_output_handler import ConsoleOutputHandler
from command_handlers.file_output_handler import FileOutputHandler

from command_handlers.command_executor import execute_command

if __name__ == "__main__":
    executable = input("Enter the command you want to execute: ")
    args = input("Enter arguments separated by space: ").split()
    options = {}  # Customize as needed
    real_time = input("Real-time output? (yes/no): ").lower() == "yes"
    interactive = input("Is this command interactive? (yes/no): ").lower() == "yes"

    command_params = CommandParameters(
        executable=executable,
        args=args,
        options=options,
        real_time=real_time,
        interactive=interactive,
    )
    output_handler = ConsoleOutputHandler()
    # or FileOutputHandler() depending on the requirement

    execute_command(command_params, output_handler)
