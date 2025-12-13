from fastapi import APIRouter, HTTPException, status, Depends

from src.auth.schemas import SystemUser
from src.service.jwt.depends import get_current_user

router = APIRouter(tags=['Profile'])


@router.get('/user/{username}')
async def profile(
    username: str,
    current_user: SystemUser = Depends(get_current_user)
    ):
    """rota para exibir informaçoes da conta do usuario"""
    pass
