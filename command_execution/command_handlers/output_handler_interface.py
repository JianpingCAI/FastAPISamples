from abc import ABC, abstractmethod


class OutputHandlerInterface(ABC):
    @abstractmethod
    def handle_output(self, message: str) -> None:
        """
        Handle standard output messages from the subprocess.
        """
        pass

    @abstractmethod
    def handle_error(self, message: str) -> None:
        """
        Handle error messages from the subprocess.
        """
        pass
