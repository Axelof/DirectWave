from fastapi import APIRouter, Depends

from JWT import JWT

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.get(".ping")
async def ping():
    return {"result": "ok"}


@router.get(".checkAuth", dependencies=[Depends(JWT)])
async def check_auth():
    return {"result": "ok"}
