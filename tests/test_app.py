from http import HTTPStatus


# teste da rota de tradução
def test_translate(client):
    response = client.post(
        '/translator/',
        json={
            'comentario': 'Olá Mundo',
            'idioma_requisitado': 'en_US',
        },
    )  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)

    assert response.json() == {'message': 'Hello World'}  # Assert(verificação)


# def test_read_root_deve_retornar_ok_e_ola_mundo(client):
#     response = client.get('/')  # Act (ação)

#     assert response.status_code == HTTPStatus.OK  # Assert (verificação)

#    assert response.json() == {'message': 'Olá Mundo'}  # Assert (verificação)

# testando se está funcionando o llm3
# def test_llm3_deve_retornar_ok_e_mensagem_com_texto_traduzido(client):
#     response = client.post(
#         '/translator/gemini/',
#         json={
#             'message': 'Olá Mundo',
#         },
#     )  # Act (ação)

#     assert response.status_code == HTTPStatus.OK  # Assert (verificação)

#   assert response.json() == {'message': 'Hello World'}  # Assert(verificação)


# testando com algo mais complexo
# def test_llm3_deve_retornar_ok_e_mensagem_com_texto_traduzido2(client):
#     response = client.post(
#         '/translator/gemini/',
#         json={
#             'message': 'その日は嵐だった。叩きつけるような雨が草原を洗い、太い雷が何本も大地へと落ちた。雷光に照らされて、一軒の家が浮かび上がる.',  # noqa: E501
#         },
#     )  # Act (ação)

#     assert response.status_code == HTTPStatus.OK  # Assert (verificação)

#     assert response.json() == {
#         'message': 'Aquele dia foi tempestuoso. Uma chuva torrencial lavava a planície, e grossos raios caíam sobre a terra. Iluminada pelos relâmpagos, uma casa emergia.'  # noqa: E501
#     }  # Assert(verificação)  # noqa: E501
