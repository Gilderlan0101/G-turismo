from datetime import datetime
from typing import Optional

import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from src.schemas.auth.schemas_auth import TokenPayload
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl='auth/login',
    scheme_name='JWT Bearer',
)

JWT_ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class DecodeToken:
    def __init__(self, token: str = Depends(OAUTH2_SCHEME)):

        self.data: Optional[TokenPayload] = None

        try:
            payload = jwt.decode(
                token, str(JWT_SECRET_KEY), algorithms=[str(JWT_ALGORITHM)]
            )
            token_data = TokenPayload(**payload)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido ou com formato incorreto.',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        if (
            token_data.exp
            and datetime.fromtimestamp(token_data.exp) < datetime.now()
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expirado. Faça login novamente',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        self.data = token_data

    def get_user_id(self) -> int:
        if self.data is None:
            raise RuntimeError('Dados do token não disponíveis.')
        return int(self.data.sub)
