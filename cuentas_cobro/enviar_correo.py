# enviar_correo.py
# Envía la cuenta de cobro por correo electrónico usando SMTP de Outlook/Hotmail

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

# ── Configuración del remitente ─────────────────────────────────────────
REMITENTE_EMAIL = "juandavdrhenalsflorez186@gmail.com"
# IMPORTANTE: Usa una contraseña de aplicación si tienes verificación en 2 pasos
# Ve a: https://myaccount.google.com/apppasswords
REMITENTE_CLAVE = ""   # <-- Coloca aquí tu App Password de Gmail

SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PUERTO = 587


def enviar_cuenta(empresa: dict, ruta_pdf: str, mes_nombre: str, anio: int) -> bool:
    """
    Envía la cuenta de cobro por correo con el PDF adjunto.
    """
    destinatario = empresa["correo_destino"]
    nombre_empresa = empresa["nombre_empresa"]

    asunto = f"Cuenta de cobro mes {mes_nombre} {anio}"

    cuerpo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a3a5c; padding: 20px; text-align: center;">
            <h2 style="color: white; margin: 0;">CUENTA DE COBRO</h2>
            <p style="color: #aed6f1; margin: 5px 0 0 0;">{mes_nombre} {anio}</p>
        </div>
        <div style="padding: 25px; background-color: #f9f9f9;">
            <p>Estimados señores,<br><b>{nombre_empresa}</b></p>
            <p>
                Por medio del presente, me permito enviarles adjunta la cuenta de cobro
                correspondiente al mes de <b>{mes_nombre} de {anio}</b>, por concepto de
                <b>{empresa['concepto']}</b>.
            </p>
            <p>
                Por favor encontrar el documento adjunto en formato PDF con el detalle 
                completo de la cuenta.
            </p>
            <p>
                Agradezco la atención prestada y quedo en espera de la confirmación 
                del pago dentro de los términos acordados.
            </p>
        </div>
        <div style="padding: 15px 25px; background-color: #eaf0f8; border-top: 2px solid #1a3a5c;">
            <p style="margin: 0; font-size: 13px;">
                <b>Octavio Cesar Rhenals Mercado</b><br>
                C.C. 78.028.895<br>
                📧 ocrhenals@hotmail.com
            </p>
        </div>
        <p style="font-size: 10px; color: #999; text-align: center; padding: 10px;">
            Correo generado automáticamente — Sistema de Cuentas de Cobro
        </p>
    </body>
    </html>
    """

    # Construir el mensaje
    mensaje = MIMEMultipart('mixed')
    mensaje['From'] = REMITENTE_EMAIL
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    mensaje.attach(MIMEText(cuerpo_html, 'html', 'utf-8'))

    # Adjuntar el PDF
    with open(ruta_pdf, 'rb') as f:
        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(f.read())
    encoders.encode_base64(adjunto)
    nombre_adjunto = os.path.basename(ruta_pdf)
    adjunto.add_header('Content-Disposition', f'attachment; filename="{nombre_adjunto}"')
    mensaje.attach(adjunto)

    # Enviar
    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PUERTO) as servidor:
            servidor.ehlo()
            servidor.starttls(context=contexto)
            servidor.ehlo()
            servidor.login(REMITENTE_EMAIL, REMITENTE_CLAVE)
            servidor.sendmail(REMITENTE_EMAIL, destinatario, mensaje.as_bytes())
        print(f"  [OK] Correo enviado a: {destinatario} ({nombre_empresa})")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"  [ERROR] Autenticación fallida: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"  [ERROR] Fallo SMTP al enviar a {destinatario}: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Error inesperado al enviar a {destinatario}: {e}")
        return False
