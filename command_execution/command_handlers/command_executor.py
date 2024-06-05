import subprocess
import sys
import logging

# import configparser

from .command_parameters import CommandParameters
from .output_handler_interface import OutputHandlerInterface


# config = configparser.ConfigParser()
# config.read("config.ini")
# critical_keywords = config["ErrorHandler"]["CriticalKeywords"].split(",")


# # Set up basic configuration for logging
# logging.basicConfig(
#     filename="command_execution.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )


def execute_command(
    params: CommandParameters, output_handler: OutputHandlerInterface
) -> None:
    """
    Executes a given command encapsulated within CommandParameters.
    """
    command = params.get_command_list()
    try:
        if params.interactive:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            handle_interactive_process(process, output_handler)
        elif params.real_time:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            handle_real_time_process(process, output_handler)
        else:
            result = subprocess.run(command, capture_output=True, text=True)
            handle_standard_process(result, output_handler)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        logging.error(f"An error occurred: {str(e)}")


def handle_interactive_process(
    process: subprocess.Popen, output_handler: OutputHandlerInterface
) -> None:
    """
    Handles interactive process communication.
    """
    try:
        while True:
            # handle stdout
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                # print(output.strip())
                # logging.info(output.strip())
                output_handler.handle_output(output.strip())

            # handle stderr
            error = process.stderr.readline()
            if error:
                # print("Error:", error.strip(), file=sys.stderr)
                # logging.error(error.strip())
                output_handler.handle_error(error.strip())

            if "Please enter" in output:  # Example condition for interaction
                user_input = input() + "\n"
                process.stdin.write(user_input)
                process.stdin.flush()
        process.wait()
    finally:
        if process.poll() is None:  # Ensure the process is terminated
            process.kill()
            process.wait()


def handle_real_time_process(
    process: subprocess.Popen, output_handler: OutputHandlerInterface
) -> None:
    """
    Handles real-time output of a process.
    """
    try:
        for line in process.stdout:
            # print(line, end="")
            # logging.info(line.strip())
            output_handler.handle_output(line.strip())
        process.wait()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()


def handle_standard_process(
    result: subprocess.CompletedProcess, output_handler: OutputHandlerInterface
) -> None:
    """
    Handles standard process execution with captured output.
    """
    if result.stdout:
        # print(result.stdout)
        # logging.info(result.stdout)
        output_handler.handle_output(result.stdout)
    if result.stderr:
        # print("Error:\n", result.stderr, file=sys.stderr)
        # logging.error(result.stderr)
        output_handler.handle_error(result.stderr)
