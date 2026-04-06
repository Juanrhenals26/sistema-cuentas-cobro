# num_a_letras.py
# Convierte números enteros a su representación en letras en español

UNIDADES = [
    '', 'UN', 'DOS', 'TRES', 'CUATRO', 'CINCO',
    'SEIS', 'SIETE', 'OCHO', 'NUEVE', 'DIEZ',
    'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE',
    'DIECISÉIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE', 'VEINTE',
    'VEINTIÚN', 'VEINTIDÓS', 'VEINTITRÉS', 'VEINTICUATRO', 'VEINTICINCO',
    'VEINTISÉIS', 'VEINTISIETE', 'VEINTIOCHO', 'VEINTINUEVE'
]

DECENAS = [
    '', '', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA',
    'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA'
]

CENTENAS = [
    '', 'CIEN', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS',
    'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS'
]


def _centenas(n):
    if n == 0:
        return ''
    if n == 100:
        return 'CIEN'
    c = n // 100
    resto = n % 100
    resultado = CENTENAS[c]
    if resto > 0:
        resultado += ' ' + _decenas(resto)
    return resultado.strip()


def _decenas(n):
    if n < 30:
        return UNIDADES[n]
    d = n // 10
    u = n % 10
    if u == 0:
        return DECENAS[d]
    return DECENAS[d] + ' Y ' + UNIDADES[u]


def _miles(n):
    if n == 0:
        return ''
    if n == 1:
        return 'MIL'
    miles = n // 1000
    resto = n % 1000
    if miles == 1:
        prefijo = 'MIL'
    else:
        prefijo = _centenas(miles) + ' MIL'
    if resto > 0:
        return prefijo + ' ' + _centenas(resto)
    return prefijo


def numero_a_letras(numero):
    """
    Convierte un número entero a su representación en letras en español.
    Ejemplo: 1500000 -> 'UN MILLÓN QUINIENTOS MIL PESOS M/CTE'
    """
    numero = int(numero)
    if numero == 0:
        return 'CERO PESOS M/CTE'

    if numero >= 1_000_000:
        millones = numero // 1_000_000
        resto = numero % 1_000_000
        if millones == 1:
            texto_millones = 'UN MILLÓN'
        else:
            texto_millones = _centenas(millones) + ' MILLONES'
        if resto > 0:
            return (texto_millones + ' ' + _miles(resto) if resto >= 1000
                    else texto_millones + ' ' + _centenas(resto)).strip() + ' PESOS M/CTE'
        return texto_millones + ' PESOS M/CTE'

    if numero >= 1000:
        return _miles(numero).strip() + ' PESOS M/CTE'

    return _centenas(numero).strip() + ' PESOS M/CTE'


if __name__ == '__main__':
    # Prueba rápida
    pruebas = [0, 100, 1000, 1500, 15000, 150000, 1500000, 2500000, 3000000]
    for n in pruebas:
        print(f"  {n:>10,} -> {numero_a_letras(n)}")
