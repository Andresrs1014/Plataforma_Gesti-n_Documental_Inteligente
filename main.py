from datetime import datetime
from pathlib import Path
from config import Config

# Excel (mantener)
from excel.generador import crear_documento as crear_documento_excel
from excel.formateador import llenar_procedimiento as llenar_procedimiento_excel
from excel.formateador import llenar_instructivo as llenar_instructivo_excel

# Word (nuevo)
from word.generador import crear_documento as crear_documento_word
from word.formateador import llenar_procedimiento as llenar_procedimiento_word
from word.formateador import llenar_instructivo as llenar_instructivo_word

# PDF (nuevo)
from pdf.conversor import word_a_pdf, crear_preview_pdf

from utils.logger import configurar_logger

logger = configurar_logger("Main")

# ==================== EXCEL (MANTENER) ====================

def ejecutar_procedimiento_excel(datos: dict) -> Path:
    """
    Orquesta la generación de un procedimiento EN EXCEL
    
    Args:
        datos: Diccionario con los datos del procedimiento
        
    Returns:
        Path del archivo Excel generado
    """
    logger.info("=" * 60)
    logger.info(f"[EXCEL] GENERANDO PROCEDIMIENTO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'PROC')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}.xlsx"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        
        # Obtener ruta de salida organizada por fecha
        carpeta_salida = Config.obtener_ruta_salida('procedimientos')
        
        # Crear documento desde plantilla
        ruta = crear_documento_excel(
            nombre_archivo, 
            carpeta_salida,
            Config.PLANTILLA_PROCEDIMIENTO_EXCEL
        )
        
        # Rellenar con datos
        llenar_procedimiento_excel(ruta, datos)
        
        logger.info("=" * 60)
        logger.info(f"✅ [EXCEL] PROCEDIMIENTO GENERADO: {ruta}")
        logger.info("=" * 60)
        
        return ruta
        
    except Exception as e:
        logger.error(f"❌ Error al generar procedimiento Excel: {e}")
        raise

def ejecutar_instructivo_excel(datos: dict) -> Path:
    """
    Orquesta la generación de un instructivo EN EXCEL
    
    Args:
        datos: Diccionario con los datos del instructivo
        
    Returns:
        Path del archivo Excel generado
    """
    logger.info("=" * 60)
    logger.info(f"[EXCEL] GENERANDO INSTRUCTIVO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'INS')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}.xlsx"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        
        # Obtener ruta de salida organizada por fecha
        carpeta_salida = Config.obtener_ruta_salida('instructivos')
        
        # Crear documento desde plantilla
        ruta = crear_documento_excel(
            nombre_archivo,
            carpeta_salida,
            Config.PLANTILLA_INSTRUCTIVO_EXCEL
        )
        
        # Rellenar con datos
        llenar_instructivo_excel(ruta, datos)
        
        logger.info("=" * 60)
        logger.info(f"✅ [EXCEL] INSTRUCTIVO GENERADO: {ruta}")
        logger.info("=" * 60)
        
        return ruta
        
    except Exception as e:
        logger.error(f"❌ Error al generar instructivo Excel: {e}")
        raise

# ==================== WORD (NUEVO - PRINCIPAL) ====================

def ejecutar_procedimiento_word(datos: dict) -> dict:
    """
    Orquesta la generación de un procedimiento EN WORD + PDF
    
    Args:
        datos: Diccionario con los datos del procedimiento
        
    Returns:
        Dict con rutas de archivos generados
    """
    print(f"\n{'-'*70}")
    print(f"[MAIN] EJECUTANDO PROCEDIMIENTO WORD")
    print(f"[MAIN] Código: {datos.get('codigo', 'N/A')}")
    print(f"{'-'*70}\n")
    
    logger.info("=" * 60)
    logger.info(f"[WORD] GENERANDO PROCEDIMIENTO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'PROC')
        version = datos.get('version', 'V1')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}_{version}"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        
        # Obtener ruta de salida organizada por fecha
        carpeta_salida = Config.obtener_ruta_salida('procedimientos')
        
        # PASO 1: Crear documento Word desde plantilla
        ruta_word = crear_documento_word(
            nombre_archivo, 
            carpeta_salida,
            Config.PLANTILLA_PROCEDIMIENTO_WORD
        )
        
        # PASO 2: Rellenar Word con datos
        llenar_procedimiento_word(ruta_word, datos)
        
        # PASO 3: Convertir a PDF
        ruta_pdf = word_a_pdf(ruta_word)
        
        # PASO 4: Crear PDF de preview (copia en carpeta temporal)
        ruta_preview = crear_preview_pdf(ruta_pdf)
        
        resultado = {
            'ruta_word': ruta_word,
            'ruta_pdf': ruta_pdf,
            'ruta_preview': ruta_preview,
            'codigo': codigo,
            'version': version,
            'tipo': 'procedimiento'
        }
        
        logger.info("=" * 60)
        logger.info(f"✅ [WORD] PROCEDIMIENTO GENERADO:")
        logger.info(f"   Word: {ruta_word.name}")
        logger.info(f"   PDF:  {ruta_pdf.name}")
        logger.info("=" * 60)
        
        return resultado
        
    except Exception as e:
        logger.error(f"❌ Error al generar procedimiento Word: {e}")
        raise

def ejecutar_instructivo_word(datos: dict) -> dict:
    """
    Orquesta la generación de un instructivo EN WORD + PDF
    
    Args:
        datos: Diccionario con los datos del instructivo
        
    Returns:
        Dict con rutas de archivos generados
    """
    logger.info("=" * 60)
    logger.info(f"[WORD] GENERANDO INSTRUCTIVO: {datos.get('codigo', 'N/A')}")
    logger.info("=" * 60)
    
    try:
        # Generar nombre de archivo
        codigo = datos.get('codigo', 'INS')
        version = datos.get('version', 'V1')
        denominacion = datos.get('denominacion', 'documento').replace(' ', '_')
        nombre_archivo = f"{codigo}_{denominacion}_{version}"
        
        logger.info(f"Nombre archivo: {nombre_archivo}")
        logger.info(f"Actividades: {len(datos.get('actividades', []))}")
        
        # Obtener ruta de salida organizada por fecha
        carpeta_salida = Config.obtener_ruta_salida('instructivos')
        
        # PASO 1: Crear documento Word desde plantilla
        ruta_word = crear_documento_word(
            nombre_archivo,
            carpeta_salida,
            Config.PLANTILLA_INSTRUCTIVO_WORD
        )
        
        # PASO 2: Rellenar Word con datos
        llenar_instructivo_word(ruta_word, datos)
        
        # PASO 3: Convertir a PDF
        ruta_pdf = word_a_pdf(ruta_word)
        
        # PASO 4: Crear PDF de preview (copia en carpeta temporal)
        ruta_preview = crear_preview_pdf(ruta_pdf)
        
        resultado = {
            'ruta_word': ruta_word,
            'ruta_pdf': ruta_pdf,
            'ruta_preview': ruta_preview,
            'codigo': codigo,
            'version': version,
            'tipo': 'instructivo',
            'actividades': len(datos.get('actividades', []))
        }
        
        logger.info("=" * 60)
        logger.info(f"✅ [WORD] INSTRUCTIVO GENERADO:")
        logger.info(f"   Word: {ruta_word.name}")
        logger.info(f"   PDF:  {ruta_pdf.name}")
        logger.info(f"   Actividades: {resultado['actividades']}")
        logger.info("=" * 60)
        
        return resultado
        
    except Exception as e:
        logger.error(f"❌ Error al generar instructivo Word: {e}")
        raise
