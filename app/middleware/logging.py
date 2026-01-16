import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response


logger = logging.getLogger("app.middleware")


async def logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start_time = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        logger.exception("Unhandled error during request")
        raise
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        query = f"?{request.url.query}" if request.url.query else ""
        logger.info(
            "request %s %s%s %s %.2fms",
            request.method,
            request.url.path,
            query,
            status_code,
            duration_ms,
        )
