@echo off
chcp 65001 >nul
title Servidor Local - GT Data Consulting (Calculo de LEDs)
color 0B

echo =========================================================================
echo                GT DATA CONSULTING - SERVIDOR LOCAL
echo       Cálculo de Lúmenes, Potencia Radiada y Circuitos de LEDs
echo =========================================================================
echo.
echo [*] Iniciando servidor web local en el puerto 8080...
echo [*] URL de acceso: http://localhost:8080/
echo [*] Compatible con Chrome, Firefox, Brave y Edge.
echo.
echo Presiona [Ctrl + C] en esta ventana para detener el servidor en cualquier momento.
echo =========================================================================
echo.

:: Abrir automáticamente la página en el navegador predeterminado
timeout /t 2 >nul
start http://localhost:8080/

:: Ejecutar el servidor HTTP con Python
python -m http.server 8080

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] No se pudo iniciar el servidor con Python.
    echo Asegúrate de tener Python instalado y añadido al PATH del sistema.
    pause
)
