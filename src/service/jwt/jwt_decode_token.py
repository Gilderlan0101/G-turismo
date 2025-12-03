from datetime import datetime
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status

from confing import JWT_ALGORITHM, JWT_SECRET_KEY, OAUTH2_SCHEME


class DecodeToken:
    def __init__(self, token: str = Depends(OAUTH2_SCHEME)):

        self.data: Optional[TokenPayload] = None

        try:
            payload = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except jwt.PyJWTError:
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
        return self.data.sub
