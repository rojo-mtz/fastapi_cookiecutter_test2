from typing import Optional

from pydantic import BaseModel


class GenerateUrlSchema(BaseModel):
    status: str
    message: str
    secret_id: str
    url: str
    expires_in_seconds: Optional[int] = None
