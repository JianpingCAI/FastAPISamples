import asyncio
import concurrent.futures
from functools import partial

class DataService:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor()

    async def fetch_data(self, input_data):
        loop = asyncio.get_running_loop()
        # Run the blocking function in the pre-created separate thread
        # Create a partial function with the input argument
        partial_func = partial(self.process_data, input_data)
        return await loop.run_in_executor(self.executor, partial_func)

    def process_data(self, input_data):
        # Simulate some processing logic
        return {"data": f"Here is your data: {input_data}!"}

    def __del__(self):
        self.executor.shutdown(wait=True)




# import asyncio
# import concurrent.futures


# class DataService:
#     async def fetch_data(self):
#         loop = asyncio.get_running_loop()
#         # Run blocking function in a separate thread
#         with concurrent.futures.ThreadPoolExecutor() as pool:
#             return await loop.run_in_executor(pool, self.process_data())

#     def process_data(self):
#         # Simulate some processing logic
#         return {"data": "Here is your data!"}
