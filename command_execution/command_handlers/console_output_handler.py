from .output_handler_interface import OutputHandlerInterface


class ConsoleOutputHandler(OutputHandlerInterface):
    def handle_output(self, message: str) -> None:
        print("Output:", message)

    def handle_error(self, message: str) -> None:
        print("Error:", message)
