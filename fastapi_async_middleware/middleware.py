from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Request: {request.url.path} took {process_time:.4f} seconds")
        return response
