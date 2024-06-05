from .output_handler_interface import OutputHandlerInterface


class FileOutputHandler(OutputHandlerInterface):
    def handle_output(self, message: str) -> None:
        with open("output_log.txt", "a") as file:
            file.write(message + "\n")

    def handle_error(self, message: str) -> None:
        with open("error_log.txt", "a") as file:
            file.write("Error: " + message + "\n")
