from fastapi import APIRouter, Depends

from src.JWT import JWT

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(".getOwnedChats", dependencies=[Depends(JWT)])
async def get_owned_chats():
    return {}
