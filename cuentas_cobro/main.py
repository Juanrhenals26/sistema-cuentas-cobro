# main.py
# Script principal del Sistema de Cuentas de Cobro
# Ejecutar diariamente con el Programador de Tareas de Windows

import json
import os
import logging
from datetime import datetime

from generar_pdf import generar_pdf
from enviar_correo import enviar_cuenta

# ── Rutas del proyecto ──────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_PDFS = os.path.join(BASE_DIR, 'pdfs')
CARPETA_LOGS = os.path.join(BASE_DIR, 'logs')
ARCHIVO_EMPRESAS = os.path.join(BASE_DIR, 'empresas.json')

# Crear carpetas si no existen
os.makedirs(CARPETA_PDFS, exist_ok=True)
os.makedirs(CARPETA_LOGS, exist_ok=True)

# ── Configurar log ──────────────────────────────────────────────────────
LOG_FILE = os.path.join(CARPETA_LOGS, f"envios_{datetime.now().strftime('%Y_%m')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(),  # También muestra en consola
    ]
)
logger = logging.getLogger(__name__)

MESES_ES = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}


def cargar_empresas() -> list:
    """Lee el archivo empresas.json y retorna la lista de empresas."""
    with open(ARCHIVO_EMPRESAS, 'r', encoding='utf-8') as f:
        return json.load(f)


def procesar_hoy(forzar: bool = False):
    """
    Verifica qué empresas tienen envío hoy y procesa cada una.

    Parámetros:
        forzar: si True, envía a TODAS las empresas sin importar el día.
                Útil para pruebas manuales.
    """
    hoy = datetime.now()
    dia_hoy = hoy.day
    mes_nombre = MESES_ES[hoy.month]

    logger.info("=" * 60)
    logger.info(f"Ejecución del {hoy.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Día actual: {dia_hoy} — Mes: {mes_nombre}")
    logger.info("=" * 60)

    empresas = cargar_empresas()
    empresas_procesadas = 0

    for empresa in empresas:
        nombre = empresa['nombre_empresa']
        dia_envio = empresa['dia_envio']

        if not forzar and dia_hoy != dia_envio:
            logger.info(f"[OMITIDO] {nombre} — día de envío programado: {dia_envio}")
            continue

        logger.info(f"[PROCESANDO] {nombre}")

        # 1. Generar PDF
        try:
            ruta_pdf = generar_pdf(empresa, hoy, CARPETA_PDFS)
            logger.info(f"  PDF generado: {os.path.basename(ruta_pdf)}")
        except Exception as e:
            logger.error(f"  ERROR al generar PDF para {nombre}: {e}")
            continue

        # 2. Enviar correo
        exito = enviar_cuenta(empresa, ruta_pdf, mes_nombre, hoy.year)
        if exito:
            logger.info(f"  Correo enviado a: {empresa['correo_destino']}")
            empresas_procesadas += 1
        else:
            logger.error(f"  FALLO el envío a: {empresa['correo_destino']}")

    logger.info("-" * 60)
    if empresas_procesadas == 0 and not forzar:
        logger.info("Ninguna empresa tiene envío programado para hoy.")
    else:
        logger.info(f"Total procesadas exitosamente: {empresas_procesadas}")
    logger.info("=" * 60)


if __name__ == '__main__':
    import sys

    # Uso: python main.py          -> modo normal (solo envía si es el día)
    # Uso: python main.py --forzar -> envía a TODAS (para pruebas)
    forzar = '--forzar' in sys.argv

    if forzar:
        print("\n⚠️  MODO FORZADO: Se procesarán TODAS las empresas sin importar el día.\n")

    procesar_hoy(forzar=forzar)
