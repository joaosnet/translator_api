from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserMessage(BaseModel):
    role: str
    content: str


class TranslateSchema(BaseModel):
    idioma: str
    comentario: str


class TranslatefordbSchema(BaseModel):
    comentario: str
