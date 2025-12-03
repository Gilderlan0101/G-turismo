from typing import Any, Dict

from fastapi import HTTPException, status

from src.models.user import User
from src.schemas.auth.schemas_login import LoginResponse
from src.service.jwt.auth import (create_access_token, create_refresh_token,
                                  verify_password)


async def checking_account(target) -> Dict[str, Any]:
    # Verifica se o usuário target tem conta no site e realiza o login

    # 1. Busca o usuário no banco de dados pelo username
    user = User.filter(username=target.username).first()

    # 2. Se o usuário não for encontrado, levanta exceção de não autorizado
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas',
        )

    # 3. Verifica a senha fornecida (target.password) contra a senha hasheada do usuário encontrado (user.password)
    if not verify_password(target.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas',
        )

    # 4. Se a verificação for bem-sucedida, gera os tokens
    user_id_str = str(user.id)
    access_token = create_access_token(user_id_str)
    refresh_token = create_refresh_token(user_id_str)

    # 5. Retorna a resposta de login
    return LoginResponse(
        id=user.id,
        email=getattr(user, 'email', ''),
        access_token=access_token,
        refresh_token=refresh_token,
    )
