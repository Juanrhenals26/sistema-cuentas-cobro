-- ============================================================
-- BASE DE DATOS DE TIENDA: INVENTARIO, VENTAS Y COMPRAS
-- ============================================================
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS tienda_db;
USE tienda_db;

-- ============================================================
-- TABLA 1: CATEGORÍAS
-- ============================================================
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA 2: PRODUCTOS (INVENTARIO)
-- ============================================================
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    id_categoria INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    cantidad_stock INT DEFAULT 0,
    cantidad_minima INT DEFAULT 10,
    cantidad_maxima INT DEFAULT 500,
    estado ENUM('Activo', 'Inactivo', 'Descontinuado') DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    INDEX idx_categoria (id_categoria),
    INDEX idx_estado (estado)
);

-- ============================================================
-- TABLA 3: PROVEEDORES
-- ============================================================
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL UNIQUE,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA 4: COMPRAS
-- ============================================================
CREATE TABLE IF NOT EXISTS compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    id_proveedor INT NOT NULL,
    fecha_compra DATE NOT NULL,
    fecha_entrega DATE,
    total_compra DECIMAL(12, 2) NOT NULL,
    estado_compra ENUM('Pendiente', 'Recibida', 'Parcial', 'Cancelada') DEFAULT 'Pendiente',
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    INDEX idx_proveedor (id_proveedor),
    INDEX idx_fecha (fecha_compra)
);

-- ============================================================
-- TABLA 5: DETALLE DE COMPRAS
-- ============================================================
CREATE TABLE IF NOT EXISTS detalle_compras (
    id_detalle_compra INT PRIMARY KEY AUTO_INCREMENT,
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    INDEX idx_compra (id_compra),
    INDEX idx_producto (id_producto)
);

-- ============================================================
-- TABLA 6: CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    apellido VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    tipo_cliente ENUM('Regular', 'Mayorista', 'VIP') DEFAULT 'Regular',
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_tipo (tipo_cliente)
);

-- ============================================================
-- TABLA 7: VENTAS
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    fecha_venta DATE NOT NULL,
    total_venta DECIMAL(12, 2) NOT NULL,
    impuesto DECIMAL(10, 2) DEFAULT 0,
    estado_venta ENUM('Completada', 'Pendiente', 'Cancelada', 'Devuelva') DEFAULT 'Completada',
    metodo_pago ENUM('Efectivo', 'Tarjeta', 'Transferencia', 'Cheque') DEFAULT 'Efectivo',
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    INDEX idx_cliente (id_cliente),
    INDEX idx_fecha (fecha_venta),
    INDEX idx_estado (estado_venta)
);

-- ============================================================
-- TABLA 8: DETALLE DE VENTAS
-- ============================================================
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id_detalle_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(5, 2) DEFAULT 0,
    subtotal DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    INDEX idx_venta (id_venta),
    INDEX idx_producto (id_producto)
);

-- ============================================================
-- TABLA 9: MOVIMIENTOS DE INVENTARIO (AUDITORÍA)
-- ============================================================
CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    tipo_movimiento ENUM('Entrada', 'Salida', 'Ajuste', 'Devolución') NOT NULL,
    cantidad INT NOT NULL,
    referencia VARCHAR(100),
    razon TEXT,
    stock_anterior INT,
    stock_nuevo INT,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100) DEFAULT 'Sistema',
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    INDEX idx_producto (id_producto),
    INDEX idx_fecha (fecha_movimiento),
    INDEX idx_tipo (tipo_movimiento)
);

-- ============================================================
-- INSERTAR DATOS DE EJEMPLO
-- ============================================================

-- Categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Productos electrónicos en general'),
('Ropa', 'Prendas de vestir'),
('Libros', 'Libros y material de lectura'),
('Alimentos', 'Productos alimenticios'),
('Accesorios', 'Accesorios varios');

