# utils/data_reader.py
# Funciones para leer datos de prueba desde archivos externos (CSV).

import csv
import logging
import os

logger = logging.getLogger(__name__)

# Carpeta data/ ubicada en la raiz del proyecto
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def read_csv(file_name):
    """
    Lee un archivo CSV de la carpeta data/ y devuelve una lista de diccionarios.
    Cada fila del CSV es un diccionario: {nombre_columna: valor}.
    """
    path = os.path.join(DATA_DIR, file_name)
    logger.info("Leyendo datos de prueba desde: %s", path)
    with open(path, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))