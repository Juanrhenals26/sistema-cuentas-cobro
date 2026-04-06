"""
app.py — Servidor web Flask para el Sistema de Cuentas de Cobro
Ejecutar: python app.py  → abre http://localhost:5000
"""
import sys
import os

# Agregar cuentas_cobro al path
CUENTAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cuentas_cobro')
sys.path.insert(0, CUENTAS_DIR)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import database as db
import scheduler as sched

app = Flask(__name__)
app.secret_key = 'cuentas-cobro-2026-secreto'

# Inicializar BD y scheduler al arrancar
db.init_db()
_scheduler = sched.iniciar_scheduler()

MESES_ES = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}


@app.context_processor
def inject_globals():
    return {'now': datetime.now(), 'meses': MESES_ES}


# ── Rutas principales ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    empresas = db.get_todas_empresas()
    stats    = db.get_estadisticas()
    hoy      = datetime.now()
    logs_recientes = db.get_logs(5)
    return render_template('index.html',
                           empresas=empresas, stats=stats,
                           hoy=hoy, logs_recientes=logs_recientes)


@app.route('/empresa/nueva', methods=['GET', 'POST'])
def nueva_empresa():
    if request.method == 'POST':
        db.crear_empresa(request.form)
        flash('✅ Empresa agregada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('empresa_form.html', empresa=None, titulo='Nueva Empresa')


@app.route('/empresa/<int:id>/editar', methods=['GET', 'POST'])
def editar_empresa(id):
    empresa = db.get_empresa(id)
    if not empresa:
        flash('Empresa no encontrada.', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        db.actualizar_empresa(id, request.form)
        flash('✅ Empresa actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('empresa_form.html', empresa=empresa, titulo='Editar Empresa')


@app.route('/empresa/<int:id>/eliminar', methods=['POST'])
def eliminar_empresa(id):
    empresa = db.get_empresa(id)
    nombre = empresa['nombre_empresa'] if empresa else ''
    db.eliminar_empresa(id)
    flash(f'🗑️ Empresa "{nombre}" eliminada.', 'info')
    return redirect(url_for('index'))


@app.route('/empresa/<int:id>/enviar', methods=['POST'])
def enviar_ahora(id):
    """Enviar cuenta de cobro de inmediato (botón manual)."""
    empresa = db.get_empresa(id)
    if not empresa:
        return jsonify({'ok': False, 'msg': 'Empresa no encontrada'})
    exito, msg = sched.procesar_empresa(empresa)
    return jsonify({'ok': exito, 'msg': msg})


@app.route('/scheduler/ejecutar', methods=['POST'])
def ejecutar_scheduler():
    """Forzar la revisión del día (envía todas las del día de hoy)."""
    sched.job_diario()
    flash('⚡ Revisión ejecutada manualmente. Revisa los logs.', 'info')
    return redirect(url_for('logs'))


@app.route('/logs')
def logs():
    registros = db.get_logs(200)
    return render_template('logs.html', logs=registros)


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        for campo in ['email_remitente', 'email_clave', 'hora_envio',
                      'minuto_envio', 'smtp_servidor', 'smtp_puerto']:
            if campo in request.form:
                db.set_config(campo, request.form[campo])
        flash('✅ Configuración guardada correctamente.', 'success')
        return redirect(url_for('config'))
    cfg = db.get_config()
    return render_template('config.html', cfg=cfg)


@app.route('/api/empresas')
def api_empresas():
    return jsonify(db.get_todas_empresas())


@app.route('/api/stats')
def api_stats():
    return jsonify(db.get_estadisticas())


if __name__ == '__main__':
    print("\n" + "="*55)
    print("  🚀 Sistema de Cuentas de Cobro — Iniciando...")
    print("="*55)
    print("  URL: http://localhost:5000")
    print("  Presiona Ctrl+C para detener")
    print("="*55 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
