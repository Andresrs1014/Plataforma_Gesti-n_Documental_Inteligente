@echo off
chcp 65001 >nul
echo ==========================================
echo   PGDI - Plataforma de Gestión Documental
echo ==========================================
echo.

REM Verificar si existe el entorno virtual
if not exist ".venv\" (
    echo [ERROR] No se encuentra el entorno virtual .venv
    echo.
    echo Por favor, ejecuta primero:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [1/3] Activando entorno virtual...
call .venv\Scripts\activate.bat

echo [2/3] Verificando dependencias...
python -c "import fastapi, uvicorn, openpyxl" 2>nul
if errorlevel 1 (
    echo [ADVERTENCIA] Instalando dependencias faltantes...
    pip install -r requirements.txt
)

echo [3/3] Iniciando servidor...
echo.
echo ==========================================
echo   Servidor iniciado correctamente
echo ==========================================
echo   URL: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo.
echo   Presiona Ctrl+C para detener
echo ==========================================
echo.

python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
