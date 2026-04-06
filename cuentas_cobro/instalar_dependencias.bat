@echo off
REM instalar_dependencias.bat
REM Instala todas las librerías Python necesarias para el sistema

echo ============================================
echo  Instalando dependencias del sistema
echo  Cuentas de Cobro Automatizadas
echo ============================================
echo.

pip install reportlab

echo.
echo ============================================
echo  Instalacion completada!
echo  Ahora configura tu contrasena en enviar_correo.py
echo  y ejecuta:  python main.py --forzar
echo ============================================
pause
