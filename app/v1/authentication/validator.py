from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr


class Sign(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(10)]

class SignUp(Sign):
    pass

class SignIn(Sign):
    pass