# 📊 BASE DE DATOS DE TIENDA - INVENTARIO, VENTAS Y COMPRAS

Una base de datos MySQL completa para gestionar un negocio de ventas con control de inventario.

## 🏗️ ESTRUCTURA DE TABLAS

```
├── categorias                 (Categorías de productos)
├── productos                  (Inventario)
├── proveedores               (Información de proveedores)
├── compras                   (Registro de compras)
├── detalle_compras           (Detalles de cada compra)
├── clientes                  (Base de datos de clientes)
├── ventas                    (Registro de ventas)
├── detalle_ventas            (Detalles de cada venta)
└── movimientos_inventario    (Auditoría de cambios en stock)
```

## 📋 DESCRIPCIÓN DE TABLAS

### 1. **CATEGORIAS**
Agrupa los productos por tipo
- `id_categoria` (PK)
- `nombre` - Nombre de la categoría
- `descripcion` - Descripción opcional

### 2. **PRODUCTOS** (Inventario)
Registro de todos los productos disponibles
- `id_producto` (PK)
- `nombre` - Nombre del producto
- `precio_unitario` - Precio de venta
- `cantidad_stock` - Units disponibles
- `cantidad_minima` - Stock mínimo recomendado
- `cantidad_maxima` - Stock máximo recomendado
- `estado` - Activo/Inactivo/Descontinuado

### 3. **PROVEEDORES**
Información de los proveedores
- `id_proveedor` (PK)
- `nombre` - Nombre del proveedor
- `contacto` - Persona de contacto
- `telefono` - Teléfono
- `email` - Email
- `ciudad`, `pais` - Ubicación

### 4. **COMPRAS**
Registro principal de compras a proveedores
- `id_compra` (PK)
- `id_proveedor` (FK)
- `fecha_compra` - Fecha de la compra
- `total_compra` - Monto total
- `estado_compra` - Pendiente/Recibida/Parcial/Cancelada

### 5. **DETALLE_COMPRAS**
Detalles de cada compra (qué se compró y cuánto)
- `id_detalle_compra` (PK)
- `id_compra` (FK)
- `id_producto` (FK)
- `cantidad` - Cantidad comprada
- `precio_unitario` - Precio de compra
- `subtotal` - Cantidad × Precio

### 6. **CLIENTES**
Base de datos de clientes
- `id_cliente` (PK)
- `nombre`, `apellido`
- `email`, `telefono`
- `tipo_cliente` - Regular/Mayorista/VIP
- `estado` - Activo/Inactivo

### 7. **VENTAS**
Registro principal de ventas a clientes
- `id_venta` (PK)
- `id_cliente` (FK)
- `fecha_venta` - Fecha de la venta
- `total_venta` - Monto total
- `impuesto` - IVA u otros impuestos
- `metodo_pago` - Efectivo/Tarjeta/Transferencia/Cheque
- `estado_venta` - Completada/Pendiente/Cancelada/Devolución

### 8. **DETALLE_VENTAS**
Detalles de cada venta (qué se vendió y cuánto)
- `id_detalle_venta` (PK)
- `id_venta` (FK)
- `id_producto` (FK)
- `cantidad` - Cantidad vendida
- `precio_unitario` - Precio de venta
- `descuento` - Descuento aplicado
- `subtotal` - Cantidad × Precio - Descuento

### 9. **MOVIMIENTOS_INVENTARIO**
Auditoría completa de cambios en el inventario
- `id_movimiento` (PK)
- `id_producto` (FK)
- `tipo_movimiento` - Entrada/Salida/Ajuste/Devolución
- `cantidad` - Cantidad del movimiento
- `stock_anterior` - Stock antes del cambio
- `stock_nuevo` - Stock después del cambio
- `fecha_movimiento` - Timestamp automático

## 🛠️ INSTALACIÓN Y SETUP

### Paso 1: Crear la Base de Datos

```bash
# Conectarse a MySQL
mysql -u root -p

# Ejecutar el script SQL
mysql -u root -p < base_datos_tienda.sql
```

O copiar y pegar el contenido de `base_datos_tienda.sql` en MySQL Workbench.

### Paso 2: Instalar Dependencias Python

```bash
pip install mysql-connector-python pandas
```

### Paso 3: Configurar la Conexión

En `gestor_tienda.py`, actualiza los parámetros de conexión:

```python
gestor = GestorTienda(
    host='localhost',
    user='root',
    password='tu_password',  # Cambiar si tienes contraseña
    database='tienda_db'
)
```

## 📖 EJEMPLOS DE USO

### Iniciando el Gestor

```python
from gestor_tienda import GestorTienda

# Conexión
gestor = GestorTienda()

# Ver reporte general
gestor.reporte_general()
```

### Obtener Productos

```python
# Obtener todos los productos activos
productos = gestor.obtener_productos()
print(productos)
```

### Crear una Venta

```python
# Items a vender
items = [
    {'id_producto': 1, 'cantidad': 2, 'descuento': 0},
    {'id_producto': 2, 'cantidad': 5, 'descuento': 10}
]

# Crear venta
id_venta = gestor.crear_venta(
    id_cliente=1,
    items=items,
    metodo_pago='Tarjeta',
    notas='Cliente VIP'
)
```

### Crear una Compra

```python
# Items a comprar
items = [
    {'id_producto': 1, 'cantidad': 10, 'precio_unitario': 850.00},
    {'id_producto': 3, 'cantidad': 20, 'precio_unitario': 72.00}
]

# Crear compra
id_compra = gestor.crear_compra(
    id_proveedor=1,
    items=items,
    notas='Compra de reposición'
)
```

