import sys
import os
import traceback

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

print("=== Test iniciando ===")
print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")

try:
    print("Importando num_a_letras...")
    from num_a_letras import numero_a_letras
    print(f"  1500000 = {numero_a_letras(1500000)}")

    print("Importando reportlab...")
    from reportlab.lib.pagesizes import letter
    print("  OK")

    print("Importando generar_pdf...")
    from generar_pdf import generar_pdf
    print("  OK")

    os.makedirs('pdfs', exist_ok=True)
    empresa = {
        'nombre_empresa': 'EMPRESA ABC S.A.S.',
        'correo_destino': 'test@test.com',
        'valor': 1500000,
        'dia_envio': 10,
        'concepto': 'Arrendamiento software PRESTASOF y GAMMA',
    }

    from datetime import datetime
    print("Generando PDF...")
    ruta = generar_pdf(empresa, datetime.now(), 'pdfs')
    print(f"  PDF generado en: {ruta}")
    print(f"  Archivo existe: {os.path.exists(ruta)}")
    print(f"  Tamanio: {os.path.getsize(ruta)} bytes")

except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()

print("=== Test finalizado ===")
