"""Fixtures compartidas por todos los tests."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"


@pytest.fixture
def driver():
    """Abre Chrome antes de cada test y lo cierra al terminar."""
    opciones = Options()
    opciones.add_argument("--start-maximized")
    # Evita el aviso de Chrome sobre contrasenas filtradas
    opciones.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    navegador = webdriver.Chrome(options=opciones)

    yield navegador

    navegador.quit()


@pytest.fixture
def inventory_page(driver):
    """Inicia sesion y devuelve el catalogo listo para usar."""
    LoginPage(driver).load().login(STANDARD_USER, STANDARD_PASSWORD)
    page = InventoryPage(driver)
    page.get_title()  # espera a que el catalogo termine de cargar
    return page