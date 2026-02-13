#!/usr/bin/env python
"""
Script de inicio para PGDI - Plataforma de Gestión Documental Inteligente
Verifica el entorno y inicia el servidor automáticamente
"""

import os
import sys
import subprocess
from pathlib import Path

# Colores para la consola
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Muestra el banner de inicio"""
    print(f"\n{Color.BLUE}{'='*50}")
    print(f"  PGDI - Plataforma de Gestión Documental")
    print(f"{'='*50}{Color.END}\n")

def verificar_entorno_virtual():
    """Verifica si existe y está activo el entorno virtual"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print(f"{Color.RED}[ERROR] No se encuentra el entorno virtual .venv{Color.END}")
        print("\nPor favor, ejecuta primero:")
        print("  python -m venv .venv")
        
        if sys.platform == "win32":
            print("  .venv\\Scripts\\activate")
        else:
            print("  source .venv/bin/activate")
        
        print("  pip install -r requirements.txt\n")
        return False
    
    # Verificar si está activo
    if sys.prefix == sys.base_prefix:
        print(f"{Color.YELLOW}[ADVERTENCIA] El entorno virtual no está activo{Color.END}")
        print("Activándolo automáticamente...\n")
    
    return True

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print(f"{Color.BLUE}[1/3]{Color.END} Verificando dependencias...")
    
    try:
        import fastapi
        import uvicorn
        import openpyxl
        print(f"{Color.GREEN}✓ Dependencias OK{Color.END}\n")
        return True
    except ImportError as e:
        print(f"{Color.YELLOW}⚠ Instalando dependencias faltantes...{Color.END}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print()
        return True

def verificar_estructura():
    """Verifica que existan las carpetas necesarias"""
    print(f"{Color.BLUE}[2/3]{Color.END} Verificando estructura...")
    
    carpetas = ['frontend', 'plantillas', 'salidas', 'excel']
    
    for carpeta in carpetas:
        path = Path(carpeta)
        if not path.exists():
            print(f"{Color.YELLOW}⚠ Creando carpeta: {carpeta}{Color.END}")
            path.mkdir(parents=True, exist_ok=True)
    
    print(f"{Color.GREEN}✓ Estructura OK{Color.END}\n")

def iniciar_servidor():
    """Inicia el servidor uvicorn"""
    print(f"{Color.BLUE}[3/3]{Color.END} Iniciando servidor...\n")
    
    print(f"{Color.GREEN}{'='*50}")
    print(f"  Servidor iniciado correctamente")
    print(f"{'='*50}{Color.END}")
    print(f"  URL:  {Color.BOLD}http://localhost:8000{Color.END}")
    print(f"  Docs: {Color.BOLD}http://localhost:8000/docs{Color.END}")
    print(f"\n  Presiona {Color.BOLD}Ctrl+C{Color.END} para detener")
    print(f"{Color.GREEN}{'='*50}{Color.END}\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Servidor detenido{Color.END}\n")

def main():
    """Función principal"""
    print_banner()
    
    if not verificar_entorno_virtual():
        sys.exit(1)
    
    if not verificar_dependencias():
        sys.exit(1)
    
    verificar_estructura()
    iniciar_servidor()

if __name__ == "__main__":
    main()
