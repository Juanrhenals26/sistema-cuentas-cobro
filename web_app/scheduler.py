"""
scheduler.py — Tarea programada diaria para envío de cuentas de cobro
"""
import sys
import os

# Agregar cuentas_cobro al path para importar módulos existentes
CUENTAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cuentas_cobro')
sys.path.insert(0, CUENTAS_DIR)

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import database as db
import generar_pdf as gpdf
import enviar_correo as ec

CARPETA_PDFS = os.path.join(CUENTAS_DIR, 'pdfs')
os.makedirs(CARPETA_PDFS, exist_ok=True)

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}


def procesar_empresa(empresa: dict) -> tuple:
    """
    Genera el PDF y envía el correo para una empresa.
    Retorna (exito: bool, mensaje: str)
    """
    # Leer config actual de BD para usar credenciales actualizadas
    cfg = db.get_config()
    ec.REMITENTE_EMAIL = cfg.get('email_remitente', 'ocrhenals@hotmail.com')
    ec.REMITENTE_CLAVE = cfg.get('email_clave', '')
    ec.SMTP_SERVIDOR   = cfg.get('smtp_servidor', 'smtp-mail.outlook.com')
    ec.SMTP_PUERTO     = int(cfg.get('smtp_puerto', 587))

    hoy = datetime.now()
    mes_nombre = MESES_ES[hoy.month]

    try:
        ruta_pdf = gpdf.generar_pdf(empresa, hoy, CARPETA_PDFS)
        exito    = ec.enviar_cuenta(empresa, ruta_pdf, mes_nombre, hoy.year)

        if exito:
            db.registrar_envio(empresa['id'], empresa['nombre_empresa'],
                               mes_nombre, hoy.year, 'OK')
            return True, f"Enviado correctamente a {empresa['correo_destino']}"
        else:
            db.registrar_envio(empresa['id'], empresa['nombre_empresa'],
                               mes_nombre, hoy.year, 'ERROR', 'Fallo en envío SMTP')
            return False, 'Fallo al enviar el correo — revisa credenciales en Configuración'

    except Exception as e:
        error = str(e)
        db.registrar_envio(empresa['id'], empresa['nombre_empresa'],
                           mes_nombre, hoy.year, 'ERROR', error)
        return False, error


def job_diario():
    """Revisa las empresas activas y envía las que corresponden al día de hoy."""
    hoy = datetime.now()
    dia_hoy = hoy.day
    print(f"[Scheduler] Revisando envíos para el día {dia_hoy}...")

    empresas = db.get_todas_empresas()
    procesadas = 0

    for e in empresas:
        if e['activa'] and e['dia_envio'] == dia_hoy:
            print(f"[Scheduler] Enviando a: {e['nombre_empresa']}")
            exito, msg = procesar_empresa(e)
            print(f"[Scheduler]   → {'OK' if exito else 'ERROR'}: {msg}")
            procesadas += 1

    if procesadas == 0:
        print(f"[Scheduler] Ninguna empresa programada para hoy (día {dia_hoy})")


def iniciar_scheduler():
    """Inicia el scheduler en background y retorna la instancia."""
    cfg = db.get_config()
    hora   = cfg.get('hora_envio', '08')
    minuto = cfg.get('minuto_envio', '00')

    scheduler = BackgroundScheduler(timezone='America/Bogota')
    scheduler.add_job(job_diario, 'cron', hour=int(hora), minute=int(minuto),
                      id='envio_diario', replace_existing=True)
    scheduler.start()
    print(f"[Scheduler] Activo — revisión diaria a las {hora}:{minuto} (hora Bogotá)")
    return scheduler
