# tests/test_login.py
# Pruebas de login de SauceDemo con datos externos (data/login_data.csv).

import logging

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_reader import read_csv

logger = logging.getLogger(__name__)

# Se leen todas las filas del CSV y se separan segun el resultado esperado
ALL_ROWS = read_csv("login_data.csv")
VALID_ROWS = [row for row in ALL_ROWS if row["expected_result"] == "success"]
INVALID_ROWS = [row for row in ALL_ROWS if row["expected_result"] == "error"]


def build_case_id(row):
    """Nombre legible para cada caso en el reporte."""
    return "{}-{}".format(row["username"] or "sin_usuario", row["expected_message"] or "ok")


@pytest.mark.ui
@pytest.mark.parametrize("row", VALID_ROWS, ids=build_case_id)
def test_login_exitoso(driver, row):
    """Con credenciales validas se llega al catalogo de productos."""
    login_page = LoginPage(driver).load()
    login_page.login(row["username"], row["password"])

    inventory_page = InventoryPage(driver)
    assert inventory_page.get_title() == "Products"
    assert "/inventory.html" in login_page.current_url()


@pytest.mark.ui
@pytest.mark.parametrize("row", INVALID_ROWS, ids=build_case_id)
def test_login_invalido(driver, row):
    """Con datos invalidos se muestra el mensaje de error esperado."""
    login_page = LoginPage(driver).load()
    login_page.login(row["username"], row["password"])

    error_text = login_page.get_error_message()
    logger.info("Mensaje de error obtenido: %s", error_text)
    assert row["expected_message"] in error_text
    assert "/inventory.html" not in login_page.current_url()