# pages/checkout_page.py
# Page Object del proceso de checkout de SauceDemo (3 pantallas).

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Representa checkout-step-one, checkout-step-two y checkout-complete."""

    # Pantalla 1: datos del comprador
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Pantalla 2: resumen
    FINISH_BUTTON = (By.ID, "finish")

    # Pantalla 3: confirmacion
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_customer_info(self, first_name, last_name, postal_code):
        """Completa el formulario de datos y hace clic en Continue."""
        logger.info("Completando datos del comprador: %s %s", first_name, last_name)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def finish_order(self):
        """Hace clic en Finish para confirmar la compra."""
        logger.info("Finalizando la compra")
        self.click(self.FINISH_BUTTON)

    def get_confirmation_message(self):
        """Devuelve el mensaje de confirmacion (Thank you for your order!)."""
        return self.get_text(self.CONFIRMATION_HEADER)

    def get_error_message(self):
        """Devuelve el error del formulario (ej: campo obligatorio)."""
        return self.get_text(self.ERROR_MESSAGE)