### Actualizar Stock Manualmente

```python
# Registrar entrada de stock
gestor.actualizar_stock(
    id_producto=1,
    cantidad=5,
    tipo_movimiento='Entrada',
    referencia='COMPRA-001',
    razon='Compra a proveedor'
)

# Registrar salida (ajuste)
gestor.actualizar_stock(
    id_producto=2,
    cantidad=3,
    tipo_movimiento='Salida',
    referencia='VENTA-001',
    razon='Venta a cliente'
)
```

### Obtener Productos con Bajo Stock

```python
bajo_stock = gestor.productos_bajo_stock()
print(bajo_stock[['nombre', 'cantidad_stock', 'cantidad_minima']])
```

### Reporte de Ventas

```python
# Ventas en un período
ventas = gestor.ventas_por_periodo('2026-03-01', '2026-03-31')
print(ventas)

# Resumen por cliente
por_cliente = gestor.ventas_por_cliente()
print(por_cliente)

# Productos más vendidos
top = gestor.producto_mas_vendido(limite=5)
print(top)
```

### Reporte de Compras

```python
# Resumen de compras por proveedor
por_proveedor = gestor.compras_por_proveedor()
print(por_proveedor)
```

## 🔍 VISTAS DISPONIBLES

La base de datos incluye 3 vistas SQL útiles:

### 1. `v_ventas_por_cliente`
```sql
SELECT * FROM v_ventas_por_cliente;
```
Muestra: Total de transacciones, monto total y ticket promedio por cliente

### 2. `v_productos_bajo_stock`
```sql
SELECT * FROM v_productos_bajo_stock;
```
Muestra: Productos con stock por debajo del mínimo y valor de compra recomendado

### 3. `v_compras_por_proveedor`
```sql
SELECT * FROM v_compras_por_proveedor;
```
Muestra: Total de compras, monto total y promedio por proveedor

## 📊 CONSULTAS SQL ÚTILES

### Ventas del mes actual

```sql
SELECT 
    v.id_venta, 
    CONCAT(c.nombre, ' ', c.apellido) as cliente,
    v.fecha_venta,
    v.total_venta,
    v.metodo_pago
FROM ventas v
JOIN clientes c ON v.id_cliente = c.id_cliente
WHERE MONTH(v.fecha_venta) = MONTH(CURDATE())
ORDER BY v.fecha_venta DESC;
```

### Productos más vendidos

```sql
SELECT 
    p.nombre,
    SUM(dv.cantidad) as total_vendido,
    SUM(dv.subtotal) as monto_total,
    COUNT(DISTINCT v.id_venta) as num_transacciones
FROM detalle_ventas dv
JOIN productos p ON dv.id_producto = p.id_producto
JOIN ventas v ON dv.id_venta = v.id_venta
GROUP BY p.id_producto, p.nombre
ORDER BY total_vendido DESC;
```

### Ganancia por producto

```sql
SELECT 
    p.nombre,
    p.precio_unitario as precio_venta,
    IFNULL(AVG(dc.precio_unitario), 0) as precio_compra_promedio,
    ROUND(p.precio_unitario - IFNULL(AVG(dc.precio_unitario), 0), 2) as ganancia_unitaria,
    SUM(dv.cantidad) as unidades_vendidas
FROM productos p
LEFT JOIN detalle_ventas dv ON p.id_producto = dv.id_producto
LEFT JOIN detalle_compras dc ON p.id_producto = dc.id_producto
GROUP BY p.id_producto, p.nombre;
```

### Inventario valorizado

```sql
SELECT 
    c.nombre as categoria,
    COUNT(p.id_producto) as num_productos,
    SUM(p.cantidad_stock) as total_unidades,
    ROUND(SUM(p.cantidad_stock * p.precio_unitario), 2) as valor_total
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria
WHERE p.estado = 'Activo'
GROUP BY c.id_categoria, c.nombre
ORDER BY valor_total DESC;
```

## 🔐 RELACIONES Y RESTRICCIONES

- **Integridad referencial**: Las claves foráneas previenen datos inconsistentes
- **Eliminación en cascada**: Al eliminar una venta, se eliminan sus detalles
- **Valores no nulos**: Campos críticos como nombre, cantidad y precio son obligatorios
- **Valores únicos**: Email de cliente, nombre de categoría y nombre de proveedor son únicos (evita duplicadas)

## 🎯 CASOS DE USO

1. **Gestión de Inventario**
   - Ver stock actual
   - Alertas de bajo stock
   - Auditar cambios de inventario

2. **Gestión de Ventas**
   - Registrar ventas
   - Aplicar descuentos
   - Análisis de productos más vendidos

3. **Gestión de Compras**
   - Registrar compras a proveedores
   - Actualizar stock automáticamente
   - Análisis de proveedores

4. **Reportes y Análisis**
   - KPI's de ventas
   - Rentabilidad por producto
   - Comportamiento de clientes
   - Análisis de proveedores

## 🚀 PRÓXIMAS MEJORAS

- [ ] Aplicación web con Flask/Django
- [ ] Dashboard en Power BI
- [ ] Automatización de órdenes de compra
- [ ] Sistema de alertas de stock
- [ ] Integración con sistemas de pago
- [ ] Reportes automáticos por email

## 📞 SOPORTE

Para más información o errores:
1. Verificar conexión MySQL
2. Asegurar que la base de datos está creada
3. Verificar permisos de usuario MySQL
4. Revisar logs de error en consola

---

**Última actualización:** Marzo 2026
**Versión:** 1.0
