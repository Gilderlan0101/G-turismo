from pydantic import BaseModel, EmailStr


class CrateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    status: bool = True
