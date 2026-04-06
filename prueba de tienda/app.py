"""
APLICACIÓN FLASK - GESTOR DE TIENDA
====================================
Interfaz web para gestionar inventario, ventas y compras
Con CRUDs completos (Create, Read, Update, Delete)
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import json

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tienda_secreta_2026'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambiar si tienes contraseña
app.config['MYSQL_DB'] = 'tienda_db'

mysql = MySQL(app)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_conexion():
    """Obtiene el cursor de la base de datos"""
    cur = mysql.get_db().cursor(MySQLdb.cursors.DictCursor)
    return cur

def guardar_cambios():
    """Guarda los cambios en la base de datos"""
    mysql.get_db().commit()

# ============================================================
# RUTAS PRINCIPALES
# ============================================================

@app.route('/')
def index():
    """Página principal con resumen"""
    try:
        cur = obtener_conexion()
        
        # Obtener estadísticas
        cur.execute("SELECT COUNT(*) as total FROM productos WHERE estado='Activo'")
        total_productos = cur.fetchone()['total']
        
        cur.execute("SELECT COUNT(*) as total FROM clientes WHERE estado='Activo'")
        total_clientes = cur.fetchone()['total']
        
        cur.execute("""
            SELECT ROUND(SUM(total_venta), 2) as total 
            FROM ventas 
            WHERE DATE(fecha_venta) = CURDATE()
        """)
        ventas_hoy = cur.fetchone()['total'] or 0
        
        cur.execute("SELECT COUNT(*) as total FROM productos WHERE cantidad_stock < cantidad_minima")
        productos_bajo_stock = cur.fetchone()['total']
        
        cur.execute("SELECT ROUND(SUM(cantidad_stock * precio_unitario), 2) as total FROM productos")
        valor_inventario = cur.fetchone()['total'] or 0
        
        estadisticas = {
            'total_productos': total_productos,
            'total_clientes': total_clientes,
            'ventas_hoy': ventas_hoy,
            'productos_bajo_stock': productos_bajo_stock,
            'valor_inventario': valor_inventario
        }
        
        return render_template('index.html', stats=estadisticas)
    except Exception as e:
        print(f"Error en index: {e}")
        return render_template('index.html', stats={})

# ============================================================
# CRUD PRODUCTOS
# ============================================================

@app.route('/productos')
def productos():
    """Listado de productos"""
    try:
        cur = obtener_conexion()
        cur.execute("""
            SELECT p.*, c.nombre as categoria_nombre 
            FROM productos p 
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            ORDER BY p.nombre
        """)
        productos_list = cur.fetchall()
        return render_template('productos.html', productos=productos_list)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/productos/new', methods=['GET', 'POST'])
def nuevo_producto():
    """Crear nuevo producto"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT * FROM categorias ORDER BY nombre")
            categorias = cur.fetchall()
            return render_template('form_producto.html', categorias=categorias, producto=None)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('productos'))
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            id_categoria = request.form['id_categoria']
            precio = request.form['precio_unitario']
            stock = request.form['cantidad_stock']
            minimo = request.form['cantidad_minima']
            maximo = request.form['cantidad_maxima']
            
            cur = obtener_conexion()
            cur.execute("""
                INSERT INTO productos 
                (nombre, descripcion, id_categoria, precio_unitario, cantidad_stock, cantidad_minima, cantidad_maxima)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, descripcion, id_categoria, precio, stock, minimo, maximo))
            guardar_cambios()
            
            flash("Producto creado exitosamente", "success")
            return redirect(url_for('productos'))
        except Exception as e:
            flash(f"Error al crear: {e}", "danger")
            return redirect(url_for('nuevo_producto'))

@app.route('/productos/edit/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    """Editar producto"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
            producto = cur.fetchone()
            cur.execute("SELECT * FROM categorias ORDER BY nombre")
            categorias = cur.fetchall()
            return render_template('form_producto.html', producto=producto, categorias=categorias)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('productos'))
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            id_categoria = request.form['id_categoria']
            precio = request.form['precio_unitario']
            stock = request.form['cantidad_stock']
            minimo = request.form['cantidad_minima']
            maximo = request.form['cantidad_maxima']
            
            cur = obtener_conexion()
            cur.execute("""
                UPDATE productos 
                SET nombre=%s, descripcion=%s, id_categoria=%s, precio_unitario=%s,
                    cantidad_stock=%s, cantidad_minima=%s, cantidad_maxima=%s
                WHERE id_producto=%s
            """, (nombre, descripcion, id_categoria, precio, stock, minimo, maximo, id))
            guardar_cambios()
            
            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for('productos'))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")
            return redirect(url_for('editar_producto', id=id))

