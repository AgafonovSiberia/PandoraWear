from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health", include_in_schema=False)
async def health() -> Response:
    return Response(status_code=204)


@router.get("/ready", include_in_schema=False)
async def ready() -> Response:
    return Response(status_code=204)
