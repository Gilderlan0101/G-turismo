from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Optional


class LoginResponse(BaseModel):
    """Resposta ao concluir login"""

    username: str                       # email
    access_token: str                   # Token gerado
    refresh_token: str                  # Token regeneração
    photo_profile: str                  # Foto de perfil


class CrateUser(BaseModel):
    """Schemas para cria uma conta"""
    username: str
    email: EmailStr
    password: str = Field(min_length=4, max_length=90)
    status: bool = True


class SystemUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    photo: Optional[str] = None
    status: bool = True

    model_config = {'from_attributes': True}


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
