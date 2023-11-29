from fastapi import APIRouter, Depends

from JWT import JWT

router = APIRouter(
    prefix="/users",
    tags=["utils"],
)

