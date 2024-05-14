from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str | None
    user_name: str
    email: str
