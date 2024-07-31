from starlette.responses import JSONResponse

from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException


async def not_found_exception_handler(request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def deletion_failed_exception_handler(request, exc: DeletionFailedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


