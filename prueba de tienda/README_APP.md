# 🚀 APLICACIÓN WEB - GESTOR DE TIENDA

Una interfaz web completa para gestionar inventario, ventas y compras con CRUDs (Create, Read, Update, Delete) implementados.

## 📋 Funcionalidades

### ✅ Gestión de Productos (CRUD completo)
- Crear nuevos productos
- Ver listado de productos
- Editar información de productos
- Eliminar productos
- Alertas de bajo stock
- Control de stock mínimo y máximo

### ✅ Gestión de Clientes (CRUD completo)
- Crear nuevos clientes
- Ver listado de clientes
- Editar datos de clientes
- Eliminar clientes
- Clasificación por tipo (Regular, Mayorista, VIP)

### ✅ Gestión de Proveedores (CRUD completo)
- Crear nuevos proveedores
- Ver listado de proveedores
- Editar información de proveedores
- Eliminar proveedores

### ✅ Registro de Ventas
- Crear nuevas ventas
- Agregar múltiples productos por venta
- Calcular totales automáticamente
- Aplicar descuentos
- Actualizar stock automáticamente
- Ver historial de ventas
- Métodos de pago (Efectivo, Tarjeta, Transferencia, Cheque)

### ✅ Registro de Compras
- Crear nuevas compras
- Agregar múltiples productos por compra
- Especificar precio unitario de compra
- Ver historial de compras
- Gestión de proveedores

### ✅ Panel de Control
- Estadísticas en tiempo real
- Total de productos activos
- Total de clientes registrados
- Ventas del día
- Productos con bajo stock
- Valor total del inventario

## 🛠️ Instalación

### Paso 1: Instalar dependencias

```bash
pip install flask flask-mysqldb
```

### Paso 2: Asegurar que MySQL está corriendo

```bash
# En Windows (si está instalado en Services)
# O ejecutar MySQL Workbench

# Verificar conexión
mysql -u root -p
```

### Paso 3: Crear la base de datos

```bash
mysql -u root -p < base_datos_tienda.sql
```

O ejecutar el script SQL directamente en MySQL Workbench.

### Paso 4: Configurar la conexión en app.py

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Tu contraseña si la tienes
app.config['MYSQL_DB'] = 'tienda_db'
```

## 🚀 Ejecutar la aplicación

```bash
python app.py
```

Luego accede a: **http://localhost:5000**

## 📱 Interfaz

### Menú de Navegación
- 🏠 **Inicio** - Panel de control con estadísticas
- 📦 **Productos** - Gestión de inventario
- 👥 **Clientes** - Base de datos de clientes
- 🤝 **Proveedores** - Información de proveedores
- 💰 **Ventas** - Registro de ventas
- 🛒 **Compras** - Registro de compras

### Colores y Diseño
- Interfaz minimalista y sencilla
- Colores corporativos: Azul (#3498db), Gris (#2c3e50)
- Responsiva para dispositivos móviles
- Tablas ordenadas y fáciles de leer
- Botones de acción claros

## 🔧 Rutas Disponibles

### Productos
- `GET /productos` - Listado de productos
- `GET /productos/new` - Formulario nuevo producto
- `POST /productos/new` - Crear producto
- `GET /productos/edit/<id>` - Formulario editar producto
- `POST /productos/edit/<id>` - Actualizar producto
- `GET /productos/delete/<id>` - Eliminar producto

### Clientes
- `GET /clientes` - Listado de clientes
- `GET /clientes/new` - Formulario nuevo cliente
- `POST /clientes/new` - Crear cliente
- `GET /clientes/edit/<id>` - Formulario editar cliente
- `POST /clientes/edit/<id>` - Actualizar cliente
- `GET /clientes/delete/<id>` - Eliminar cliente

### Proveedores
- `GET /proveedores` - Listado de proveedores
- `GET /proveedores/new` - Formulario nuevo proveedor
- `POST /proveedores/new` - Crear proveedor
- `GET /proveedores/edit/<id>` - Formulario editar proveedor
- `POST /proveedores/edit/<id>` - Actualizar proveedor
- `GET /proveedores/delete/<id>` - Eliminar proveedor

### Ventas
- `GET /ventas` - Listado de ventas
- `GET /ventas/new` - Formulario nueva venta
- `POST /ventas/new` - Crear venta
- `GET /ventas/delete/<id>` - Eliminar venta

### Compras
- `GET /compras` - Listado de compras
- `GET /compras/new` - Formulario nueva compra
- `POST /compras/new` - Crear compra
- `GET /compras/delete/<id>` - Eliminar compra

## 🎯 Ejemplo de Uso

### 1. Crear un Producto
1. Ir a **Productos** → **➕ Nuevo Producto**
2. Llenar el formulario:
   - Nombre: "Laptop HP"
   - Categoría: "Electrónica"
   - Precio: 899.99
   - Stock: 15
   - Mínimo: 5
   - Máximo: 50
3. Clic en **Crear**

### 2. Crear un Cliente
1. Ir a **Clientes** → **➕ Nuevo Cliente**
2. Llenar datos del cliente
3. Clic en **Crear**

### 3. Registrar una Venta
1. Ir a **Ventas** → **➕ Nueva Venta**
2. Seleccionar cliente
3. Agregar productos a vender
4. El sistema calcula automáticamente:
   - Precio unitario
   - Subtotal por item
   - Total con impuesto (10%)
5. Seleccionar método de pago
6. Clic en **Registrar Venta**
7. El stock se actualiza automáticamente

### 4. Registrar una Compra
1. Ir a **Compras** → **➕ Nueva Compra**
2. Seleccionar proveedor
3. Agregar productos a comprar
4. Especificar precio de compra unitario
5. El sistema calcula el total automáticamente
6. Clic en **Registrar Compra**

## 📊 Estructura de Archivos

```
proyecto/
├── app.py                          # Aplicación Flask principal
├── base_datos_tienda.sql          # Script para crear BD
├── gestor_tienda.py               # Gestor en línea de comandos (alternativa)
├── README_TIENDA.md               # Documentación de la BD
├── README_APP.md                  # Este archivo
└── templates/
    ├── base.html                  # Template base con CSS y navegación
    ├── index.html                 # Panel de inicio
    ├── productos.html             # Listado de productos
    ├── form_producto.html         # Formulario producto
    ├── clientes.html              # Listado de clientes
    ├── form_cliente.html          # Formulario cliente
    ├── proveedores.html           # Listado de proveedores
    ├── form_proveedor.html        # Formulario proveedor
    ├── ventas.html                # Listado de ventas
    ├── form_venta.html            # Formulario venta (con JavaScript)
    ├── compras.html               # Listado de compras
    ├── form_compra.html           # Formulario compra (con JavaScript)
    ├── 404.html                   # Página error 404
    └── 500.html                   # Página error 500
