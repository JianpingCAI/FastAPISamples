import re
import sys
import argparse
from typing import List, Tuple, Dict


class LogEntry:
    def __init__(
        self,
        thread_id: str,
        request_number: int,
        request_content: str,
        duration: float,
    ):
        self.thread_id = thread_id
        self.request_number = request_number
        self.request_content = request_content
        self.duration = duration

    def __repr__(self) -> str:
        return (
            f"thread_id={self.thread_id}, request_number={self.request_number}, "
            f"\nrequest_content=\n'{self.request_content}', "
            f"\nduration={self.duration:.2f}s"
        )


def analyze_log_file(file_path: str) -> List[LogEntry]:
    # Regular expression patterns to match the required lines
    thread_requestId_content_pattern = re.compile(
        r"-------\[(.*?)\] Request \[(\d+)\] ------\n(.*?)\n---------------------------",
        re.DOTALL,
    )
    thread_duration_pattern = re.compile(
        r"\[(.*?)\]The Request \[(\d+)\] is done in ([\d.]+)s"
    )

    # List to store the LogEntry objects
    results: List[LogEntry] = []

    try:
        with open(file_path, "r") as file:
            log_content: str = file.read()

        # Extract all request details
        thread_requestId_content_list: List[Tuple[str, str, str]] = (
            thread_requestId_content_pattern.findall(log_content)
        )
        thread_requestId_content_dict: Dict[Tuple[str, int], str] = {
            (thread, int(num)): content
            for (thread, num, content) in thread_requestId_content_list
        }

        # Extract all thread durations
        thread_duration_list: List[Tuple[str, str, str]] = (
            thread_duration_pattern.findall(log_content)
        )
        thread_duration_dict: Dict[Tuple[str, int], float] = {
            (thread, int(num)): float(duration)
            for (thread, num, duration) in thread_duration_list
        }

        # Process each request and find the corresponding content and duration
        for (
            thread_id,
            request_id,
        ), request_content in thread_requestId_content_dict.items():

            # Find processing duration
            duration: float = thread_duration_dict.get((thread_id, request_id), 0.0)

            # Create LogEntry and add to results, limit request_content to 1000 characters
            results.append(
                LogEntry(
                    thread_id,
                    request_id,
                    request_content.strip(),  # Limit the content length
                    duration,
                )
            )

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {file_path}.")
    except ValueError as ve:
        print(f"Error: A value error occurred: {ve}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

    return results


def print_formatted_results(results: List[LogEntry]) -> None:
    for entry in results:
        print(f"{entry}\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze log file and extract request details."
    )
    parser.add_argument(
        "--log_file", type=str, required=True, help="Path to the log file"
    )

    args = parser.parse_args()

    log_file_path: str = args.log_file
    entries: List[LogEntry] = analyze_log_file(log_file_path)

    # Sort entries by duration in descending order and get the top ten
    sorted_entries: List[LogEntry] = sorted(
        entries, key=lambda x: x.duration, reverse=True
    )[:10]

    print_formatted_results(sorted_entries)
