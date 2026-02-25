import logging
from pathlib import Path
from config import Config

def configurar_logger(nombre: str) -> logging.Logger:
    """
    Configura un logger con formato empresarial
    
    Args:
        nombre: Nombre del módulo que usa el logger
        
    Returns:
        Logger configurado
    """
    
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    
    # Limpiar handlers existentes para evitar duplicados
    logger.handlers.clear()
    
    # Asegurar que el logger no use el handler del root logger
    logger.propagate = False
    
    # Formato profesional -> Configura el formato del log para que cualquier modificación futura sea consistente
    formato = logging.Formatter(
        '%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s | %(lineno)d',
        datefmt='%Y-%m-%d %H:%M:%S'
    ) 
    
    # Handler para archivo
    try:
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"⚠️  No se pudo crear archivo de log: {e}")
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)
    
    return logger
