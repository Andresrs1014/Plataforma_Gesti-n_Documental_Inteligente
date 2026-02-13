from pathlib import Path
import shutil
from datetime import datetime
from config import Config
from utils.logger import configurar_logger

logger = configurar_logger("Generador")

def crear_documento(nombre_archivo: str, carpeta_destino: Path, plantilla: str) -> Path:
    """
    Crea una copia de la plantilla en la carpeta destino
    
    Args:
        nombre_archivo: Nombre del archivo a crear
        carpeta_destino: Carpeta donde guardar el documento
        plantilla: Nombre de la plantilla a usar
        
    Returns:
        Path del documento creado
        
    Raises:
        FileNotFoundError: Si la plantilla no existe
        PermissionError: Si no hay permisos para escribir
    """
    
    logger.info(f"Iniciando creación de documento: {nombre_archivo}")
    
    # Validar que plantilla existe
    ruta_plantilla = Config.PLANTILLAS_DIR / plantilla
    if not ruta_plantilla.exists():
        logger.error(f"Plantilla no encontrada: {ruta_plantilla}")
        raise FileNotFoundError(f"Plantilla no existe: {plantilla}")
    
    logger.info(f"Plantilla encontrada: {ruta_plantilla}")
    
    # Crear carpeta destino si no existe
    try:
        carpeta_destino.mkdir(parents=True, exist_ok=True)
        logger.info(f"Carpeta destino verificada: {carpeta_destino}")
    except PermissionError as e:
        logger.error(f"Sin permisos para crear carpeta: {carpeta_destino}")
        raise PermissionError(f"No hay permisos para escribir en: {carpeta_destino}") from e
    
    # Agregar timestamp para evitar duplicados
    timestamp = datetime.now().strftime(Config.TIMESTAMP_FORMATO)
    nombre_base = nombre_archivo.replace('.xlsx', '')
    nombre_final = f"{nombre_base}_{timestamp}.xlsx"
    destino = carpeta_destino / nombre_final
    
    # Copiar plantilla
    try:
        shutil.copy(ruta_plantilla, destino)
        logger.info(f"✅ Documento creado exitosamente: {destino}")
        return destino
    except Exception as e:
        logger.error(f"Error al copiar plantilla: {e}")
        raise
