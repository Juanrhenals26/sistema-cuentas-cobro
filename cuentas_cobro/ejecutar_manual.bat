@echo off
REM ejecutar_manual.bat
REM Ejecuta el sistema manualmente (envia a TODAS las empresas)
REM Util para hacer pruebas o envios manuales

echo ============================================
echo  Ejecutando Sistema de Cuentas de Cobro
echo  MODO: FORZADO (todas las empresas)
echo ============================================
echo.

cd /d "%~dp0"
python main.py --forzar

echo.
pause
