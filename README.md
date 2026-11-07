# Proyecto Final - Framework de Automatizacion de Pruebas

Autora: Micaela Jostic
Curso: Automatizacion QA

## Proposito del proyecto

Framework de pruebas automatizadas que cubre dos capas de una aplicacion:

- **UI:** pruebas de interfaz web sobre [SauceDemo](https://www.saucedemo.com/) con Selenium WebDriver y el patron Page Object Model.
- **API:** pruebas de servicios REST sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con la libreria Requests.

Genera un reporte HTML con el resultado de cada prueba, guarda capturas de pantalla cuando una prueba de UI falla y registra un log detallado de la ejecucion.

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| Pytest | Framework de testing, fixtures y parametrizacion |
| Selenium WebDriver | Automatizacion de la interfaz web (Chrome) |
| Requests | Pruebas de API REST |
| pytest-html | Reporte HTML de resultados |
| logging (libreria estandar) | Registro de pasos clave de la ejecucion |
| Git y GitHub | Control de versiones, ramas y Pull Requests |

## Estructura del proyecto

```
proyecto-final-automation-testing-micaela-jostic/
  data/
    login_data.csv        Datos de prueba del login (casos validos e invalidos)
    checkout_data.csv     Datos de prueba del checkout (campos faltantes)
  pages/                  Page Objects (una clase por pagina)
    base_page.py          Acciones comunes con esperas explicitas
    login_page.py         Pagina de login
    inventory_page.py     Catalogo de productos
    cart_page.py          Carrito de compras
    checkout_page.py      Proceso de checkout (3 pantallas)
  tests/
    test_login.py         Login con datos externos (5 pruebas)
    test_shopping.py      Catalogo, carrito y cierre de sesion (4 pruebas)
    test_checkout.py      Compra completa y checkout incompleto (4 pruebas)
    test_api.py           Pruebas de API (6 pruebas)
  utils/
    api_client.py         Cliente HTTP para JSONPlaceholder
    data_reader.py        Lectura de datos de prueba desde CSV
  reports/
    reporte.html          Reporte HTML de la ultima ejecucion
  conftest.py             Fixtures, capturas de pantalla y marcas en el log
  pytest.ini              Configuracion de pytest (reporte, log, marcadores)
  requirements.txt        Dependencias del proyecto
```

Las carpetas `logs/` y `screenshots/` se crean automaticamente al ejecutar las pruebas y no se suben al repositorio.

## Instalacion de dependencias

Requisitos previos: Python 3 y Google Chrome instalados.

1. Clonar el repositorio:

```
git clone https://github.com/micajostic/proyecto-final-automation-testing-micaela-jostic.git
cd proyecto-final-automation-testing-micaela-jostic
```

2. Instalar las dependencias:

```
python -m pip install -r requirements.txt
```

Selenium descarga automaticamente el driver de Chrome que necesita.

## Como ejecutar las pruebas

Todas las pruebas (UI y API):

```
python -m pytest
```

Solo las pruebas de UI o solo las de API:

```
python -m pytest -m ui
python -m pytest -m api
```

Un archivo o una prueba puntual:

```
python -m pytest tests/test_login.py
python -m pytest -k test_compra_completa
```

Para ver el nombre de cada prueba en la terminal se puede agregar `-v`.

Nota: se usa `python -m pytest` porque en algunas instalaciones de Windows el comando `pytest` no esta en el PATH.

## Casos de prueba cubiertos

| Archivo | Pruebas | Que valida |
|---|---|---|
| test_login.py | 5 | Login valido y 4 escenarios negativos: usuario bloqueado, clave incorrecta, usuario vacio y clave vacia |
| test_shopping.py | 4 | Catalogo, agregar producto al carrito, quitar producto y cerrar sesion |
| test_checkout.py | 4 | Compra completa y 3 escenarios con datos obligatorios faltantes |
| test_api.py | 6 | GET (lista y detalle), 404, POST, DELETE y una peticion encadenada |

Total: 19 pruebas (13 de UI y 6 de API). Cada prueba abre su propio navegador, por lo que son independientes entre si.

## Datos de prueba

Los datos de login y checkout estan en archivos CSV dentro de `data/`. Cada fila es un caso de prueba y `pytest.mark.parametrize` ejecuta la misma prueba una vez por fila. Para agregar un caso solo hay que agregar una linea al CSV.

## Como interpretar los reportes

**Reporte HTML (`reports/reporte.html`)**: se abre con doble clic en el navegador. Muestra el entorno de ejecucion, un resumen con la cantidad de pruebas pasadas y falladas, y una tabla con el resultado (`Passed` o `Failed`), el nombre y la duracion de cada prueba. Se puede filtrar por estado con las casillas de arriba. Al hacer clic en una prueba fallida se despliega el detalle: el error, el log capturado y la captura de pantalla del navegador en el momento de la falla.

**Log (`logs/ejecucion.log`)**: cada linea tiene fecha, hora, nivel, modulo y mensaje. Cada prueba empieza con `===== INICIO: nombre =====` y termina con `===== FIN: nombre =====`, y en el medio se ven los pasos realizados (abrir URL, clics, textos escritos, peticiones HTTP y sus codigos de respuesta). Es el punto de partida para depurar una falla.

**Capturas (`screenshots/`)**: cuando falla una prueba de UI se guarda una imagen con el nombre `AAAAMMDD_HHMMSS_nombre-del-test.png`.

## Como agregar una prueba nueva

1. Si la prueba usa una pagina nueva, crear su clase en `pages/` heredando de `BasePage`.
2. Crear la funcion `test_...` en un archivo de `tests/` usando las fixtures `driver` o `inventory_page`.
3. Marcarla con `@pytest.mark.ui` o `@pytest.mark.api`.
4. Si necesita varios conjuntos de datos, agregar un CSV en `data/` y leerlo con `read_csv`.

## Flujo de trabajo con Git

Cada funcionalidad se desarrollo en una rama propia (`feature/page-objects`, `feature/tests-ui`, `feature/tests-api`, `feature/reportes`) y se fusiono a `main` mediante Pull Request.