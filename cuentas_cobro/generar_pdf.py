import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from num_a_letras import numero_a_letras

# Datos fijos del emisor
EMISOR = {
    "nombre": "Octavio Cesar Rhenals Mercado",
    "identificacion": "78.028.895 de Cerete",
    "correo": "ocrhenals@hotmail.com",
    "cuenta_banco": "Bancolombia",
    "cuenta_num": "091-388984-55",
    "cuenta_tipo": "Ahorro"
}

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}


def generar_pdf(empresa: dict, fecha: datetime, carpeta_salida: str) -> str:
    """
    Genera el PDF con el diseño de captura (fondo azul claro, tablas estructuradas, firma).
    """
    mes_nombre = MESES_ES[fecha.month]
    anio = fecha.year
    dia = fecha.day

    nombre_archivo = (
        f"CuentaCobro_{empresa['nombre_empresa'].replace(' ', '_').replace('.', '')}_"
        f"{mes_nombre.upper()}_{anio}.pdf"
    )
    ruta_pdf = os.path.join(carpeta_salida, nombre_archivo)

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    # Estilos de texto
    estilo_titulo = ParagraphStyle(
        'titulo', parent=styles['Normal'], fontSize=12,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    estilo_negrita = ParagraphStyle(
        'negrita', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold'
    )
    estilo_normal = ParagraphStyle(
        'normal', parent=styles['Normal'], fontSize=10, fontName='Helvetica'
    )
    estilo_centro = ParagraphStyle(
        'centro', parent=styles['Normal'], fontSize=10, 
        alignment=TA_CENTER, fontName='Helvetica'
    )
    estilo_centro_negrita = ParagraphStyle(
        'centro_negrita', parent=styles['Normal'], fontSize=11, 
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    estilo_centro_grande = ParagraphStyle(
        'centro_grande', parent=styles['Normal'], fontSize=14, 
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )
    estilo_justificado = ParagraphStyle(
        'justificado', parent=styles['Normal'], fontSize=10, 
        alignment=TA_JUSTIFY, fontName='Helvetica'
    )

    valor_formato = f"${empresa['valor']:,.0f}".replace(',', '.')
    valor_letras = numero_a_letras(empresa['valor']).capitalize().replace(" m/cte", " mct.")
    if "mct" not in valor_letras.lower():
        valor_letras += " mct."
        
    concepto_txt = f"Por concepto de {empresa['concepto']} del mes de {mes_nombre} {anio}."

    elementos = []
    azul_claro = colors.HexColor('#d9e1f2')
    azul_oscuro = colors.HexColor('#4472c4') # Para texto o borde si es necesario

    # --- 1. TABLA SUPERIOR ---
    fecha_str = f"{dia} {mes_nombre}. de {anio}"
    
    col_widths_top = [3.5 * cm, 7.5 * cm, 4 * cm]
    datos_top = [
        ['', Paragraph("CUENTA DE COBRO", estilo_titulo), ''],
        [Paragraph('Responsable', estilo_negrita), Paragraph(EMISOR['nombre'], estilo_normal), ''],
        [Paragraph('Identificación', estilo_negrita), Paragraph(EMISOR['identificacion'], estilo_normal), ''],
        [Paragraph('Fecha', estilo_negrita), Paragraph(fecha_str, estilo_normal), ''],
        [Paragraph('Valor', estilo_negrita), Paragraph(f"<b>{valor_formato}</b>", estilo_normal), ''],
        [Paragraph('Valor Letras', estilo_negrita), Paragraph(valor_letras, estilo_normal), ''],
    ]

    tabla_top = Table(datos_top, colWidths=col_widths_top)
    estilo_tabla_top = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, azul_oscuro),
        ('BACKGROUND', (0, 1), (0, 5), azul_claro),  # Fondo azul a etiquetas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Combinaciones
        ('SPAN', (1, 1), (2, 1)), # Responsable
        ('SPAN', (1, 2), (2, 2)), # Identificacion
        # Fecha NO combina con celda 3
        ('SPAN', (1, 4), (2, 4)), # Valor
        ('SPAN', (1, 5), (2, 5)), # Valor Letras
    ])
    tabla_top.setStyle(estilo_tabla_top)
    elementos.append(tabla_top)
    elementos.append(Spacer(1, 0.5 * cm))

    # --- 2. CUADRO CENTRAL (DESCRIPCIÓN) ---
    texto_legal = (
        "Solicito a ustedes la aplicación de la tabla de retención en la fuente "
        "establecida en el artículo 383 del estatuto tributario, ya que para las "
        "actividades realizadas para ustedes no he contratado o vinculado dos (2) o "
        "más trabajadores asociados a dichas actividades. Dichas actividades "
        "fueron realizadas de manera personal."
    )
    
    # Construir contenido del cuadro central
    contenido_central = []
    contenido_central.append(Paragraph(empresa['nombre_empresa'].upper(), estilo_centro_grande))
    contenido_central.append(Paragraph("debe a", estilo_centro))
    contenido_central.append(Spacer(1, 10))
    contenido_central.append(Paragraph(EMISOR['nombre'].upper(), estilo_centro_grande))
    contenido_central.append(Spacer(1, 15))
    contenido_central.append(Paragraph(f"La suma de {valor_letras.lower()} ({valor_formato})", estilo_negrita))
    contenido_central.append(Spacer(1, 15))
    contenido_central.append(Paragraph(concepto_txt, estilo_justificado))
    contenido_central.append(Spacer(1, 15))
    contenido_central.append(Paragraph(texto_legal, estilo_justificado))
    contenido_central.append(Spacer(1, 15))
    contenido_central.append(Paragraph(f"Se firma en Montería a los {dia} días del mes de {mes_nombre} del {anio}.", estilo_normal))
    contenido_central.append(Spacer(1, 15))
    contenido_central.append(Paragraph("Cuenta Bancaria:", estilo_centro_negrita))
    contenido_central.append(Spacer(1, 5))
    
    # Banco a la izquierda
    txt_banco = f"<b>{EMISOR['cuenta_banco']}</b><br/><font color='gray'>{EMISOR['cuenta_num']}</font><br/>{EMISOR['cuenta_tipo']}"
    contenido_central.append(Paragraph(txt_banco, estilo_normal))

    # Lo metemos en una tabla de 1 celda para el cuadro azul
    tabla_central = Table(
        [
            [Paragraph("DESCRIPCIÓN", estilo_centro_negrita)],
            [contenido_central]
        ],
        colWidths=[15 * cm]
    )
    tabla_central.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, azul_oscuro),
        ('BACKGROUND', (0, 1), (0, 1), azul_claro),  # Fondo azul claro al contenido
        ('BACKGROUND', (0, 0), (0, 0), colors.white), # DESCRIPCION en blanco
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 1), (0, 1), 15),
        ('TOPPADDING', (0, 1), (0, 1), 15),
        ('LEFTPADDING', (0, 1), (0, 1), 15),
        ('RIGHTPADDING', (0, 1), (0, 1), 15),
    ]))
    elementos.append(tabla_central)
    elementos.append(Spacer(1, 0.3 * cm))

    # --- 3. RECUADRO INFERIOR (FIRMA Y RECIBE) ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_firma = os.path.join(base_dir, "firma.png")
    
    img_firma = ""
    if os.path.exists(ruta_firma):
        # Ajustar el tamaño manteniendo la proporción
        img_firma = Image(ruta_firma, width=4*cm, height=1.5*cm)

    firma_col = [
        img_firma if img_firma else Spacer(1, 1.5*cm),
        Paragraph("________________________________", estilo_normal),
        Paragraph("<b>Entregado</b>", estilo_normal)
    ]
    
    recibe_col = [
        Spacer(1, 1.5*cm), # Mismo espacio
        Paragraph("Recibe", estilo_centro_negrita)
    ]

    tabla_firmas = Table([
        [firma_col, recibe_col]
    ], colWidths=[10 * cm, 5 * cm])
    
    tabla_firmas.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, azul_oscuro),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabla_firmas)

    doc.build(elementos)
    print(f"  [OK] PDF modificado generado: {ruta_pdf}")
    return ruta_pdf


if __name__ == '__main__':
    # Prueba rápida
    empresa_prueba = {
        "nombre_empresa": "COOMULTICOR",
        "correo_destino": "test@test.com",
        "valor": 500000,
        "dia_envio": 10,
        "concepto": "Arrendamiento software PRESTASOF y GAMMA",
    }
    # Fecha de la captura
    fecha_prueba = datetime.strptime("2026-03-29", "%Y-%m-%d")
    
    os.makedirs('pdfs', exist_ok=True)
    ruta = generar_pdf(empresa_prueba, fecha_prueba, 'pdfs')
    print(f"PDF de prueba generado en: {ruta}")
