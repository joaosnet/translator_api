# import ollama
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root() -> dict:
    return {'message': 'Olá Mundo'}


# @app.post('/llm3/{conteudo}')
# def llm3(conteudo: dict) -> str:
#     # Extract the values from the JSON
#     idioma = conteudo.get('idioma', '')
#     comentario = conteudo.get('comentario', '')

#     prompt = f"""Atue como tradutor + corretor com 20 anos de experiência.
#     Seu trabalho é fazer a tradução do idioma {idioma}.
#   Não quero outra coisa, apenas a tradução (e se necessário a correção do tex
#    to). Para a próxima tarefa, faça a tradução (e se necessário a correção do
#     texto) do seguinte texto: {comentario}"""

#     response = ollama.chat(
#         model='llama3',
#         messages=[
#             {
#                 'role': 'user',
#                 'content': prompt,
#             }
#         ],
#     )

#     return response['message']['content']
