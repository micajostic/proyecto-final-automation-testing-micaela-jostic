# tests/test_api.py
# Pruebas de la API publica JSONPlaceholder con la libreria requests.

import logging

import pytest

from utils.api_client import JsonPlaceholderClient

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client():
    """Cliente de API nuevo para cada test."""
    return JsonPlaceholderClient()


@pytest.mark.api
def test_obtener_publicacion_existente(api_client):
    """GET /posts/1 devuelve 200 y la estructura esperada."""
    response = api_client.get_post(1)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    for field in ("userId", "id", "title", "body"):
        assert field in body


@pytest.mark.api
def test_listar_publicaciones(api_client):
    """GET /posts devuelve una lista con 100 publicaciones."""
    response = api_client.get_posts()

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100
    assert "title" in posts[0]


@pytest.mark.api
def test_publicacion_inexistente(api_client):
    """GET de un id que no existe devuelve 404 y cuerpo vacio (escenario de error)."""
    response = api_client.get_post(99999)

    assert response.status_code == 404
    assert response.json() == {}


@pytest.mark.api
def test_crear_publicacion(api_client):
    """POST /posts devuelve 201 y repite los datos enviados con un id nuevo."""
    payload = {"title": "Mi publicacion", "body": "Contenido de prueba", "userId": 1}

    response = api_client.create_post(payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
def test_eliminar_publicacion(api_client):
    """DELETE /posts/1 devuelve 200 y cuerpo vacio."""
    response = api_client.delete_post(1)

    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.api
def test_encadenado_listar_y_obtener(api_client):
    """Encadenamiento: el id del primer post de la lista se usa en la segunda peticion."""
    first_post = api_client.get_posts().json()[0]
    logger.info("Primer post de la lista: id=%s", first_post["id"])

    detail = api_client.get_post(first_post["id"])

    assert detail.status_code == 200
    assert detail.json()["title"] == first_post["title"]