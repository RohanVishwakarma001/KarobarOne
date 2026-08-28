from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from uuid import UUID

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "customer"
    storeId: Optional[Union[UUID, str, int]] = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    userId: Union[UUID, int, str]
    role: str
    storeId: Optional[Union[UUID, str, int]] = None