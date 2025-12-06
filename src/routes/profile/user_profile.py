from fastapi import APIRouter, HTTPException, status
from src.schemas.auth.schemas_auth import SystemUser
from src.service.jwt.depends import get_current_user


router = APIRouter(tags['Profile'])


@router.get('/user/profile')
async def profile(current_user: SystemUser = Depends(get_current_user)):
    """rota para exibir informaçoes da conta do usuario"""
    pass
