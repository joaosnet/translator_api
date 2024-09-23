# from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


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


class ConfigDict:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Comentario(BaseModel):
    comentario_id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    comentario: str
    idioma_requisitado: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            'example': {
                'comentario': 'ola',
                'idioma_requisitado': 'en',
            }
        }


class ComentarioCollection(BaseModel):
    comentarios: List[Comentario]


def mongo_to_comentario(doc: dict) -> Comentario:
    return Comentario(
        comentario_id=str(doc['_id']),
        usuario=doc['usuario'],
        data=doc['data'],
        comentario=doc['comentario'],
        idioma_requisitado=doc['idioma_requisitado'],
    )
