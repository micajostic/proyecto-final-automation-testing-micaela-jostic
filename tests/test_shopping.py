# tests/test_shopping.py
# Pruebas del catalogo, el carrito y el cierre de sesion de SauceDemo.

import logging

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.mark.ui
def test_catalogo_muestra_productos(inventory_page):
    """El catalogo muestra 6 productos con nombre y precio."""
    assert inventory_page.get_title() == "Products"
    assert inventory_page.get_product_count() == 6
    assert inventory_page.get_first_product_name() != ""
    assert inventory_page.get_first_product_price().startswith("$")


@pytest.mark.ui
def test_agregar_producto_al_carrito(driver, inventory_page):
    """Un producto agregado aparece en el carrito."""
    product_name = inventory_page.get_first_product_name()
    inventory_page.add_first_product_to_cart()
    assert inventory_page.get_cart_count() == 1

    inventory_page.open_cart()
    cart_page = CartPage(driver)
    assert cart_page.get_title() == "Your Cart"
    assert "/cart.html" in cart_page.current_url()
    assert cart_page.get_item_names() == [product_name]


@pytest.mark.ui
def test_quitar_producto_del_carrito(driver, inventory_page):
    """Al quitar el unico producto el carrito queda vacio."""
    inventory_page.add_first_product_to_cart()
    inventory_page.open_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == 1
    cart_page.remove_first_item()
    assert cart_page.get_item_count() == 0


@pytest.mark.ui
def test_cerrar_sesion(driver, inventory_page):
    """Despues de cerrar sesion se vuelve a la pantalla de login."""
    inventory_page.logout()

    login_page = LoginPage(driver)
    assert login_page.is_visible(LoginPage.LOGIN_BUTTON)
    assert "/inventory.html" not in login_page.current_url()