@app.route('/productos/delete/<int:id>')
def eliminar_producto(id):
    """Eliminar producto"""
    try:
        cur = obtener_conexion()
        cur.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
        guardar_cambios()
        flash("Producto eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('productos'))

# ============================================================
# CRUD CLIENTES
# ============================================================

@app.route('/clientes')
def clientes():
    """Listado de clientes"""
    try:
        cur = obtener_conexion()
        cur.execute("SELECT * FROM clientes ORDER BY nombre")
        clientes_list = cur.fetchall()
        return render_template('clientes.html', clientes=clientes_list)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/clientes/new', methods=['GET', 'POST'])
def nuevo_cliente():
    """Crear nuevo cliente"""
    if request.method == 'GET':
        return render_template('form_cliente.html', cliente=None)
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            pais = request.form['pais']
            tipo = request.form['tipo_cliente']
            
            cur = obtener_conexion()
            cur.execute("""
                INSERT INTO clientes 
                (nombre, apellido, email, telefono, direccion, ciudad, pais, tipo_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, email, telefono, direccion, ciudad, pais, tipo))
            guardar_cambios()
            
            flash("Cliente creado exitosamente", "success")
            return redirect(url_for('clientes'))
        except Exception as e:
            flash(f"Error al crear: {e}", "danger")
            return redirect(url_for('nuevo_cliente'))

@app.route('/clientes/edit/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    """Editar cliente"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
            cliente = cur.fetchone()
            return render_template('form_cliente.html', cliente=cliente)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('clientes'))
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            pais = request.form['pais']
            tipo = request.form['tipo_cliente']
            
            cur = obtener_conexion()
            cur.execute("""
                UPDATE clientes 
                SET nombre=%s, apellido=%s, email=%s, telefono=%s, direccion=%s, ciudad=%s, pais=%s, tipo_cliente=%s
                WHERE id_cliente=%s
            """, (nombre, apellido, email, telefono, direccion, ciudad, pais, tipo, id))
            guardar_cambios()
            
            flash("Cliente actualizado exitosamente", "success")
            return redirect(url_for('clientes'))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")
            return redirect(url_for('editar_cliente', id=id))

@app.route('/clientes/delete/<int:id>')
def eliminar_cliente(id):
    """Eliminar cliente"""
    try:
        cur = obtener_conexion()
        cur.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
        guardar_cambios()
        flash("Cliente eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('clientes'))

# ============================================================
# CRUD PROVEEDORES
# ============================================================

@app.route('/proveedores')
def proveedores():
    """Listado de proveedores"""
    try:
        cur = obtener_conexion()
        cur.execute("SELECT * FROM proveedores ORDER BY nombre")
        proveedores_list = cur.fetchall()
        return render_template('proveedores.html', proveedores=proveedores_list)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/proveedores/new', methods=['GET', 'POST'])
def nuevo_proveedor():
    """Crear nuevo proveedor"""
    if request.method == 'GET':
        return render_template('form_proveedor.html', proveedor=None)
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            contacto = request.form['contacto']
            telefono = request.form['telefono']
            email = request.form['email']
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            pais = request.form['pais']
            
            cur = obtener_conexion()
            cur.execute("""
                INSERT INTO proveedores 
                (nombre, contacto, telefono, email, direccion, ciudad, pais)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, contacto, telefono, email, direccion, ciudad, pais))
            guardar_cambios()
            
            flash("Proveedor creado exitosamente", "success")
            return redirect(url_for('proveedores'))
        except Exception as e:
            flash(f"Error al crear: {e}", "danger")
            return redirect(url_for('nuevo_proveedor'))

@app.route('/proveedores/edit/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    """Editar proveedor"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT * FROM proveedores WHERE id_proveedor = %s", (id,))
            proveedor = cur.fetchone()
            return render_template('form_proveedor.html', proveedor=proveedor)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('proveedores'))
    
    else:  # POST
        try:
            nombre = request.form['nombre']
            contacto = request.form['contacto']
            telefono = request.form['telefono']
            email = request.form['email']
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            pais = request.form['pais']
            
            cur = obtener_conexion()
            cur.execute("""
                UPDATE proveedores 
                SET nombre=%s, contacto=%s, telefono=%s, email=%s, direccion=%s, ciudad=%s, pais=%s
                WHERE id_proveedor=%s
            """, (nombre, contacto, telefono, email, direccion, ciudad, pais, id))
            guardar_cambios()
            
            flash("Proveedor actualizado exitosamente", "success")
            return redirect(url_for('proveedores'))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")
            return redirect(url_for('editar_proveedor', id=id))

@app.route('/proveedores/delete/<int:id>')
def eliminar_proveedor(id):
    """Eliminar proveedor"""
    try:
        cur = obtener_conexion()
        cur.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id,))
        guardar_cambios()
        flash("Proveedor eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('proveedores'))

# ============================================================
# CRUD VENTAS
# ============================================================

@app.route('/ventas')
def ventas():
    """Listado de ventas"""
    try:
        cur = obtener_conexion()
        cur.execute("""
            SELECT v.*, CONCAT(c.nombre, ' ', c.apellido) as cliente_nombre
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha_venta DESC LIMIT 100
        """)
        ventas_list = cur.fetchall()
        return render_template('ventas.html', ventas=ventas_list)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/ventas/new', methods=['GET', 'POST'])
def nueva_venta():
    """Crear nueva venta"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT id_cliente, CONCAT(nombre, ' ', apellido) as nombre FROM clientes WHERE estado='Activo'")
            clientes_list = cur.fetchall()
            cur.execute("SELECT id_producto, nombre, precio_unitario, cantidad_stock FROM productos WHERE estado='Activo'")
            productos_list = cur.fetchall()
            return render_template('form_venta.html', clientes=clientes_list, productos=productos_list, venta=None)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('ventas'))
    
    else:  # POST
        try:
            id_cliente = request.form['id_cliente']
            metodo_pago = request.form.get('metodo_pago', 'Efectivo')
            notas = request.form.get('notas', '')
            
            # Parsear items
            items_json = request.form['items']
            items = json.loads(items_json)
            
            # Calcular total
            total_venta = sum(item['cantidad'] * item['precio'] for item in items)
            impuesto = total_venta * 0.1
            
            cur = obtener_conexion()
            
            # Crear venta
            cur.execute("""
                INSERT INTO ventas (id_cliente, fecha_venta, total_venta, impuesto, metodo_pago, notas)
                VALUES (%s, CURDATE(), %s, %s, %s, %s)
            """, (id_cliente, total_venta, impuesto, metodo_pago, notas))
            
            id_venta = cur.lastrowid
            
            # Añadir detalles y actualizar stock
            for item in items:
                subtotal = item['cantidad'] * item['precio']
                cur.execute("""
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_venta, item['id_producto'], item['cantidad'], item['precio'], subtotal))
                
                # Actualizar stock
                cur.execute("""
                    UPDATE productos 
                    SET cantidad_stock = cantidad_stock - %s
                    WHERE id_producto = %s
                """, (item['cantidad'], item['id_producto']))
            
            guardar_cambios()
            flash("Venta creada exitosamente", "success")
            return redirect(url_for('ventas'))
        except Exception as e:
            flash(f"Error al crear: {e}", "danger")
            return redirect(url_for('nueva_venta'))

