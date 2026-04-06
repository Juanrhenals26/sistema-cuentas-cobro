import smtplib
import ssl
import sys

email = 'juandavdrhenalsflorez186@gmail.com'
password = 'twiaurhueyrxcvtg'
server_addr = 'smtp.gmail.com'
port = 587

print(f"Probando conexion a {server_addr}:{port} para {email} con GMAIL...")

try:
    context = ssl.create_default_context()
    with smtplib.SMTP(server_addr, port) as server:
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        print("Intentando login...")
        server.login(email, password)
        print("\n¡LOGIN EXITOSO!")
except smtplib.SMTPAuthenticationError as e:
    print(f"\nERROR DE AUTENTICACION GMAIL: {e}")
except Exception as e:
    print(f"\nOTRO ERROR: {type(e).__name__}: {e}")
