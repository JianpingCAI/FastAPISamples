import re
import sys
import argparse
from typing import List, Tuple


class LogEntry:
    def __init__(
        self,
        thread_id: str,
        request_number: int,
        request_content_xml: str,
        request_content: str,
        duration: float,
    ):
        self.thread_id = thread_id
        self.request_number = request_number
        self.request_content_xml = request_content_xml
        self.request_content = request_content
        self.duration = duration

    def __repr__(self) -> str:
        return (
            f"LogEntry(thread_id={self.thread_id}, request_number={self.request_number}, "
            f"request_content_xml='{self.request_content_xml}', request_content='{self.request_content}', "
            f"duration={self.duration:.2f}s)"
        )


def analyze_log_file(file_path: str) -> List[LogEntry]:
    # Regular expression patterns to match the required lines
    xml_request_pattern = re.compile(
        r"test \[(thread\d+)\] get a request:\n<xml>(.*?)</xml>", re.DOTALL
    )
    thread_request_pattern = re.compile(
        r"-------\[(thread\d+)\] Request \[(\d+)\] ------\n(.*?)\n---------------------------",
        re.DOTALL,
    )
    duration_pattern = re.compile(
        r"\[(thread\d+)\]The Request \[(\d+)\] is done in ([\d.]+)s"
    )

    # List to store the LogEntry objects
    results: List[LogEntry] = []

    try:
        with open(file_path, "r") as file:
            log_content: str = file.read()

        # Extract all XML requests
        xml_requests: List[Tuple[str, str]] = xml_request_pattern.findall(log_content)
        xml_dict: dict[Tuple[str, int], str] = {
            (thread, i + 1): content.strip()
            for i, (thread, content) in enumerate(xml_requests)
        }

        # Extract all non-XML request details
        thread_requests: List[Tuple[str, str, str]] = thread_request_pattern.findall(
            log_content
        )
        duration_matches: List[Tuple[str, str, str]] = duration_pattern.findall(
            log_content
        )

        # Process each request and find the corresponding content and duration
        for thread_id, request_number_str, request_content in thread_requests:
            request_number: int = int(request_number_str)

            # Get XML content
            request_content_xml: str = xml_dict.get((thread_id, request_number), "")

            # Find processing duration
            duration: float = 0.0
            for t_id, num, dur in duration_matches:
                if int(num) == request_number and t_id == thread_id:
                    duration = float(dur)
                    break

            # Create LogEntry and add to results
            results.append(
                LogEntry(
                    thread_id,
                    request_number,
                    request_content_xml,
                    request_content.strip(),
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
        print(
            f"Thread ID: {entry.thread_id}, Request Number: {entry.request_number}, "
            f"Request Content XML: '{entry.request_content_xml}', "
            f"Request Content: '{entry.request_content}', Duration: {entry.duration:.2f}s"
        )


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

    print_formatted_results(entries)
