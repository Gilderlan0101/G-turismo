from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.auth.schemas_login import LoginResponse
from src.schemas.auth.schemas_register import CrateUser
from src.service.auth_user.auth_register import create_account

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


@router.post('/confirm_account')
async def comfim_activate_account(
    ):
pass
