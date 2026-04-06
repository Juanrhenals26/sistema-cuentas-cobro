# 📄 Sistema Automatizado de Cuentas de Cobro

Sistema en Python que genera y envía cuentas de cobro en PDF por correo electrónico de forma automática.

---

## 📁 Estructura del proyecto

```
cuentas_cobro/
├── main.py                      ← Script principal (ejecutar diariamente)
├── generar_pdf.py               ← Genera el PDF de la cuenta de cobro
├── enviar_correo.py             ← Envía el correo con el PDF adjunto
├── num_a_letras.py              ← Convierte números a letras en español
├── empresas.json                ← Datos de tus empresas (editable)
├── instalar_dependencias.bat    ← Instala librerías Python (1 sola vez)
├── ejecutar_manual.bat          ← Prueba el sistema manualmente
├── configurar_tarea_windows.bat ← Automatiza la ejecución diaria
├── pdfs/                        ← PDFs generados (se crean solos)
└── logs/                        ← Registros de envíos (se crean solos)
```

---

## 🚀 Instalación (paso a paso)

### Paso 1 — Instalar Python
1. Ve a: https://www.python.org/downloads/
2. Descarga la versión más reciente (3.10 o superior)
3. **MUY IMPORTANTE:** Durante la instalación, marca la casilla **"Add Python to PATH"**
4. Finaliza la instalación

### Paso 2 — Instalar dependencias
1. Abre la carpeta `cuentas_cobro` en el Explorador de archivos
2. Haz **doble clic** en `instalar_dependencias.bat`
3. Espera a que termine → verás "Instalación completada!"

### Paso 3 — Configurar tu contraseña de correo

> ⚠️ **Si tienes verificación en dos pasos (recomendado):**
> 1. Ve a https://account.microsoft.com/security
> 2. Busca "Contraseña de aplicación" → Crear nueva
> 3. Copia esa contraseña (es diferente a tu contraseña normal)

1. Abre `enviar_correo.py` con el Bloc de Notas o VS Code
2. Busca esta línea:
   ```python
   REMITENTE_CLAVE = "TU_CONTRASEÑA_AQUI"
   ```
3. Reemplaza `TU_CONTRASEÑA_AQUI` con tu contraseña (o contraseña de aplicación)
4. Guarda el archivo

### Paso 4 — Configurar tus empresas

Abre `empresas.json` y edita los datos:

```json
[
  {
    "nombre_empresa": "NOMBRE DE LA EMPRESA S.A.S.",
    "correo_destino": "correo@empresa.com",
    "valor": 1500000,
    "dia_envio": 10,
    "concepto": "Arrendamiento software PRESTASOF y GAMMA"
  }
]
```

| Campo | Descripción |
|-------|-------------|
| `nombre_empresa` | Nombre completo de la empresa |
| `correo_destino` | Correo donde se enviará la cuenta |
| `valor` | Valor en pesos (sin puntos ni comas) |
| `dia_envio` | Día del mes para enviar (1-31) |
| `concepto` | Descripción del cobro |

### Paso 5 — Probar el sistema

1. Haz **doble clic** en `ejecutar_manual.bat`
2. Verás en pantalla qué empresas se procesaron
3. Revisa la carpeta `pdfs/` para ver los archivos generados
4. Revisa la carpeta `logs/` para ver el registro detallado

---

## ⚙️ Automatización diaria (Programador de Tareas)

Para que el sistema se ejecute automáticamente todos los días:

1. Haz **clic derecho** en `configurar_tarea_windows.bat`
2. Selecciona **"Ejecutar como administrador"**
3. Espera el mensaje de confirmación

Esto crea una tarea que se ejecuta **todos los días a las 8:00 AM**. El sistema revisará si alguna empresa tiene envío programado para ese día y, si es así, generará y enviará automáticamente la cuenta.

Para ver o modificar la tarea:
- Abre el **Programador de tareas** de Windows
- Busca `CuentasCobro_Automaticas`

---

## 🔧 Uso desde la línea de comandos

```bash
# Modo normal: solo envía si hoy es el día programado
python main.py

# Modo forzado: envía a TODAS las empresas (útil para pruebas)
python main.py --forzar
```

---

## ➕ Agregar una nueva empresa

1. Abre `empresas.json`
2. Agrega un nuevo objeto al final de la lista:
```json
{
  "nombre_empresa": "NUEVA EMPRESA S.A.S.",
  "correo_destino": "pagos@nuevaempresa.com",
  "valor": 800000,
  "dia_envio": 15,
  "concepto": "Arrendamiento software PRESTASOF y GAMMA"
}
```
3. Guarda el archivo. ¡Listo! Se procesará automáticamente.

---

## 📋 Registro de envíos (logs)

En la carpeta `logs/` encontrarás archivos como `envios_2026_03.log` con el detalle de:
- Fecha y hora de cada ejecución
- Empresas procesadas
- Estado de cada envío (OK o ERROR)
- Errores si los hubo

---

## ❓ Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: reportlab` | Ejecuta `instalar_dependencias.bat` |
| Error de autenticación de correo | Verifica tu contraseña o genera una "contraseña de aplicación" en tu cuenta de Microsoft |
| El correo no llega | Revisa la carpeta de spam del destinatario |
| PDF no se genera | Verifica que la carpeta `pdfs/` exista (se crea automáticamente) |
| Tarea no se ejecuta | Asegúrate de que Python esté en el PATH del sistema |

---

*Sistema desarrollado en Python con ReportLab para generación de PDFs y smtplib para envío de correos.*
