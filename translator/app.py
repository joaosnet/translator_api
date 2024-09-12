from http import HTTPStatus
from pprint import pprint as pp

import google.generativeai as genai
from fastapi import FastAPI
from ollama import AsyncClient

from translator.schemas import Message, TranslatefordbSchema, TranslateSchema

app = FastAPI()

genai.configure(api_key='AIzaSyCkBIo7h-UrTNlo7V3qzEAeu4o0JcAqKuA')


@app.get('/', response_model=Message, status_code=HTTPStatus.OK.value)
def read_root() -> dict:
    return {'message': 'Olá Mundo'}


@app.post(
    '/translator/', response_model=Message, status_code=HTTPStatus.OK.value
)  # noqa: E501
async def llm3(conteudo: TranslateSchema) -> Message:
    idioma = conteudo.idioma
    comentario = conteudo.comentario
    # switch case para definir o idioma
    match idioma:
        case 'en_US':
            idioma = 'inglês'
        case 'de':
            idioma = 'Alemão'
        case 'pt':
            idioma = 'Português do Brasil'
        case _:
            idioma = 'idioma desconhecido'
    prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
    Seu trabalho é fazer a tradução para o idioma + correção  "{idioma}", caso
    já esteja no idioma selecionado faça a correção do texto.
    Não quero outra coisa, apenas a tradução (e se necessário a correção do tex
    to). Para a próxima tarefa, faça a tradução (e se necessário a correção do
    texto) do seguinte texto: "{comentario}"
    quero um message simples, direta e clara, sem erros de tradução ou gramati
    cais, OU SEJA APENAS RESPONDA COM A TRADUÇÃO DO TEXTO
    Exemplo de Idioma: en
    Exemplo de Texto enviado: Olá Mundo
    Exemplo de SUA RESPOSTA: Hello World"""

    response = await AsyncClient().chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
    )

    return Message(message=response['message']['content'])


# criando uma rota para para usar a api do gemini para traduzir os comentarios
# do usuario para os tres idiomas e quardar em um banco de dados
@app.post(
    '/translator/gemini/',
    response_model=Message,
    status_code=HTTPStatus.OK.value,
)  # noqa: E501
def gemini(conteudo: TranslatefordbSchema):
    model = genai.GenerativeModel('gemini-1.5-flash')

    comentario = conteudo.comentario
    # switch case para definir o idioma
    idiomas = ['inglês', 'Alemão', 'Português do Brasil']

    for i, idioma in enumerate(idiomas):
        prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
        Seu trabalho é fazer a tradução para o idioma + correção  "{idioma}",
        caso já esteja no idioma selecionado faça a correção do texto.
        Não quero outra coisa, apenas a tradução (e se necessário a correção do
        texto). Para a próxima tarefa, faça a tradução (e se necessário a
        correção do texto) do seguinte texto: "{comentario}" quero um message
        simples, direta e clara, sem erros de tradução ou gramati
        cais, OU SEJA APENAS RESPONDA COM A TRADUÇÃO DO TEXTO
        Exemplo de Idioma: en
        Exemplo de Texto enviado: Olá Mundo
        Exemplo de SUA RESPOSTA: Hello World"""

        response = model.generate_content(prompt)
        response = response.text
        pp(response)

        # salvar no banco de dados

    return Message(message=response)
