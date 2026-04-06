"""
database.py — Gestión de la base de datos SQLite
Tablas: empresas, envios_log, config
"""
import sqlite3
import json
import os
from datetime import datetime

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DB_PATH   = os.path.join(BASE_DIR, 'cuentas_cobro.db')
JSON_PATH = os.path.join(BASE_DIR, '..', 'cuentas_cobro', 'empresas.json')


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Crea tablas y migra el JSON si la BD está vacía."""
    conn = get_conn()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT NOT NULL,
            correo_destino TEXT NOT NULL,
            valor          REAL NOT NULL,
            dia_envio      INTEGER NOT NULL,
            concepto       TEXT NOT NULL,
            activa         INTEGER DEFAULT 1,
            creado_en      TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS envios_log (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id      INTEGER,
            empresa_nombre  TEXT,
            fecha_envio     TEXT,
            mes             TEXT,
            anio            INTEGER,
            estado          TEXT,
            error_msg       TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE SET NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS config (
            clave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')

    # Migrar JSON → BD si no hay empresas
    c.execute('SELECT COUNT(*) FROM empresas')
    if c.fetchone()[0] == 0 and os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            empresas = json.load(f)
        for e in empresas:
            c.execute(
                'INSERT INTO empresas (nombre_empresa, correo_destino, valor, dia_envio, concepto) VALUES (?,?,?,?,?)',
                (e['nombre_empresa'], e['correo_destino'], e['valor'], e['dia_envio'], e['concepto'])
            )
        print(f"[DB] {len(empresas)} empresas migradas desde empresas.json")

    # Config por defecto
    defaults = [
        ('email_remitente', 'ocrhenals@hotmail.com'),
        ('email_clave',     'melimeli1'),
        ('hora_envio',      '08'),
        ('minuto_envio',    '00'),
        ('smtp_servidor',   'smtp-mail.outlook.com'),
        ('smtp_puerto',     '587'),
    ]
    for clave, valor in defaults:
        c.execute('INSERT OR IGNORE INTO config (clave, valor) VALUES (?,?)', (clave, valor))

    conn.commit()
    conn.close()


# ── CRUD Empresas ──────────────────────────────────────────────────────────────

def get_todas_empresas():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM empresas ORDER BY dia_envio, nombre_empresa').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_empresa(id):
    conn = get_conn()
    row = conn.execute('SELECT * FROM empresas WHERE id=?', (id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def crear_empresa(data):
    conn = get_conn()
    conn.execute(
        'INSERT INTO empresas (nombre_empresa, correo_destino, valor, dia_envio, concepto, activa) VALUES (?,?,?,?,?,?)',
        (data['nombre_empresa'], data['correo_destino'], float(data['valor']),
         int(data['dia_envio']), data['concepto'], int(data.get('activa', 1)))
    )
    conn.commit()
    conn.close()


def actualizar_empresa(id, data):
    conn = get_conn()
    conn.execute(
        'UPDATE empresas SET nombre_empresa=?, correo_destino=?, valor=?, dia_envio=?, concepto=?, activa=? WHERE id=?',
        (data['nombre_empresa'], data['correo_destino'], float(data['valor']),
         int(data['dia_envio']), data['concepto'], 1 if data.get('activa') else 0, id)
    )
    conn.commit()
    conn.close()


def eliminar_empresa(id):
    conn = get_conn()
    conn.execute('DELETE FROM empresas WHERE id=?', (id,))
    conn.commit()
    conn.close()


# ── Logs ───────────────────────────────────────────────────────────────────────

def registrar_envio(empresa_id, empresa_nombre, mes, anio, estado, error_msg=None):
    conn = get_conn()
    conn.execute(
        'INSERT INTO envios_log (empresa_id, empresa_nombre, fecha_envio, mes, anio, estado, error_msg) VALUES (?,?,?,?,?,?,?)',
        (empresa_id, empresa_nombre, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mes, anio, estado, error_msg)
    )
    conn.commit()
    conn.close()


def get_logs(limit=200):
    conn = get_conn()
    rows = conn.execute('SELECT * FROM envios_log ORDER BY fecha_envio DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_estadisticas():
    conn = get_conn()
    hoy = datetime.now()
    mes_str = hoy.strftime('%Y-%m')

    total = conn.execute('SELECT COUNT(*) FROM empresas WHERE activa=1').fetchone()[0]
    ok_mes = conn.execute(
        "SELECT COUNT(*) FROM envios_log WHERE fecha_envio LIKE ? AND estado='OK'",
        (f'{mes_str}%',)
    ).fetchone()[0]
    err_mes = conn.execute(
        "SELECT COUNT(*) FROM envios_log WHERE fecha_envio LIKE ? AND estado='ERROR'",
        (f'{mes_str}%',)
    ).fetchone()[0]

    dia_hoy = hoy.day
    proximos = conn.execute(
        '''SELECT nombre_empresa, dia_envio, valor FROM empresas WHERE activa=1
           ORDER BY CASE WHEN dia_envio >= ? THEN dia_envio - ? ELSE dia_envio + 31 - ? END
           LIMIT 5''',
        (dia_hoy, dia_hoy, dia_hoy)
    ).fetchall()

    conn.close()
    return {
        'total_empresas': total,
        'envios_ok_mes':  ok_mes,
        'envios_err_mes': err_mes,
        'proximos':       [dict(p) for p in proximos],
    }


# ── Config ─────────────────────────────────────────────────────────────────────

def get_config():
    conn = get_conn()
    rows = conn.execute('SELECT clave, valor FROM config').fetchall()
    conn.close()
    return {r['clave']: r['valor'] for r in rows}


def set_config(clave, valor):
    conn = get_conn()
    conn.execute('INSERT OR REPLACE INTO config (clave, valor) VALUES (?,?)', (clave, valor))
    conn.commit()
    conn.close()
