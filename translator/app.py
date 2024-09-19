import google.generativeai as genai
import motor.motor_asyncio
from fastapi import Body, FastAPI, status

from translator.schemas import (
    Comentario,
    ComentarioCollection,
    Message,
)

app = FastAPI()

genai.configure(api_key='AIzaSyCkBIo7h-UrTNlo7V3qzEAeu4o0JcAqKuA')

URL = 'mongodb://admin:123@127.0.0.1:27017/comentarios_projeto?retryWrites=true&w=majority'
client = motor.motor_asyncio.AsyncIOMotorClient(URL)
db = client.get_database('comentarios_projeto')
coments_collection = db.get_collection('comentarios')


@app.post(
    '/translator/gemini/',
    response_description='Add new translated comment',
    response_model=Message,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def gemini(conteudo: Comentario = Body(...)):
    """
    Translate the user's comment into three languages
    and store it in the database.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    comentario = conteudo.comentario
    idiomas = ['inglês', 'Alemão', 'Português do Brasil']
    traducoes = {}

    for idioma in idiomas:
        prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
        Seu trabalho é fazer a tradução para o idioma + correção  "{idioma}",
        caso já esteja no idioma selecionado faça a correção do texto.
        Não quero outra coisa, apenas a tradução (e se necessário a correção do
        texto). Para a próxima tarefa, faça a tradução (e se necessário a
        correção do texto) do seguinte texto: "{comentario}" quero um message
        simples, direta e clara, sem erros de tradução ou gramaticais, OU SEJA APENAS RESPONDA COM A TRADUÇÃO DO TEXTO
        Exemplo de Idioma: en
        Exemplo de Texto enviado: Olá Mundo
        Exemplo de SUA RESPOSTA: Hello World"""  # noqa: E501

        response = model.generate_content(prompt)
        traducoes[idioma] = response.text

    # Criar o documento para inserir no MongoDB
    comentario_documento = {
        'usuario': conteudo.usuario,
        'data': conteudo.data,
        'comentarios': traducoes,
    }

    # Inserir o documento no MongoDB
    new_comment = await coments_collection.insert_one(comentario_documento)
    await coments_collection.find_one({
        '_id': new_comment.inserted_id
    })

    match conteudo.idioma_requisitado:
        case 'en_US':
            idioma = 'inglês'
            comentario_traduzido = traducoes[idioma]
        case 'de':
            idioma = 'Alemão'
            comentario_traduzido = traducoes[idioma]
        case 'pt':
            idioma = 'Português do Brasil'
            comentario_traduzido = traducoes[idioma]
        case _:
            idioma = 'inglês'
            comentario_traduzido = traducoes[idioma]

    return Message(message=comentario_traduzido)


@app.get(
    '/translator/comments/',
    response_description='List all comments',
    response_model=ComentarioCollection,
    response_model_by_alias=False,
)
async def list_comments():
    """
    List all of the comments in the database.

    The response is unpaginated and limited to 1000 results.
    """
    comentarios = await coments_collection.find().to_list(1000)
    return ComentarioCollection(comentarios=comentarios)

# @app.get('/', response_model=Message, status_code=HTTPStatus.OK.value)
# def read_root() -> dict:
#     return {'message': 'Olá Mundo'}


# @app.post(
#     '/translator/', response_model=Message, status_code=HTTPStatus.OK.value
# )  # noqa: E501
# async def llm3(conteudo: TranslateSchema) -> Message:
#     idioma = conteudo.idioma
#     comentario = conteudo.comentario
#     # switch case para definir o idioma
#     match idioma:
#         case 'en_US':
#             idioma = 'inglês'
#         case 'de':
#             idioma = 'Alemão'
#         case 'pt':
#             idioma = 'Português do Brasil'
#         case _:
#             idioma = 'idioma desconhecido'
#     prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
#    Seu trabalho é fazer a tradução para o idioma + correção  "{idioma}", caso
#     já esteja no idioma selecionado faça a correção do texto.
#   Não quero outra coisa, apenas a tradução (e se necessário a correção do tex
#    to). Para a próxima tarefa, faça a tradução (e se necessário a correção do
#     texto) do seguinte texto: "{comentario}"
#    quero um message simples, direta e clara, sem erros de tradução ou gramati
#     cais, OU SEJA APENAS RESPONDA COM A TRADUÇÃO DO TEXTO
#     Exemplo de Idioma: en
#     Exemplo de Texto enviado: Olá Mundo
#     Exemplo de SUA RESPOSTA: Hello World"""

#     response = await AsyncClient().chat(
#         model='llama3',
#         messages=[
#             {
#                 'role': 'user',
#                 'content': prompt,
#             }
#         ],
#     )

#     return Message(message=response['message']['content'])
