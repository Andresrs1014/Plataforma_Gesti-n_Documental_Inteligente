from pathlib import Path
import shutil
from datetime import datetime
from config import Config
from utils.logger import configurar_logger

logger = configurar_logger("Word-Generador")

def crear_documento(nombre_archivo: str, carpeta_destino: Path, plantilla: str) -> Path:
    """
    Crea una copia de la plantilla Word en la carpeta destino
    
    Args:
        nombre_archivo: Nombre del archivo a crear (sin extensión)
        carpeta_destino: Carpeta donde guardar el documento
        plantilla: Nombre de la plantilla Word a usar
        
    Returns:
        Path del documento creado
        
    Raises:
        FileNotFoundError: Si la plantilla no existe
        PermissionError: Si no hay permisos para escribir
    """
    
    logger.info(f"[WORD] Iniciando creación de documento: {nombre_archivo}")
    
    # Validar que plantilla existe
    ruta_plantilla = Config.PLANTILLAS_WORD_DIR / plantilla
    
    if not ruta_plantilla.exists():
        logger.error(f"Plantilla Word no encontrada: {ruta_plantilla}")
        raise FileNotFoundError(f"Plantilla Word no existe: {plantilla}")
    
    logger.info(f"Plantilla Word encontrada: {ruta_plantilla}")
    
    # Crear carpeta destino si no existe
    try:
        carpeta_destino.mkdir(parents=True, exist_ok=True)
        logger.info(f"Carpeta destino verificada: {carpeta_destino}")
    except PermissionError as e:
        logger.error(f"Sin permisos para crear carpeta: {carpeta_destino}")
        raise PermissionError(f"No hay permisos para escribir en: {carpeta_destino}") from e
    
    # Agregar timestamp y versión
    timestamp = datetime.now().strftime(Config.TIMESTAMP_FORMATO)
    
    # Extraer versión de los datos si existe, sino usar V1
    nombre_base = nombre_archivo.replace('.docx', '')
    nombre_final = f"{nombre_base}_{timestamp}.docx"
    destino = carpeta_destino / nombre_final
    
    # Copiar plantilla
    try:
        shutil.copy(ruta_plantilla, destino)
        logger.info(f"✅ [WORD] Documento creado exitosamente: {destino}")
        return destino
    except Exception as e:
        logger.error(f"Error al copiar plantilla Word: {e}")
        raise
