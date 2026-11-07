"""Fixtures compartidas por todos los tests."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Abre Chrome antes de cada test y lo cierra al terminar."""
    opciones = Options()
    opciones.add_argument("--start-maximized")

    navegador = webdriver.Chrome(options=opciones)

    yield navegador

    navegador.quit()

