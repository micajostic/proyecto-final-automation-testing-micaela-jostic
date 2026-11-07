"""Funciones auxiliares y selectores del sitio saucedemo.com."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import URL_BASE, TIMEOUT


# ---------- SELECTORES: LOGIN ----------
CAMPO_USUARIO = (By.ID, "user-name")
CAMPO_PASSWORD = (By.ID, "password")
BOTON_LOGIN = (By.ID, "login-button")
TITULO_PRODUCTOS = (By.CLASS_NAME, "title")
MENSAJE_ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

# ---------- SELECTORES: INVENTARIO ----------
CONTENEDOR_INVENTARIO = (By.ID, "inventory_container")
PRODUCTOS = (By.CLASS_NAME, "inventory_item")
NOMBRE_PRODUCTO = (By.CLASS_NAME, "inventory_item_name")
PRECIO_PRODUCTO = (By.CLASS_NAME, "inventory_item_price")
FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")
BOTON_MENU = (By.ID, "react-burger-menu-btn")

# ---------- SELECTORES: CARRITO ----------
BOTON_AGREGAR = (By.CLASS_NAME, "btn_inventory")
CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
LINK_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
ITEMS_CARRITO = (By.CLASS_NAME, "cart_item")


# ---------- LOGIN ----------
def ir_a_login(driver):
    """Abre la pagina de login de saucedemo."""
    driver.get(URL_BASE)


def iniciar_sesion(driver, usuario, password):
    """Completa el formulario de login y hace clic en Login."""
    driver.find_element(*CAMPO_USUARIO).send_keys(usuario)
    driver.find_element(*CAMPO_PASSWORD).send_keys(password)
    driver.find_element(*BOTON_LOGIN).click()


# ---------- ESPERAS ----------
def esperar_url_contiene(driver, texto, timeout=TIMEOUT):
    """Espera explicita: frena hasta que la URL contenga el texto."""
    WebDriverWait(driver, timeout).until(EC.url_contains(texto))


def esperar_elemento(driver, localizador, timeout=TIMEOUT):
    """Espera explicita: frena hasta que el elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_contador_carrito(driver, valor, timeout=TIMEOUT):
    """Espera explicita hasta que el globito del carrito muestre ese valor."""
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element(CONTADOR_CARRITO, str(valor))
    )


# ---------- INVENTARIO ----------
def listar_productos(driver):
    """Devuelve la lista de productos visibles en el inventario."""
    esperar_elemento(driver, CONTENEDOR_INVENTARIO)
    return driver.find_elements(*PRODUCTOS)


def datos_primer_producto(driver):
    """Devuelve una tupla (nombre, precio) del primer producto del listado."""
    primer_producto = listar_productos(driver)[0]

    nombre = primer_producto.find_element(*NOMBRE_PRODUCTO).text
    precio = primer_producto.find_element(*PRECIO_PRODUCTO).text

    return nombre, precio


# ---------- CARRITO ----------
def agregar_primer_producto_al_carrito(driver):
    """Agrega el primer producto al carrito y devuelve su nombre."""
    primer_producto = listar_productos(driver)[0]

    nombre = primer_producto.find_element(*NOMBRE_PRODUCTO).text
    primer_producto.find_element(*BOTON_AGREGAR).click()

    return nombre


def contador_carrito(driver):
    """Devuelve el numero del globito del carrito. Si no hay globito, devuelve 0."""
    globitos = driver.find_elements(*CONTADOR_CARRITO)

    if not globitos:
        return 0

    return int(globitos[0].text)


def ir_al_carrito(driver):
    """Hace clic en el icono del carrito y espera a que cargue esa pagina."""
    driver.find_element(*LINK_CARRITO).click()
    esperar_url_contiene(driver, "/cart.html")


def items_del_carrito(driver):
    """Devuelve la lista de productos que hay dentro del carrito."""
    return driver.find_elements(*ITEMS_CARRITO)