from typing import Dict, List, Optional


class CommandParameters:
    def __init__(
        self,
        executable: str,
        args: Optional[List[str]] = None,
        options: Optional[Dict[str, Optional[str]]] = None,
        real_time: bool = False,
        interactive: bool = False,
    ):
        """
        Initializes the command parameters.

        :param executable: The main command or executable to run.
        :param args: List of arguments for the command.
        :param options: Dictionary of options or flags for the command.
        :param real_time: Boolean indicating if the output should be in real-time.
        :param interactive: Boolean indicating if the command requires interactive input.
        """
        self.executable = executable
        self.args = args if args else []
        self.options = options if options else {}
        self.real_time = real_time
        self.interactive = interactive

    def get_command_list(self) -> List[str]:
        """
        Constructs the command list from the instance attributes.
        """
        command_list = [self.executable]
        for option, value in self.options.items():
            command_list.append(option)
            if value:
                command_list.append(value)
        command_list.extend(self.args)
        return command_list