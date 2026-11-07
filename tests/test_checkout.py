# tests/test_checkout.py
# Pruebas del proceso de compra (checkout) de SauceDemo.

import logging

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_reader import read_csv

logger = logging.getLogger(__name__)

# Casos negativos: cada fila del CSV deja un campo obligatorio vacio
INCOMPLETE_DATA = read_csv("checkout_data.csv")


def build_case_id(row):
    """Nombre legible para cada caso en el reporte."""
    return row["expected_message"]


def go_to_checkout_form(driver, inventory_page):
    """Agrega un producto, abre el carrito y llega al formulario de checkout."""
    inventory_page.add_first_product_to_cart()
    inventory_page.open_cart()
    CartPage(driver).go_to_checkout()
    return CheckoutPage(driver)


@pytest.mark.ui
def test_compra_completa(driver, inventory_page):
    """Flujo completo: producto, carrito, datos, resumen y confirmacion."""
    checkout_page = go_to_checkout_form(driver, inventory_page)
    checkout_page.fill_customer_info("Micaela", "Jostic", "1000")
    assert "checkout-step-two" in checkout_page.current_url()

    checkout_page.finish_order()
    assert checkout_page.get_confirmation_message() == "Thank you for your order!"
    assert "checkout-complete" in checkout_page.current_url()


@pytest.mark.ui
@pytest.mark.parametrize("row", INCOMPLETE_DATA, ids=build_case_id)
def test_checkout_con_datos_incompletos(driver, inventory_page, row):
    """Si falta un dato obligatorio se muestra el error y no se avanza."""
    checkout_page = go_to_checkout_form(driver, inventory_page)
    checkout_page.fill_customer_info(
        row["first_name"], row["last_name"], row["postal_code"]
    )

    assert row["expected_message"] in checkout_page.get_error_message()
    assert "checkout-step-one" in checkout_page.current_url()