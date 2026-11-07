# utils/api_client.py
# Cliente para la API publica JSONPlaceholder (https://jsonplaceholder.typicode.com)

import logging

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://jsonplaceholder.typicode.com"
REQUEST_TIMEOUT = 10  # segundos


class JsonPlaceholderClient:
    """Agrupa las llamadas HTTP a la API para no repetirlas en los tests."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def _request(self, method, path, **kwargs):
        """Hace la peticion, registra en el log y devuelve la respuesta."""
        url = self.base_url + path
        logger.info("Peticion %s %s", method, url)
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
        logger.info("Respuesta %s en %s", response.status_code, url)
        return response

    def get_posts(self):
        """GET /posts: lista de publicaciones."""
        return self._request("GET", "/posts")

    def get_post(self, post_id):
        """GET /posts/{id}: una publicacion."""
        return self._request("GET", "/posts/{}".format(post_id))

    def create_post(self, payload):
        """POST /posts: crea una publicacion con los datos recibidos."""
        return self._request("POST", "/posts", json=payload)

    def delete_post(self, post_id):
        """DELETE /posts/{id}: elimina una publicacion."""
        return self._request("DELETE", "/posts/{}".format(post_id))