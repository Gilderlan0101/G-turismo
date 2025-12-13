from fastapi import APIRouter, HTTPException, status, Depends

from src.auth.schemas import SystemUser
from src.service.jwt.depends import get_current_user

router = APIRouter(tags=['services'])


@router.get('/get_service')
async def service(current_user: SystemUser = Depends(get_current_user)):
    """service exibir todos os serviçoes de turismo publicados"""
    pass
