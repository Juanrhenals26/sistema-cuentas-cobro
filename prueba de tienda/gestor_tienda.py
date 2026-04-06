"""
GESTOR DE BASE DE DATOS DE TIENDA
=====================================
Script para gestionar la base de datos MySQL de inventario, ventas y compras
Incluye funciones para:
- Conexión a la base de datos
- Consultas comunes
- Reportes
- Gestión de inventario
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import json

class GestorTienda:
    """Clase para gestionar la base de datos de la tienda"""
    
    def __init__(self, host='localhost', user='root', password='', database='tienda_db'):
        """Inicializa la conexión a la base de datos"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None
        self.conectar()
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Conexión exitosa a {self.database}")
        except Error as e:
            print(f"✗ Error al conectar: {e}")
            return False
        return True
    
    def ejecutar_query(self, query, params=None, fetch=False):
        """Ejecuta una consulta a la base de datos"""
        if not self.conexion:
            print("No hay conexión activa")
            return None
        
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                resultado = cursor.fetchall()
            else:
                self.conexion.commit()
                resultado = cursor.rowcount
            
            cursor.close()
            return resultado
        except Error as e:
            print(f"✗ Error en query: {e}")
            return None
    
    # ============================================================
    # FUNCIONES DE INVENTARIO
    # ============================================================
    
    def obtener_productos(self, filtro_activos=True):
        """Obtiene lista de productos"""
        query = """
        SELECT p.id_producto, p.nombre, p.descripcion, c.nombre as categoria,
               p.precio_unitario, p.cantidad_stock, p.cantidad_minima, p.estado
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        """
        if filtro_activos:
            query += "WHERE p.estado = 'Activo'"
        query += "ORDER BY p.nombre"
        
        return pd.DataFrame(self.ejecutar_query(query, fetch=True))
    
    def actualizar_stock(self, id_producto, cantidad, tipo_movimiento, referencia='', razon=''):
        """Actualiza el stock de un producto"""
        try:
            cursor = self.conexion.cursor()
            
            # Obtener stock actual
            query_stock = "SELECT cantidad_stock FROM productos WHERE id_producto = %s"
            cursor.execute(query_stock, (id_producto,))
            resultado = cursor.fetchone()
            
            if not resultado:
                print("Producto no encontrado")
                return False
            
            stock_anterior = resultado[0]
            
            # Calcular nuevo stock según tipo de movimiento
            if tipo_movimiento == 'Entrada':
                stock_nuevo = stock_anterior + cantidad
            elif tipo_movimiento == 'Salida':
                stock_nuevo = stock_anterior - cantidad
            elif tipo_movimiento == 'Ajuste':
                stock_nuevo = cantidad
            else:
                print("Tipo de movimiento inválido")
                return False
            
            # Validar que no sea negativo
            if stock_nuevo < 0:
                print("Error: Stock insuficiente")
                return False
            
            # Actualizar stock
            query_update = "UPDATE productos SET cantidad_stock = %s WHERE id_producto = %s"
            cursor.execute(query_update, (stock_nuevo, id_producto))
            
            # Registrar movimiento
            query_movimiento = """
            INSERT INTO movimientos_inventario 
            (id_producto, tipo_movimiento, cantidad, referencia, razon, stock_anterior, stock_nuevo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_movimiento, (id_producto, tipo_movimiento, cantidad, 
                                             referencia, razon, stock_anterior, stock_nuevo))
            
            self.conexion.commit()
            cursor.close()
            print(f"✓ Stock actualizado: {stock_anterior} → {stock_nuevo}")
            return True
        
        except Error as e:
            print(f"✗ Error al actualizar stock: {e}")
            return False
    
    def productos_bajo_stock(self):
        """Obtiene productos con stock bajo"""
        query = "SELECT * FROM v_productos_bajo_stock"
        return pd.DataFrame(self.ejecutar_query(query, fetch=True))
    
    # ============================================================
    # FUNCIONES DE VENTAS
    # ============================================================
    
    def crear_venta(self, id_cliente, items, metodo_pago='Efectivo', notas=''):
        """
        Crea una venta completa
        items: lista de dicts {'id_producto': X, 'cantidad': Y, 'descuento': Z}
        """
        try:
            cursor = self.conexion.cursor()
            
            # Calcular total
            total_venta = 0
            for item in items:
                query = "SELECT precio_unitario FROM productos WHERE id_producto = %s"
                cursor.execute(query, (item['id_producto'],))
                resultado = cursor.fetchone()
                
                if not resultado:
                    print(f"Producto {item['id_producto']} no encontrado")
                    return False
                
                precio = resultado[0]
                total_venta += precio * item['cantidad']
            
            impuesto = total_venta * 0.1  # 10% de impuesto
            
            # Crear venta
            query_venta = """
            INSERT INTO ventas (id_cliente, fecha_venta, total_venta, impuesto, metodo_pago, notas)
            VALUES (%s, CURDATE(), %s, %s, %s, %s)
            """
            cursor.execute(query_venta, (id_cliente, total_venta, impuesto, metodo_pago, notas))
            id_venta = cursor.lastrowid
            
            # Añadir detalles de venta y actualizar stock
            for item in items:
                query_precio = "SELECT precio_unitario FROM productos WHERE id_producto = %s"
                cursor.execute(query_precio, (item['id_producto'],))
                precio = cursor.fetchone()[0]
                
                descuento = item.get('descuento', 0)
                subtotal = (precio * item['cantidad']) - descuento
                
                query_detalle = """
                INSERT INTO detalle_ventas 
                (id_venta, id_producto, cantidad, precio_unitario, descuento, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_detalle, (id_venta, item['id_producto'], 
                                              item['cantidad'], precio, descuento, subtotal))
                
                # Actualizar stock
                cursor.execute("SELECT cantidad_stock FROM productos WHERE id_producto = %s",
                              (item['id_producto'],))
                stock_actual = cursor.fetchone()[0]
                nuevo_stock = stock_actual - item['cantidad']
                
                if nuevo_stock < 0:
                    self.conexion.rollback()
                    print(f"Error: Stock insuficiente para producto {item['id_producto']}")
                    return False
                
                cursor.execute("UPDATE productos SET cantidad_stock = %s WHERE id_producto = %s",
                              (nuevo_stock, item['id_producto']))
            
            self.conexion.commit()
            cursor.close()
            print(f"✓ Venta #{id_venta} creada exitosamente")
            return id_venta
        
        except Error as e:
            self.conexion.rollback()
            print(f"✗ Error al crear venta: {e}")
            return False
    
    def ventas_por_cliente(self):
        """Obtiene resumen de ventas por cliente"""
        query = "SELECT * FROM v_ventas_por_cliente"
        return pd.DataFrame(self.ejecutar_query(query, fetch=True))
    
    def ventas_por_periodo(self, fecha_inicio, fecha_fin):
        """Obtiene ventas dentro de un período"""
        query = """
        SELECT v.id_venta, CONCAT(c.nombre, ' ', c.apellido) AS cliente,
               v.fecha_venta, v.total_venta, v.metodo_pago, v.estado_venta
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE v.fecha_venta BETWEEN %s AND %s
        ORDER BY v.fecha_venta DESC
        """
        return pd.DataFrame(self.ejecutar_query(query, (fecha_inicio, fecha_fin), fetch=True))
    
    # ============================================================
    # FUNCIONES DE COMPRAS
    # ============================================================
    
    def crear_compra(self, id_proveedor, items, fecha_compra=None, notas=''):
        """
        Crea una compra
        items: lista de dicts {'id_producto': X, 'cantidad': Y, 'precio_unitario': Z}
        """
        try:
            cursor = self.conexion.cursor()
            
            if fecha_compra is None:
                fecha_compra = datetime.now().strftime('%Y-%m-%d')
            
            # Calcular total
            total_compra = sum(item['cantidad'] * item['precio_unitario'] for item in items)
            
            # Crear compra
            query_compra = """
            INSERT INTO compras (id_proveedor, fecha_compra, total_compra, notas)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_compra, (id_proveedor, fecha_compra, total_compra, notas))
            id_compra = cursor.lastrowid
            
            # Añadir detalles de compra
            for item in items:
                subtotal = item['cantidad'] * item['precio_unitario']
                query_detalle = """
                INSERT INTO detalle_compras 
                (id_compra, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_detalle, (id_compra, item['id_producto'], 
                                              item['cantidad'], item['precio_unitario'], subtotal))
            
            self.conexion.commit()
            cursor.close()
            print(f"✓ Compra #{id_compra} creada exitosamente")
            return id_compra
        
        except Error as e:
            self.conexion.rollback()
            print(f"✗ Error al crear compra: {e}")
            return False
    
    def compras_por_proveedor(self):
        """Obtiene resumen de compras por proveedor"""
        query = "SELECT * FROM v_compras_por_proveedor"
        return pd.DataFrame(self.ejecutar_query(query, fetch=True))
    
    # ============================================================
    # REPORTES Y ANÁLISIS
    # ============================================================
    
    def reporte_general(self):
        """Genera un reporte general del negocio"""
        print("\n" + "="*60)
        print("REPORTE GENERAL DE LA TIENDA")
        print("="*60)
        
        # Total de productos
        query = "SELECT COUNT(*) as total FROM productos WHERE estado='Activo'"
        total_productos = self.ejecutar_query(query, fetch=True)[0]['total']
        print(f"\n📦 PRODUCTOS: {total_productos} activos")
        
        # Valor total del inventario
        query = """
        SELECT ROUND(SUM(cantidad_stock * precio_unitario), 2) as valor_inventario
        FROM productos WHERE estado='Activo'
        """
        valor_inv = self.ejecutar_query(query, fetch=True)[0]['valor_inventario'] or 0
        print(f"💰 Valor de inventario: ${valor_inv:,.2f}")
        
        # Total de ventas este mes
        query = """
        SELECT ROUND(SUM(total_venta), 2) as total_ventas
        FROM ventas
        WHERE MONTH(fecha_venta) = MONTH(CURDATE()) 
        AND YEAR(fecha_venta) = YEAR(CURDATE())
        """
        total_ventas = self.ejecutar_query(query, fetch=True)[0]['total_ventas'] or 0
        print(f"📈 Ventas este mes: ${total_ventas:,.2f}")
        
        # Total de compras este mes
        query = """
        SELECT ROUND(SUM(total_compra), 2) as total_compras
        FROM compras
        WHERE MONTH(fecha_compra) = MONTH(CURDATE())
        AND YEAR(fecha_compra) = YEAR(CURDATE())
        """
        total_compras = self.ejecutar_query(query, fetch=True)[0]['total_compras'] or 0
        print(f"🛒 Compras este mes: ${total_compras:,.2f}")
        
        # Productos con bajo stock
        bajo_stock = len(self.productos_bajo_stock())
        print(f"⚠️  Productos con bajo stock: {bajo_stock}")
        
        print("\n" + "="*60 + "\n")
    
    def producto_mas_vendido(self, limite=5):
        """Obtiene los productos más vendidos"""
        query = """
        SELECT p.id_producto, p.nombre, SUM(dv.cantidad) as total_vendido,
               SUM(dv.subtotal) as monto_total
        FROM detalle_ventas dv
        JOIN productos p ON dv.id_producto = p.id_producto
        GROUP BY p.id_producto, p.nombre
        ORDER BY total_vendido DESC
        LIMIT %s
        """
        return pd.DataFrame(self.ejecutar_query(query, (limite,), fetch=True))
    
    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada")


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("SISTEMA DE GESTIÓN DE TIENDA")
    print("="*60)
    
    # Inicializar el gestor
    # NOTA: Cambiar los parámetros según tu configuración de MySQL
    gestor = GestorTienda(
        host='localhost',
        user='root',
        password='',  # Cambiar si tienes contraseña
        database='tienda_db'
    )
    
    # Mostrar reporte general
    gestor.reporte_general()
    
    # Obtener productos
    print("📋 PRODUCTOS DISPONIBLES:")
    print(gestor.obtener_productos().to_string(index=False))
    
    # Productos con bajo stock
    print("\n⚠️  PRODUCTOS CON BAJO STOCK:")
    bajo = gestor.productos_bajo_stock()
    if not bajo.empty:
        print(bajo.to_string(index=False))
    else:
        print("✓ Todos los productos tienen stock adecuado")
    
    # Productos más vendidos
    print("\n🏆 PRODUCTOS MÁS VENDIDOS:")
    print(gestor.producto_mas_vendido().to_string(index=False))
    
    # Ventas por cliente
    print("\n👤 RESUMEN DE VENTAS POR CLIENTE:")
    print(gestor.ventas_por_cliente().to_string(index=False))
    
    # Compras por proveedor
    print("\n🤝 RESUMEN DE COMPRAS POR PROVEEDOR:")
    print(gestor.compras_por_proveedor().to_string(index=False))
    
    # Cerrar conexión
    gestor.cerrar_conexion()
    
    print("\n✓ Sistema de gestión listo para usar")
