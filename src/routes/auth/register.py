from fastapi import APIRouter, Depends, HTTPException, status, Body

from src.schemas.auth.schemas_login import LoginResponse
from src.schemas.auth.schemas_register import CrateUser
from src.service.auth_user.auth_register import create_account
from src.service.send_email.send_verification_code import send_code_email
from src.service.jwt.depends import get_current_user
from src.schemas.auth.schemas_auth import SystemUser


router = APIRouter(tags=['Authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(target: CrateUser):
    """Responsavel por cadastra uma conta de um usuario"""
    print(target)
    data = {
        'username': target.username,
        'email': target.email,
        'password': target.password,
        'status': target.status,
    }
    create = await create_account(target=data)
    if create:
        return {'message': 'account created successfully'}

    else:
        return create


@router.post('/send_code_for_email')
async def seend_code_for_email(
current_user: SystemUser = Depends(get_current_user)
):

    send = await send_code_email(target_email=current_user.email)
    if send:
        return {'message': 'Verifique seu email'}
    else:
        return {'message': 'Erro ao tenta verifica email. Tente novamente.'}


@router.post('/comfim_account')
async def comfim_account_with_code():
    pass