@app.route('/ventas/delete/<int:id>')
def eliminar_venta(id):
    """Eliminar venta"""
    try:
        cur = obtener_conexion()
        
        # Obtener detalles de la venta para reversar el stock
        cur.execute("SELECT id_producto, cantidad FROM detalle_ventas WHERE id_venta = %s", (id,))
        detalles = cur.fetchall()
        
        for detalle in detalles:
            cur.execute("""
                UPDATE productos 
                SET cantidad_stock = cantidad_stock + %s
                WHERE id_producto = %s
            """, (detalle['cantidad'], detalle['id_producto']))
        
        # Eliminar detalles y venta
        cur.execute("DELETE FROM detalle_ventas WHERE id_venta = %s", (id,))
        cur.execute("DELETE FROM ventas WHERE id_venta = %s", (id,))
        guardar_cambios()
        
        flash("Venta eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('ventas'))

# ============================================================
# CRUD COMPRAS
# ============================================================

@app.route('/compras')
def compras():
    """Listado de compras"""
    try:
        cur = obtener_conexion()
        cur.execute("""
            SELECT c.*, p.nombre as proveedor_nombre
            FROM compras c
            LEFT JOIN proveedores p ON c.id_proveedor = p.id_proveedor
            ORDER BY c.fecha_compra DESC LIMIT 100
        """)
        compras_list = cur.fetchall()
        return render_template('compras.html', compras=compras_list)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/compras/new', methods=['GET', 'POST'])
def nueva_compra():
    """Crear nueva compra"""
    if request.method == 'GET':
        try:
            cur = obtener_conexion()
            cur.execute("SELECT id_proveedor, nombre FROM proveedores WHERE estado='Activo'")
            proveedores_list = cur.fetchall()
            cur.execute("SELECT id_producto, nombre FROM productos WHERE estado='Activo'")
            productos_list = cur.fetchall()
            return render_template('form_compra.html', proveedores=proveedores_list, productos=productos_list, compra=None)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('compras'))
    
    else:  # POST
        try:
            id_proveedor = request.form['id_proveedor']
            notas = request.form.get('notas', '')
            
            # Parsear items
            items_json = request.form['items']
            items = json.loads(items_json)
            
            # Calcular total
            total_compra = sum(item['cantidad'] * item['precio'] for item in items)
            
            cur = obtener_conexion()
            
            # Crear compra
            cur.execute("""
                INSERT INTO compras (id_proveedor, fecha_compra, total_compra, notas)
                VALUES (%s, CURDATE(), %s, %s)
            """, (id_proveedor, total_compra, notas))
            
            id_compra = cur.lastrowid
            
            # Añadir detalles
            for item in items:
                subtotal = item['cantidad'] * item['precio']
                cur.execute("""
                    INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_compra, item['id_producto'], item['cantidad'], item['precio'], subtotal))
            
            guardar_cambios()
            flash("Compra creada exitosamente", "success")
            return redirect(url_for('compras'))
        except Exception as e:
            flash(f"Error al crear: {e}", "danger")
            return redirect(url_for('nueva_compra'))

@app.route('/compras/delete/<int:id>')
def eliminar_compra(id):
    """Eliminar compra"""
    try:
        cur = obtener_conexion()
        cur.execute("DELETE FROM detalle_compras WHERE id_compra = %s", (id,))
        cur.execute("DELETE FROM compras WHERE id_compra = %s", (id,))
        guardar_cambios()
        flash("Compra eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for('compras'))

# ============================================================
# MANEJO DE ERRORES
# ============================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_servidor(e):
    return render_template('500.html'), 500

# ============================================================
# EJECUTAR APLICACIÓN
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SERVIDOR INICIADO")
    print("="*60)
    print("📍 Acceder en: http://localhost:5000")
    print("👥 Interfaz de Gestión de Tienda")
    print("="*60 + "\n")
    app.run(debug=True, host='localhost', port=5000)
