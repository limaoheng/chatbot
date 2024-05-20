from typing import Optional

from pydantic import BaseModel
from pydantic_core import Url


class Message(BaseModel):
    text: str
    url: Optional[Url]
