from typing import Any, Dict

from fastapi import HTTPException, status
from src.auth.exceptions import EMAIL_ALREADY_EXISTS,  ERROR_MISSING_FIELDS
from src.models.user import User
from src.service.jwt.auth import get_hashed_password, verify_password
from src.global_utils.hashed_email import (create_email_search_hash, get_hashed_email,
                                    verify_email)


async def create_account(target) -> Dict[str, Any]:
    """create_account: Responsavel por cria cota para um usuario"""
    try:

        if not target:
            raise ERROR_MISSING_FIELDS


        user = await User.filter(
            email_search_hash=create_email_search_hash(target.get('email'))
        ).exists()
        if user:
            raise EMAIL_ALREADY_EXISTS

        # Caso esse email não esteja no banco de dados vamos cria uma conta para esse usuario
        # Ao cria a conta o usuario tem tera que ativa sua conta com o codigo que foi enviado
        # por email. Para verifica a conta acesser a rota (verified_account)
        if isinstance(target, dict):

            create = await User.create(
                username=target.get('username'),
                email=target.get('email'),
                password=get_hashed_password(target.get('password')),
                status=target.get('status'),
                email_search_hash=create_email_search_hash(
                    target.get('email')
                ),
                verified_account=False,  # Atualize para True quando o usuario verifica a conta
            )

            return {
                'username': target.get('username'),
                'email': target.get('email'),
                'status': True,
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error  {}'.format(str(e)),
        )
