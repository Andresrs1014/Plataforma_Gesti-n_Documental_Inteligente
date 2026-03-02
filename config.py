from pathlib import Path
from datetime import datetime
from typing import Optional

class Config:
    
    
    # =====================  RUTAS BASE ======================
    
    BASE_DIR = Path(__file__).parent
    
    # Plantillas
    PLANTILLAS_DIR = BASE_DIR / "plantillas"
    PLANTILLAS_EXCEL_DIR = PLANTILLAS_DIR / "excel"
    PLANTILLAS_WORD_DIR = PLANTILLAS_DIR / "word"
    
    # Salidas
    
    SALIDAS_DIR = BASE_DIR / "salidas"
    TEMP_DIR = BASE_DIR / "temp"
    TEMP_PREVIEW_DIR = TEMP_DIR / "previews"
    
    # Logs y mapeo
    
    LOGS_DIR = BASE_DIR / "logs"
    MAPPING_DIR = BASE_DIR / "mapping"
    
    # Base de datos
    DATABASE_FILE = BASE_DIR / "pgdi.db"
    
    # ==================== PLANTILLAS EXCEL (legacy) ====================
    PLANTILLA_PROCEDIMIENTO_EXCEL = "FORMATO_PROCEDIMIENTO.xlsx"
    PLANTILLA_INSTRUCTIVO_EXCEL = "FORMATO_INSTRUCTIVO.xlsx"
    
    # ==================== PLANTILLA WORD (única) =====================
    PLANTILLA_INSTRUCTIVO = "INSTRUCTIVO.docx"
    
    # ==================== CONFIGURACIÓN DE API =====================
    
    API_TITLE = "PGDI - Plataforma de Gestión Documental Inteligente"
    API_DESCRIPTION = "Sistema automatizado para generaciión de Procedimientos e Instructivos"
    API_VERSION = "2.1.0"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # ==================== FORMATO DE FECHAS ====================
    FECHA_FORMATO = "%Y-%m-%d"
    FECHA_HORA_FORMATO = "%Y-%m-%d %H:%M:%S"
    TIMESTAMP_FORMATO = "%Y%m%d_%H%M%S"

    # Formato para carpetas (año/mes)
    CARPETA_AÑO_FORMATO = "%Y"
    CARPETA_MES_FORMATO = "%m_%B"
    
    # ==================== LOGGING ======================
    LOG_LEVEL = "INFO"
    LOG_FILE = LOGS_DIR / f"pgdi_{datetime.now().strftime('%Y%m%d')}.log"
    
    # ==================== CONFIGURACIÓN DE ARCHIVOS ====================
    
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = ['.docx', '.pdf', '.xlsx']
    
    # ==================== MÉTODOS DE UTILIDAD ======================
    
    @classmethod
    def crear_directorios(cls):
        
        directorios = [
            cls.PLANTILLAS_EXCEL_DIR,
            cls.PLANTILLAS_WORD_DIR,
            cls.TEMP_DIR,
            cls.TEMP_PREVIEW_DIR,
            cls.LOGS_DIR,
            cls.MAPPING_DIR,
            cls.SALIDAS_DIR,
        ]
    
        for directorio in directorios:
            directorio.mkdir(parents=True, exist_ok=True)
            
        print(f" Directorios creados/verificados correctamente >:3")
    
    @classmethod
    def validar_plantillas_excel(cls):
        
        plantilla_proc = cls.PLANTILLAS_EXCEL_DIR / cls.PLANTILLA_PROCEDIMIENTO_EXCEL
        plantilla_inst = cls.PLANTILLAS_EXCEL_DIR / cls.PLANTILLA_INSTRUCTIVO_EXCEL
        
        errores = []
        if not plantilla_proc.exists():
            errores.append(f"Plantilla Excel no encontrada: {plantilla_proc}")
        if not plantilla_inst.exists():
            errores.append(f"Plantilla Excel no encontrada: {plantilla_inst}")
        
        if errores:
            for error in errores:
                print(error)
                return False
        
        print(f" Plantillas Excel validadas correctamente >:3")
        return True 
    @classmethod
    def validar_plantillas_word(cls):
        """Valida que exista la plantilla Word Unica (INSTRUCTIVO)"""
        plantilla = cls.PLANTILLAS_WORD_DIR / cls.PLANTILLA_INSTRUCTIVO
        if not plantilla.exists():
            print(f"❌ Plantilla Word no encontrada: {plantilla}")
            return False
        print(f"✅ Plantilla Word encontrada: {cls.PLANTILLA_INSTRUCTIVO}")
        return True
    
    @classmethod
    def obtener_ruta_salida(cls, tipo: str, anio: Optional[str] = None, mes: Optional[str] = None):
        """
        Obtiene la ruta de salida organizada por año/mes
        
        Args:
            tipo: 'procedimientos' o 'instructivos'
            anio: Año (si None, usa año actual)
            mes: Mes con nombre (si None, usa mes actual)
            
        Returns:
            Path de la carpeta de salida
        """
        if not anio:
            anio = datetime.now().strftime(cls.CARPETA_AÑO_FORMATO)
        if not mes:
            mes = datetime.now().strftime(cls.CARPETA_MES_FORMATO)
        
        ruta = cls.SALIDAS_DIR / anio / mes / tipo
        ruta.mkdir(parents=True, exist_ok=True)
        
        return ruta

Config.crear_directorios()