# main.py
from registration import register_with_server
from websocket_client import start_websocket_client
import asyncio


def main():
    runner_id = register_with_server()
    asyncio.run(start_websocket_client(runner_id))


if __name__ == "__main__":
    main()
