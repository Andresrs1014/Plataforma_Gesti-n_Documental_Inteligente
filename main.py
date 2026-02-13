from datetime import datetime
from pathlib import Path
from config import Config
from excel.generador import crear_documento
from excel.formateador import llenar_procedimiento, llenar_instructivo
from utils.logger import configurar_logger

logger = configurar_logger("Main")

def ejecutar_procedimiento(datos: dict) -> Path:
    """
    Orquesta la generación de un procedimiento
    
    Args:
        datos: Diccionario con los datos del procedimiento
        
    Returns:
        Path del archivo generado
    """
    logger.info("=" * 60)
    logger.info(f"GENERANDO PROCEDIMIENTO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'PROC')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}.xlsx"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        
        # Crear documento desde plantilla
        ruta = crear_documento(
            nombre_archivo, 
            Config.SALIDAS_PROCEDIMIENTOS,
            Config.PLANTILLA_PROCEDIMIENTO
        )
        
        # Rellenar con datos
        llenar_procedimiento(ruta, datos)
        
        logger.info("=" * 60)
        logger.info(f"✅ PROCEDIMIENTO GENERADO: {ruta}")
        logger.info("=" * 60)
        
        return ruta
        
    except Exception as e:
        logger.error(f"❌ Error al generar procedimiento: {e}")
        raise

def ejecutar_instructivo(datos: dict) -> Path:
    """
    Orquesta la generación de un instructivo
    
    Args:
        datos: Diccionario con los datos del instructivo
        
    Returns:
        Path del archivo generado
    """
    logger.info("=" * 60)
    logger.info(f"GENERANDO INSTRUCTIVO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'INS')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}.xlsx"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        
        # Crear documento desde plantilla
        ruta = crear_documento(
            nombre_archivo,
            Config.SALIDAS_INSTRUCTIVOS,
            Config.PLANTILLA_INSTRUCTIVO
        )
        
        # Rellenar con datos
        llenar_instructivo(ruta, datos)
        
        logger.info("=" * 60)
        logger.info(f"✅ INSTRUCTIVO GENERADO: {ruta}")
        logger.info("=" * 60)
        
        return ruta
        
    except Exception as e:
        logger.error(f"❌ Error al generar instructivo: {e}")
        raise