-- Productos
INSERT INTO productos (nombre, descripcion, id_categoria, precio_unitario, cantidad_stock, cantidad_minima, cantidad_maxima) VALUES
('Laptop HP', 'Laptop HP Core i7, 16GB RAM', 1, 899.99, 15, 5, 50),
('Mouse Logitech', 'Mouse inalámbrico', 1, 29.99, 120, 20, 200),
('Teclado Mecánico', 'Teclado RGB con switches', 1, 79.99, 45, 10, 100),
('Camiseta M', 'Camiseta de algodón', 2, 19.99, 200, 50, 500),
('Pantalón Jeans', 'Pantalón vaquero azul', 2, 59.99, 80, 20, 150),
('El Quijote', 'Novela clásica', 3, 25.00, 35, 5, 100),
('Café Premium', 'Café molido 1kg', 4, 12.99, 500, 100, 1000),
('Monitor LG 27"', 'Monitor Full HD', 1, 199.99, 8, 2, 30),
('Audífonos Sony', 'Audífonos con cancelación de ruido', 5, 149.99, 25, 5, 80),
('Arroz 5kg', 'Arroz blanco premium', 4, 8.99, 300, 50, 500);

-- Proveedores
INSERT INTO proveedores (nombre, contacto, telefono, email, direccion, ciudad, pais) VALUES
('Distribuidora Electrónica SA', 'Juan Pérez', '555-1234', 'contacto@electronics.com', 'Calle Principal 123', 'Madrid', 'España'),
('Textiles y Moda Inc', 'María García', '555-5678', 'info@textiles.com', 'Avenida Central 456', 'Barcelona', 'España'),
('Editorial Libros Mundo', 'Carlos López', '555-9012', 'ventas@librosmundo.com', 'Plaza Mayor 789', 'Valencia', 'España'),
('Alimentos Frescos Ltd', 'Ana Rodríguez', '555-3456', 'compras@alimentosfrescos.com', 'Calle del Comercio 321', 'Bilbao', 'España'),
('Tech Components Global', 'Pedro Martínez', '555-7890', 'orders@techcomponents.com', 'Parque Industrial A1', 'Sevilla', 'España');

-- Clientes
INSERT INTO clientes (nombre, apellido, email, telefono, direccion, ciudad, pais, tipo_cliente) VALUES
('Cliente', 'Mayorista A', 'mayorista.a@email.com', '666-0001', 'Av. Empresarial 100', 'Madrid', 'España', 'Mayorista'),
('Cliente', 'Regular B', 'cliente.b@email.com', '666-0002', 'Calle Residencial 50', 'Barcelona', 'España', 'Regular'),
('Cliente', 'VIP C', 'cliente.vip@email.com', '666-0003', 'Av. Lujo 200', 'Valencia', 'España', 'VIP'),
('Cliente', 'Regular D', 'cliente.d@email.com', '666-0004', 'Calle Normal 75', 'Bilbao', 'España', 'Regular'),
('Cliente', 'Mayorista E', 'mayorista.e@email.com', '666-0005', 'Polígono Industrial 30', 'Sevilla', 'España', 'Mayorista');

-- Compras
INSERT INTO compras (id_proveedor, fecha_compra, fecha_entrega, total_compra, estado_compra) VALUES
(1, '2026-03-01', '2026-03-05', 3599.96, 'Recibida'),
(1, '2026-03-02', '2026-03-06', 1599.92, 'Recibida'),
(2, '2026-03-05', '2026-03-10', 2399.80, 'Recibida'),
(3, '2026-03-08', '2026-03-12', 875.00, 'Recibida'),
(4, '2026-03-10', '2026-03-14', 4495.00, 'Pendiente');

-- Detalle de Compras
INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 2, 850.00, 1700.00),
(1, 8, 2, 189.99, 379.98),
(1, 2, 30, 25.99, 779.70),
(1, 9, 15, 135.00, 2025.00),
(2, 3, 20, 72.00, 1440.00),
(2, 9, 8, 19.99, 159.92),
(3, 4, 60, 15.99, 959.40),
(3, 5, 30, 45.00, 1350.00),
(3, 4, 10, 9.00, 90.40),
(4, 6, 35, 25.00, 875.00),
(5, 7, 200, 11.99, 2398.00),
(5, 10, 150, 8.50, 1275.00),
(5, 7, 100, 8.22, 822.00);

-- Ventas
INSERT INTO ventas (id_cliente, fecha_venta, total_venta, impuesto, estado_venta, metodo_pago) VALUES
(1, '2026-03-15', 1899.80, 189.98, 'Completada', 'Transferencia'),
(2, '2026-03-16', 329.97, 32.99, 'Completada', 'Efectivo'),
(3, '2026-03-16', 2599.75, 259.97, 'Completada', 'Tarjeta'),
(4, '2026-03-17', 229.99, 23.00, 'Completada', 'Efectivo'),
(5, '2026-03-17', 1199.95, 119.99, 'Completada', 'Transferencia'),
(2, '2026-03-18', 69.98, 7.00, 'Completada', 'Tarjeta');

