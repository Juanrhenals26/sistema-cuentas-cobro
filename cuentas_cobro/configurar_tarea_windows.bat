@echo off
REM configurar_tarea_windows.bat
REM Configura el Programador de Tareas de Windows para ejecutar
REM el sistema automaticamente todos los dias a las 8:00 AM
REM IMPORTANTE: Ejecutar como Administrador

echo ============================================
echo  Configurando Tarea Programada en Windows
echo  El sistema se ejecutara todos los dias a las 8:00 AM
echo ============================================
echo.

REM Obtener ruta absoluta del directorio actual
set DIRECTORIO=%~dp0
set SCRIPT_PYTHON=%DIRECTORIO%main.py

echo Directorio del proyecto: %DIRECTORIO%
echo Script Python: %SCRIPT_PYTHON%
echo.

REM Crear la tarea programada
schtasks /create /tn "CuentasCobro_Automaticas" ^
  /tr "python \"%SCRIPT_PYTHON%\"" ^
  /sc DAILY ^
  /st 08:00 ^
  /f

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Tarea programada creada exitosamente!
    echo      Nombre: CuentasCobro_Automaticas
    echo      Horario: Todos los dias a las 08:00 AM
) ELSE (
    echo.
    echo [ERROR] No se pudo crear la tarea.
    echo         Asegurate de ejecutar este archivo como Administrador.
)

echo.
pause
