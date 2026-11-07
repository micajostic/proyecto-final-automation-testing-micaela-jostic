# pages/cart_page.py
# Page Object del carrito de compras de SauceDemo.

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Representa https://www.saucedemo.com/cart.html"""

    # Selectores
    TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_title(self):
        """Devuelve el titulo de la pagina (ej: Your Cart)."""
        return self.get_text(self.TITLE)

    def get_item_names(self):
        """Devuelve una lista con los nombres de los productos del carrito."""
        self.find(self.TITLE)
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [element.text for element in elements]

    def get_item_count(self):
        """Cantidad de productos que hay en el carrito."""
        self.find(self.TITLE)
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_first_item(self):
        """Quita el primer producto del carrito."""
        logger.info("Quitando el primer producto del carrito")
        self.driver.find_elements(*self.REMOVE_BUTTONS)[0].click()

    def go_to_checkout(self):
        """Hace clic en Checkout."""
        logger.info("Yendo al checkout")
        self.click(self.CHECKOUT_BUTTON)