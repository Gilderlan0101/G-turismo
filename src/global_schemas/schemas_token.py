from pydantic import BaseModel, EmailStr
from typing import Optional

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
