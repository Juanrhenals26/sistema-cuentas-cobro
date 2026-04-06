@echo off
chcp 65001 >nul
title Sistema de Cuentas de Cobro

echo.
echo  ================================================
echo   Sistema de Cuentas de Cobro - Iniciando...
echo  ================================================
echo.

cd /d "%~dp0"

REM Activar entorno virtual si existe
if exist "..\\.venv\\Scripts\\activate.bat" (
    call "..\\.venv\\Scripts\\activate.bat"
    echo  [OK] Entorno virtual activado.
) else (
    echo  [ADVERTENCIA] No se encontro el entorno virtual .venv
    echo  Usando Python del sistema...
)
echo.

echo  Iniciando servidor web...
echo  Abre tu navegador en: http://localhost:5000
echo  Presiona Ctrl+C para detener.
echo.

python app.py

pause
