from fastapi import APIRouter, HTTPException, status
from src.schemas.auth.schemas_auth import SystemUser
from src.service.jwt.depends import get_current_user


router = APIRouter(tags=['services'])


@router.get('/api/v1/all_services')
async def service(current_user: SystemUser = Depends(get_current_user)):
    """service exibir todos os serviçoes de turismo publicados"""
    pass
