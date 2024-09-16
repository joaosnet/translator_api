from datetime import datetime
from typing import Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field


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


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ConfigDict:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Comentario(BaseModel):
    comentario_id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    usuario: str
    data: datetime = Field(default_factory=datetime.utcnow)
    comentarios: Dict[str, str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'comentario_id': '507f1f77bcf86cd799439011',
                'usuario': 'nome_usuario',
                'data': '2023-10-01T00:00:00Z',
                'comentarios': {
                    'pt': 'Comentário em português',
                    'en': 'Comment in English',
                    'de': 'Kommentar auf Deutsch',
                },
            }
        }


class ComentarioCollection(BaseModel):
    comentarios: List[Comentario]
