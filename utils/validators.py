from typing import Dict, Any
import re
from datetime import datetime

class ValidadorDatos:
    """Validaciones de datos de entrada"""
    
    @staticmethod
    def validar_codigo(codigo: str) -> bool:
        """
        Valida formato de código: XXX-000-XXX
        
        Ejemplos válidos:
        - PROC-001-GAF
        - INS-042-GAD
        """
        patron = r'^[A-Z]{3,4}-\d{3}-[A-Z]{3,4}$'
        return bool(re.match(patron, codigo))
    
    @staticmethod
    def validar_fecha(fecha: str) -> bool:
        """
        Valida formato de fecha: YYYY-MM-DD
        
        Ejemplo válido: 2026-02-13
        """
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_version(version: str) -> bool:
        """
        Valida formato de versión: V1, V2, etc.
        """
        patron = r'^V\d+$'
        return bool(re.match(patron, version.upper()))
    
    @staticmethod
    def validar_texto_obligatorio(texto: str, min_length: int = 3) -> bool:
        """
        Valida que un texto no esté vacío y tenga longitud mínima
        """
        return isinstance(texto, str) and len(texto.strip()) >= min_length
    
    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """
        Limpia y normaliza texto
        """
        if not isinstance(texto, str):
            return ""
        return texto.strip()
    
    @staticmethod
    def normalizar_codigo(codigo: str) -> str:
        """
        Convierte código a mayúsculas y limpia espacios
        """
        return codigo.strip().upper()
