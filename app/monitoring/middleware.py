from __future__ import annotations

import time

from fastapi import Request

from app.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY


async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        path = request.url.path
        method = request.method
        elapsed = time.perf_counter() - start
        REQUEST_COUNT.labels(method=method, path=path, status=str(status_code)).inc()
        REQUEST_LATENCY.labels(method=method, path=path).observe(elapsed)
