"""Fixtures y hooks compartidos por todos los tests."""

import base64
import logging
import os
import re
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"

# Carpeta donde se guardan las capturas de los tests que fallan
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


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


@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    """Marca en el log el inicio y el fin de cada test."""
    logger.info("===== INICIO: %s =====", request.node.name)
    yield
    logger.info("===== FIN: %s =====", request.node.name)


def save_screenshot(driver, test_name):
    """
    Guarda una captura en screenshots/ con fecha, hora y nombre del test.
    Devuelve los bytes de la imagen (o None si no se pudo capturar).
    """
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", test_name)
        path = os.path.join(SCREENSHOT_DIR, "{}_{}.png".format(timestamp, safe_name))
        png = driver.get_screenshot_as_png()
        with open(path, "wb") as image_file:
            image_file.write(png)
        logger.error("Captura guardada en: %s", path)
        return png
    except Exception as error:
        logger.error("No se pudo capturar la pantalla: %s", error)
        return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Registra el resultado de cada test y, si falla, captura la pantalla."""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.failed):
        logger.info("Resultado de %s: %s", item.name, report.outcome.upper())

        extras = getattr(report, "extras", [])
        driver = item.funcargs.get("driver")
        if report.failed and driver is not None:
            png = save_screenshot(driver, item.name)
            if png is not None:
                encoded = base64.b64encode(png).decode("utf-8")
                extras.append(pytest_html.extras.png(encoded))
        report.extras = extras