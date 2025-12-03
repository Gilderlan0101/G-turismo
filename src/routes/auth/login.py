from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth.schemas_auth import SystemUser
from src.schemas.auth.schemas_login import LoginResponse
from src.service.auth_user.auth_login import checking_account
from src.service.jwt.depends import get_current_user

router = APIRouter(tags=['Authentication'])


@router.post(
    '/login', response_model=LoginResponse, status_code=status.HTTP_200_OK
)
async def login(target: OAuth2PasswordRequestForm = Depends()):
    """Rota responsavel por autentica um usuario se o mesmo tive uma conta"""

    verify_auth = await checking_account(target=target)
    if not verify_auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Conta não econtrada. Crie uma conta em menos de 1 minuto.',
        )

    return verify_auth




