import os

from pydantic import BaseModel


class Settings(BaseModel):
    API_URL: str


settings = Settings(API_URL=os.environ.get("API_URL"))
