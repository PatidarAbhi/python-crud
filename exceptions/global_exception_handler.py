from starlette.responses import JSONResponse

from exceptions.not_found_exception import NotFoundException


async def not_found_exception_handler(request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


