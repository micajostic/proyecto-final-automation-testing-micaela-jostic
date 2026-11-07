# pages/inventory_page.py
# Page Object del catalogo de productos de SauceDemo.

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Representa https://www.saucedemo.com/inventory.html"""

    # Selectores
    TITLE = (By.CLASS_NAME, "title")
    PRODUCTS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_title(self):
        """Devuelve el titulo de la pagina (ej: Products)."""
        return self.get_text(self.TITLE)

    def get_product_count(self):
        """Cantidad de productos visibles en el catalogo."""
        self.find(self.PRODUCTS)
        return len(self.driver.find_elements(*self.PRODUCTS))

    def get_first_product_name(self):
        """Nombre del primer producto."""
        return self.driver.find_elements(*self.PRODUCT_NAMES)[0].text

    def get_first_product_price(self):
        """Precio del primer producto (texto, ej: $29.99)."""
        return self.driver.find_elements(*self.PRODUCT_PRICES)[0].text

    def add_first_product_to_cart(self):
        """Agrega el primer producto al carrito."""
        logger.info("Agregando el primer producto al carrito")
        self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)[0].click()

    def get_cart_count(self):
        """Numero que muestra el carrito. Devuelve 0 si esta vacio."""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def open_cart(self):
        """Hace clic en el icono del carrito."""
        self.click(self.CART_LINK)

    def logout(self):
        """Abre el menu lateral y cierra sesion."""
        logger.info("Cerrando sesion")
        self.click(self.MENU_BUTTON)
        logout_link = self.find(self.LOGOUT_LINK)
        # Clic por JavaScript: el menu lateral tiene una animacion
        # y un clic normal puede caer mientras todavia se mueve
        self.driver.execute_script("arguments[0].click();", logout_link)