from fastapi import Depends, HTTPException, status

from config import OAUTH2_SCHEME
from src.models.user import User
from src.auth.schemas import SystemUser
from src.service.jwt.jwt_decode_token import DecodeToken


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME),
) -> SystemUser:

    token_data = DecodeToken(str(token))
    user_id = int(token_data.data.sub)

    search_target_user = await User.get_or_none(id=user_id)

    if search_target_user:
        system_user_data = SystemUser(
            id=search_target_user.id,
            username=search_target_user.username,
            email=search_target_user.email,
            photo=search_target_user.photo,
            status=search_target_user.status,
        )

        return system_user_data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Usuário não encontrado após validação do token.',
    )
