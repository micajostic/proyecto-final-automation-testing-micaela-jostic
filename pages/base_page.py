# pages/base_page.py
# Clase base: acciones comunes que heredan todas las paginas.

import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    """Clase padre de todos los Page Objects."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def open(self, url):
        """Abre una URL en el navegador."""
        logger.info("Abriendo URL: %s", url)
        self.driver.get(url)

    def find(self, locator):
        """Espera a que el elemento sea visible y lo devuelve."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        """Espera a que el elemento sea clickeable y hace clic."""
        logger.info("Click en: %s", locator)
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type_text(self, locator, text):
        """Borra el campo y escribe el texto."""
        logger.info("Escribiendo en %s", locator)
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Devuelve el texto visible de un elemento."""
        return self.find(locator).text

    def is_visible(self, locator):
        """Devuelve True si el elemento aparece dentro del timeout."""
        try:
            self.find(locator)
            return True
        except Exception:
            return False

    def current_url(self):
        """Devuelve la URL actual."""
        return self.driver.current_url