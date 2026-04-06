# 🚀 GUÍA RÁPIDA - INICIAR LA APLICACIÓN

## Pasos para ejecutar en 2 minutos:

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

O instalar individualmente:
```bash
pip install flask
pip install flask-mysqldb
```

### 2️⃣ Crear la base de datos MySQL

**Opción A: Desde terminal**
```bash
mysql -u root -p < base_datos_tienda.sql
```

**Opción B: Desde MySQL Workbench**
1. Abrir MySQL Workbench
2. Crear nueva conexión (si es necesario)
3. Abrir nuevo editor de queries
4. Copiar y pegar el contenido de `base_datos_tienda.sql`
5. Ejecutar (Ctrl+Enter)

### 3️⃣ Ejecutar la aplicación
```bash
python app.py
```

Deberías ver:
```
============================================================
🚀 SERVIDOR INICIADO
============================================================
📍 Acceder en: http://localhost:5000
👥 Interfaz de Gestión de Tienda
============================================================
```

### 4️⃣ Abrir en el navegador
```
http://localhost:5000
```

## ✅ Verificación

Al abrir la aplicación deberías ver:
- ✓ Panel de control con estadísticas
- ✓ Menú de navegación
- ✓ Dashboard con tarjetas de información
- ✓ Accesos rápidos para crear nuevos registros

## 🎮 Primeras acciones

1. **Crear un Producto**
   - Click en "📦 Productos"
   - Click en "➕ Nuevo Producto"
   - Llenar el formulario
   - Guardar

2. **Agregar un Cliente**
   - Click en "👥 Clientes"
   - Click en "➕ Nuevo Cliente"
   - Llenar datos
   - Guardar

3. **Registrar una Venta**
   - Click en "💰 Ventas"
   - Click en "➕ Nueva Venta"
   - Seleccionar cliente
   - Agregar productos
   - Guardar

## 🐛 Si algo no funciona

### Error: "Connection refused"
MySQL no está corriendo. Inicia el servidor:
```bash
# Windows
net start MySQL80  # o tu versión

# Mac
brew services start mysql
```

### Error: "Access denied"
Verifica en `app.py` que usuario/contraseña son correctos:
```python
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambiar si tienes contraseña
```

### Error: "No database"
Ejecuta el script SQL para crear la base de datos:
```bash
mysql -u root -p < base_datos_tienda.sql
```

## 📁 Archivos importantes

- **app.py** - Aplicación Flask (el servidor)
- **base_datos_tienda.sql** - Script de la base de datos
- **templates/** - Carpeta con las páginas HTML
- **requirements.txt** - Dependencias del proyecto

## 🎯 Funcionalidades principales

| Módulo | Funciones |
|--------|-----------|
| 📦 Productos | Crear, editar, eliminar, ver stock |
| 👥 Clientes | Crear, editar, eliminar clientes |
| 🤝 Proveedores | Crear, editar, eliminar proveedores |
| 💰 Ventas | Registrar ventas, actualizar stock |
| 🛒 Compras | Registrar compras a proveedores |

## 💡 Tips

- Usa Firefox o Chrome para mejor compatibilidad
- La aplicación es responsiva (funciona en móvil)
- Los cambios se guardan automáticamente
- El stock se actualiza al vender/comprar
- Los formularios muestran alertas de éxito/error

## 🔗 Recursos

Ver también:
- `README_APP.md` - Documentación completa de la web
- `README_TIENDA.md` - Documentación de la base de datos
- `base_datos_tienda.sql` - Estructura de las tablas

---

✨ **¡Listo para usar!** ✨
