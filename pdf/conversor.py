from pathlib import Path
from docx2pdf import convert
from config import Config
from utils.logger import configurar_logger
from typing import Optional
import shutil

logger = configurar_logger("PDF-Conversor")

def word_a_pdf(ruta_word: Path, ruta_pdf: Optional[Path] = None) -> Path:
    """
    Convierte un archivo Word (.docx) a PDF
    
    Args:
        ruta_word: Path del archivo Word a convertir
        ruta_pdf: Path donde guardar el PDF (si None, usa misma ubicación)
        
    Returns:
        Path del archivo PDF generado
        
    Raises:
        FileNotFoundError: Si el archivo Word no existe
        Exception: Si falla la conversión
    """
    logger.info(f"[PDF] Iniciando conversión Word → PDF: {ruta_word.name}")
    
    # Validar que archivo Word existe
    if not ruta_word.exists():
        logger.error(f"Archivo Word no encontrado: {ruta_word}")
        raise FileNotFoundError(f"Archivo no existe: {ruta_word}")
    
    # Si no se especifica ruta PDF, usar misma carpeta con extensión .pdf
    if ruta_pdf is None:
        ruta_pdf = ruta_word.with_suffix('.pdf')
    
    try:
        # Convertir Word a PDF
        convert(str(ruta_word), str(ruta_pdf))
        
        logger.info(f"✅ [PDF] Conversión exitosa: {ruta_pdf.name}")
        return ruta_pdf
        
    except Exception as e:
        logger.error(f"❌ Error al convertir Word a PDF: {e}")
        raise

def crear_preview_pdf(ruta_pdf_original: Path) -> Path:
    """
    Crea una copia del PDF en la carpeta preview para vista previa
    
    Args:
        ruta_pdf_original: Path del archivo PDF ya generado
        
    Returns:
        Path del PDF de preview
    """
    logger.info(f"[PDF] Creando preview: {ruta_pdf_original.name}")
    
    # Validar que el PDF original existe
    if not ruta_pdf_original.exists():
        logger.error(f"PDF original no encontrado: {ruta_pdf_original}")
        raise FileNotFoundError(f"PDF no existe: {ruta_pdf_original}")
    
    # Nombre del archivo preview
    nombre_preview = f"preview_{ruta_pdf_original.stem}.pdf"
    ruta_preview = Config.TEMP_PREVIEW_DIR / nombre_preview
    
    # Asegurar que carpeta preview existe
    Config.TEMP_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Copiar PDF en lugar de re-convertir
        shutil.copy2(ruta_pdf_original, ruta_preview)
        logger.info(f"✅ [PDF] Preview creado: {ruta_preview.name}")
        return ruta_preview
    except Exception as e:
        logger.error(f"❌ Error al crear preview: {e}")
        raise
