import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from utils.exceptions import *


class ExceptionMiddleware(BaseHTTPMiddleware):
    """Middleware to catch exceptions and return a JSON response"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except DuplicateRecordException as exc:
            return JSONResponse(status_code=400, content={"detail": exc.message})
        except Exception as exc:
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={"message": f"An unexpected error occurred:\n{str(exc)}"},
            )
