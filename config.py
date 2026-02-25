from pathlib import Path
from datetime import datetime
from typing import Optional

class Config:
    """Configuración centralizada del proyecto PGDI"""
    
    # ==================== RUTAS BASE ====================
    BASE_DIR = Path(__file__).resolve().parent
    
    # Plantillas
    PLANTILLAS_DIR = BASE_DIR / "plantillas"
    PLANTILLAS_EXCEL_DIR = PLANTILLAS_DIR / "excel"      # ⭐ NUEVO
    PLANTILLAS_WORD_DIR = PLANTILLAS_DIR / "word"        # ⭐ NUEVO
    
    # Salidas
    SALIDAS_DIR = BASE_DIR / "salidas"
    TEMP_DIR = BASE_DIR / "temp"                         # ⭐ NUEVO
    TEMP_PREVIEW_DIR = TEMP_DIR / "preview"              # ⭐ NUEVO
    
    # Logs y mapeo
    LOGS_DIR = BASE_DIR / "logs"
    MAPPING_DIR = BASE_DIR / "mapping"
    
    # Base de datos
    DATABASE_FILE = BASE_DIR / "pgdi.db"                 # ⭐ NUEVO
    
    # ==================== PLANTILLAS EXCEL ====================
    PLANTILLA_PROCEDIMIENTO_EXCEL = "FORMATO_PROCEDIMIENTO.xlsx"
    PLANTILLA_INSTRUCTIVO_EXCEL = "FORMATO_INSTRUCTIVO.xlsx"
    
    # ==================== PLANTILLAS WORD ==================== 
    PLANTILLA_PROCEDIMIENTO_WORD = "PROCEDIMIENTO.docx"  # ⭐ NUEVO
    PLANTILLA_INSTRUCTIVO_WORD = "INSTRUCTIVO.docx"      # ⭐ NUEVO
    
    # ==================== ARCHIVOS DE MAPEO ====================
    MAPEO_PROCEDIMIENTO = "procedimiento_map.json"
    MAPEO_INSTRUCTIVO = "instructivo_map.json"
    
    # ==================== CONFIGURACIÓN DE API ====================
    API_TITLE = "PGDI - Plataforma de Gestión Documental Inteligente"
    API_DESCRIPTION = "Sistema automatizado para generación de Procedimientos e Instructivos"
    API_VERSION = "2.0.0"                                # ⭐ ACTUALIZADO (v2 con Word)
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # ==================== FORMATO DE FECHAS ====================
    FECHA_FORMATO = "%Y-%m-%d"
    FECHA_HORA_FORMATO = "%Y-%m-%d %H:%M:%S"            # ⭐ NUEVO
    TIMESTAMP_FORMATO = "%Y%m%d_%H%M%S"
    
    # Formato para carpetas (año/mes)
    CARPETA_AÑO_FORMATO = "%Y"                           # ⭐ NUEVO
    CARPETA_MES_FORMATO = "%m_%B"                        # ⭐ NUEVO (02_Febrero)
    
    # ==================== LOGGING ====================
    LOG_LEVEL = "INFO"
    LOG_FILE = LOGS_DIR / f"pgdi_{datetime.now().strftime('%Y%m%d')}.log"
    
    # ==================== CONFIGURACIÓN DE ARCHIVOS ====================
    MAX_FILE_SIZE_MB = 10                                # ⭐ NUEVO
    ALLOWED_EXTENSIONS = ['.docx', '.pdf', '.xlsx']      # ⭐ NUEVO
    
    # ==================== MÉTODOS DE UTILIDAD ====================
    
    @classmethod
    def crear_directorios(cls):
        """Crea todos los directorios necesarios"""
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
        
        print(f"✅ Directorios creados/verificados")
    
    @classmethod
    def validar_plantillas_excel(cls):
        """Valida que existan las plantillas Excel"""
        plantilla_proc = cls.PLANTILLAS_EXCEL_DIR / cls.PLANTILLA_PROCEDIMIENTO_EXCEL
        plantilla_inst = cls.PLANTILLAS_EXCEL_DIR / cls.PLANTILLA_INSTRUCTIVO_EXCEL
        
        errores = []
        if not plantilla_proc.exists():
            errores.append(f"❌ Plantilla Excel no encontrada: {plantilla_proc}")
        if not plantilla_inst.exists():
            errores.append(f"❌ Plantilla Excel no encontrada: {plantilla_inst}")
        
        if errores:
            for error in errores:
                print(error)
            return False
        
        print(f"✅ Plantillas Excel validadas")
        return True
    
    @classmethod
    def validar_plantillas_word(cls):
        """Valida que existan las plantillas Word"""
        plantilla_proc = cls.PLANTILLAS_WORD_DIR / cls.PLANTILLA_PROCEDIMIENTO_WORD
        plantilla_inst = cls.PLANTILLAS_WORD_DIR / cls.PLANTILLA_INSTRUCTIVO_WORD
        
        errores = []
        if not plantilla_proc.exists():
            errores.append(f"❌ Plantilla Word no encontrada: {plantilla_proc}")
        else:
            print(f"✅ Plantilla Word encontrada: {cls.PLANTILLA_PROCEDIMIENTO_WORD}")
            
        if not plantilla_inst.exists():
            errores.append(f"❌ Plantilla Word no encontrada: {plantilla_inst}")
        else:
            print(f"✅ Plantilla Word encontrada: {cls.PLANTILLA_INSTRUCTIVO_WORD}")
        
        if errores:
            for error in errores:
                print(error)
            return False
        
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

# Inicializar al importar
Config.crear_directorios()
