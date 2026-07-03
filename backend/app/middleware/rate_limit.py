from collections import defaultdict
from time import time
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time()
        self.hits[client] = [hit for hit in self.hits[client] if now - hit < self.window_seconds]
        if len(self.hits[client]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")
        self.hits[client].append(now)
        return await call_next(request)