-- Detalle de Ventas
INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, descuento, subtotal) VALUES
(1, 1, 2, 899.99, 0, 1799.98),
(1, 2, 5, 29.99, 0, 149.95),
(1, 9, 1, 149.99, 0, 149.99),
(2, 4, 10, 19.99, 0, 199.90),
(2, 5, 2, 65.00, 0, 130.00),
(3, 8, 3, 199.99, 0, 599.97),
(3, 1, 1, 899.99, 0, 899.99),
(3, 9, 4, 150.00, 0, 600.00),
(3, 2, 20, 29.99, 100, 500.00),
(4, 7, 10, 12.99, 0, 129.90),
(4, 10, 5, 8.99, 0, 44.95),
(5, 9, 8, 149.99, 0, 1199.92),
(6, 4, 2, 19.99, 0, 39.98),
(6, 5, 1, 59.99, 0, 59.99),
(6, 7, 5, 12.99, 0, 64.95);

-- Movimientos de Inventario
INSERT INTO movimientos_inventario (id_producto, tipo_movimiento, cantidad, referencia, razon, stock_anterior, stock_nuevo) VALUES
(1, 'Entrada', 2, 'COMPRA-001', 'Compra a proveedor', 13, 15),
(2, 'Entrada', 30, 'COMPRA-001', 'Compra a proveedor', 90, 120),
(3, 'Entrada', 20, 'COMPRA-002', 'Compra a proveedor', 25, 45),
(4, 'Entrada', 60, 'COMPRA-003', 'Compra a proveedor', 140, 200),
(1, 'Salida', 2, 'VENTA-001', 'Venta al cliente', 15, 13),
(4, 'Salida', 10, 'VENTA-002', 'Venta al cliente', 200, 190),
(7, 'Entrada', 200, 'COMPRA-005', 'Compra a proveedor', 300, 500),
(7, 'Salida', 15, 'VENTA-004', 'Venta al cliente', 500, 485);

-- ============================================================
-- VISTA: RESUMEN DE VENTAS POR CLIENTE
-- ============================================================
CREATE VIEW v_ventas_por_cliente AS
SELECT 
    c.id_cliente,
    CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente,
    c.tipo_cliente,
    COUNT(v.id_venta) AS total_transacciones,
    SUM(v.total_venta) AS monto_total,
    AVG(v.total_venta) AS ticket_promedio
FROM clientes c
LEFT JOIN ventas v ON c.id_cliente = v.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido, c.tipo_cliente;

-- ============================================================
-- VISTA: PRODUCTOS CON BAJO STOCK
-- ============================================================
CREATE VIEW v_productos_bajo_stock AS
SELECT 
    id_producto,
    nombre,
    cantidad_stock,
    cantidad_minima,
    (cantidad_minima - cantidad_stock) AS falta_para_minimo,
    precio_unitario,
    (cantidad_minima * precio_unitario) AS valor_compra_minimo
FROM productos
WHERE cantidad_stock < cantidad_minima
ORDER BY falta_para_minimo DESC;

-- ============================================================
-- VISTA: RESUMEN DE COMPRAS POR PROVEEDOR
-- ============================================================
CREATE VIEW v_compras_por_proveedor AS
SELECT 
    p.id_proveedor,
    p.nombre AS proveedor,
    COUNT(c.id_compra) AS total_compras,
    SUM(c.total_compra) AS monto_total,
    AVG(c.total_compra) AS promedio_compra,
    MAX(c.fecha_compra) AS ultima_compra
FROM proveedores p
LEFT JOIN compras c ON p.id_proveedor = c.id_proveedor
GROUP BY p.id_proveedor, p.nombre;

-- ============================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================================
CREATE INDEX idx_productos_stock ON productos(cantidad_stock);
CREATE INDEX idx_ventas_estado ON ventas(estado_venta);
CREATE INDEX idx_compras_estado ON compras(estado_compra);
CREATE INDEX idx_clientes_estado ON clientes(estado);

-- ============================================================
-- Mostrar estructura de la base de datos
-- ============================================================
SELECT 'Base de datos creada exitosamente. Tablas:' AS mensaje;
SHOW TABLES;