```

## 🎨 Estilos CSS

### Colores Utilizados
- Primario: #3498db (Azul)
- Secundario: #34495e (Gris oscuro)
- Éxito: #27ae60 (Verde)
- Peligro: #e74c3c (Rojo)
- Advertencia: #f39c12 (Naranja)
- Fondo: #f5f5f5 (Gris claro)

### Componentes
- Tarjetas con sombra
- Tablas con hover
- Botones con transiciones
- Formularios intuitivos
- Alertas de éxito/error
- Badges de estado

## 🔐 Características de Seguridad

- Parametrización de consultas SQL (prevención de SQL Injection)
- Confirmación antes de eliminar registros
- Validación de campos requeridos
- Manejo de errores con try-catch
- Flash messages para feedback del usuario

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask
```

### Error: "No module named 'MySQLdb'"
```bash
pip install flask-mysqldb
```

### Error: "Cannot connect to MySQL"
1. Verificar que MySQL está corriendo
2. Verificar usuario/contraseña en app.py
3. Verificar que la BD está creada

### Error: "Table already exists"
Drop la BD y vuelve a crear:
```sql
DROP DATABASE tienda_db;
mysql -u root -p < base_datos_tienda.sql
```

## 📝 Notas

- La aplicación usa Flask en modo debug (cambiar en producción)
- Los CRUDs son operaciones básicas sin autenticación
- Las transacciones se hacen automáticamente
- El stock se actualiza automáticamente al vender

## 🚀 Próximas Mejoras

- [ ] Sistema de autenticación de usuarios
- [ ] Roles y permisos (Administrador, Vendedor, Almacén)
- [ ] Búsqueda y filtrado avanzado
- [ ] Reportes en PDF
- [ ] Gráficos de ventas
- [ ] Dashboard con más métricas
- [ ] Importar/Exportar datos a Excel
- [ ] API REST para móvil
- [ ] Notificaciones de bajo stock

## 📞 Contacto

Para reportar errores o sugerencias, contacta al desarrollador.

---

**Versión:** 1.0  
**Última actualización:** Marzo 2026  
**Desarrollado con:** Flask + MySQL + HTML/CSS
