from http import HTTPStatus

from fastapi.testclient import TestClient

from translator.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)

    assert response.json() == {'message': 'Olá Mundo'}  # Assert (verificação)


# testando se está funcionando o llm3
def test_llm3_deve_retornar_ok_e_mensagem_com_texto_traduzido():
    client = TestClient(app)  # Arrange (organização)

    response = client.post(
        '/llm3/',
        json={
            'idioma': 'en',
            'comentario': 'Olá Mundo',
        },
    )  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)

    assert response.json() == {'message': 'Hello World'}  # Assert(verificação)


# testando com algo mais complexo
def test_llm3_deve_retornar_ok_e_mensagem_com_texto_traduzido2():
    client = TestClient(app)  # Arrange (organização)

    response = client.post(
        '/llm3/',
        json={
            'idioma': 'pt_br',
            'comentario': 'その日は嵐だった。叩きつけるような雨が草原を洗い、太い雷が何本も大地へと落ちた。雷光に照らされて、一軒の家が浮かび上がる.',  # noqa: E501
        },
    )  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (verificação)

    assert response.json() == {'message': 'Aquele dia foi tempestuoso. Uma chuva torrencial lavava a planície, e grossos raios caíam sobre a terra. Iluminada pelos relâmpagos, uma casa emergia.'}  # Assert(verificação)  # noqa: E501
