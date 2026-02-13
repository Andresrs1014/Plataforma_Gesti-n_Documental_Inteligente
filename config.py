from pathlib import Path
from datetime import datetime

class Config:
    """Configuración centralizada del proyecto PGDI"""
    
    # Rutas base
    BASE_DIR = Path(__file__).resolve().parent
    PLANTILLAS_DIR = BASE_DIR / "plantillas"
    SALIDAS_DIR = BASE_DIR / "salidas"
    LOGS_DIR = BASE_DIR / "logs"
    MAPPING_DIR = BASE_DIR / "mapping"
    
    # Rutas de salida específicas
    SALIDAS_PROCEDIMIENTOS = SALIDAS_DIR / "procedimientos"
    SALIDAS_INSTRUCTIVOS = SALIDAS_DIR / "instructivos"
    
    # Plantillas
    PLANTILLA_PROCEDIMIENTO = "FORMATO_PROCEDIMIENTO.xlsx"
    PLANTILLA_INSTRUCTIVO = "FORMATO_INSTRUCTIVO.xlsx"
    
    # Archivos de mapeo
    MAPEO_PROCEDIMIENTO = "procedimiento_map.json"
    MAPEO_INSTRUCTIVO = "instructivo_map.json"
    
    # Configuración de API
    API_TITLE = "PGDI - Plataforma de Gestión Documental Inteligente"
    API_DESCRIPTION = "Sistema automatizado para generación de Procedimientos e Instructivos"
    API_VERSION = "1.0.0"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # Formato de fechas
    FECHA_FORMATO = "%Y-%m-%d"
    TIMESTAMP_FORMATO = "%Y%m%d_%H%M%S"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = LOGS_DIR / f"pgdi_{datetime.now().strftime('%Y%m%d')}.log"
    
    @classmethod
    def crear_directorios(cls):
        """Crea todos los directorios necesarios"""
        cls.SALIDAS_PROCEDIMIENTOS.mkdir(parents=True, exist_ok=True)
        cls.SALIDAS_INSTRUCTIVOS.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.MAPPING_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorios creados/verificados")
    
    @classmethod
    def validar_plantillas(cls):
        """Valida que existan las plantillas necesarias"""
        plantilla_proc = cls.PLANTILLAS_DIR / cls.PLANTILLA_PROCEDIMIENTO
        plantilla_inst = cls.PLANTILLAS_DIR / cls.PLANTILLA_INSTRUCTIVO
        
        errores = []
        if not plantilla_proc.exists():
            errores.append(f"❌ Plantilla no encontrada: {plantilla_proc}")
        if not plantilla_inst.exists():
            errores.append(f"❌ Plantilla no encontrada: {plantilla_inst}")
        
        if errores:
            for error in errores:
                print(error)
            return False
        
        print(f"✅ Plantillas validadas correctamente")
        return True

# Inicializar al importar
Config.crear_directorios()
