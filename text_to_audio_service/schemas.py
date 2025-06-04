from pydantic import BaseModel


class TextSpeech(BaseModel):

    text_: str
