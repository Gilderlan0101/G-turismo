from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.create_account import create_account
from src.auth.exceptions import ERROR_SEND_EMAIL
from src.auth.schemas import CrateUser, LoginResponse
from src.auth.utils import checking_account as validate_account
from src.auth.schemas import SystemUser
from src.service.jwt.depends import get_current_user
from src.service.send_email.send_verification_code import (
    activating_the_account_with_a_code, send_code_email)

router = APIRouter(tags=['Authentication'])


@router.post(
    '/login', response_model=LoginResponse, status_code=status.HTTP_200_OK
)
async def login(target: OAuth2PasswordRequestForm = Depends()):
    """Rota responsável por autenticar um usuário se o mesmo tiver uma conta."""

    verify_auth = await validate_account(target={'email': target.username, 'password': target.password})

    if verify_auth is None:
        raise HTTPException(
            status_code=status.HTTP_402_UNAUTHORIZED,
            detail='Credenciais inválidas. Verifique seu e-mail e senha.',
        )

    return verify_auth


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(target: CrateUser):
    """Responsavel por cadastra uma conta de um usuario"""

    create = await create_account(target=dict(target))
    if create:
        return {'message': 'account created successfully'}
    else:
        return create


@router.post(
    '/send_code_for_email',
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary='Envia código de verificação por email',
    description="""
    Envia um código de verificação para o email do usuário autenticado.

    O código será utilizado para verificar a conta do usuário.
    """,
)
async def send_code_for_email(
    current_user: SystemUser = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Envia código de verificação para o email do usuário.

    Args:
        current_user: Usuário autenticado obtido através do token JWT.

    Returns:
        Dict com mensagem de sucesso ou erro.

    Raises:
        HTTPException: Se ocorrer um erro durante o processo.
    """
    send_success = await send_code_email(target_email=current_user.email)

    if send_success:
        return {'message': 'Código de verificação enviado com sucesso. Verifique seu email.'}
    else:
            return ERRO_SEND_EMAIL


@router.post('/comfim_account')
async def comfim_account_with_code(
    code: str = Body(...),
    current_user: SystemUser = Depends(get_current_user),
):

    activate_account = await activating_the_account_with_a_code(
        target_account=current_user.email, code=code
    )

    if activate_account:
        return {'mensagem': 'Conta ativada com sucesso'}

    else:
        return activate_account
