from http import HTTPStatus

import ollama
from fastapi import FastAPI

from translator.schemas import Message, TranslateSchema

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK.value)
def read_root() -> dict:
    return {'message': 'Olá Mundo'}


@app.post('/translator/', response_model=Message, status_code=HTTPStatus.OK.value)  # noqa: E501
def llm3(conteudo: TranslateSchema) -> Message:
    idioma = conteudo.idioma
    comentario = conteudo.comentario

    prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
    Seu trabalho é fazer a tradução do idioma "{idioma}".
    Não quero outra coisa, apenas a tradução (e se necessário a correção do tex
    to). Para a próxima tarefa, faça a tradução (e se necessário a correção do
    texto) do seguinte texto: "{comentario}"
    quero um message simples, direta e clara, sem erros de tradução ou gramati
    cais, OU SEJA APENAS RESPONDA COM A TRADUÇÃO DO TEXTO
    Exemplo de Idioma: en
    Exemplo de Texto enviado: Olá Mundo
    Exemplo de SUA RESPOSTA: Hello World"""

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
    )

    return Message(message=response['message']['content'])
