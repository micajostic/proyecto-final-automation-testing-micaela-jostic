# pages/login_page.py
# Page Object de la pagina de login de SauceDemo.

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Representa https://www.saucedemo.com/ (pantalla de login)."""

    URL = "https://www.saucedemo.com/"

    # Selectores: viven aca, no en los tests
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        """Abre la pagina de login."""
        self.open(self.URL)
        return self

    def login(self, username, password):
        """Completa usuario y clave y hace clic en Login."""
        logger.info("Login con usuario: %s", username)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Devuelve el texto del mensaje de error (login fallido)."""
        return self.get_text(self.ERROR_MESSAGE)