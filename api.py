from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pathlib import Path

from models.procedimiento import Procedimiento
from models.instructivo import Instructivo

# Importar funciones Word (principal)
from main import (
    ejecutar_procedimiento_word, 
    ejecutar_instructivo_word,
    ejecutar_procedimiento_excel,
    ejecutar_instructivo_excel
)

from config import Config
from utils.logger import configurar_logger

# Configurar logger
logger = configurar_logger("API")

# Validar plantillas al inicio
logger.info("🚀 Iniciando PGDI API v2.0 (Pydantic V2)...")
Config.validar_plantillas_excel()
Config.validar_plantillas_word()

# Crear aplicación FastAPI
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MANEJADOR DE ERRORES V2 ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Maneja errores de validación de Pydantic V2 y devuelve respuesta detallada
    """
    errores_detallados = []
    
    for error in exc.errors():
        # Extraer información del error (V2)
        campo_path = error.get('loc', ())
        campo = '.'.join(str(x) for x in campo_path if x != 'body')
        mensaje = error.get('msg', 'Error de validación')
        tipo_error = error.get('type', 'validation_error')
        
        # Obtener input (V2 usa 'input' en lugar de 'value')
        valor = error.get('input', None)
        
        # Traducir mensaje técnico a mensaje amigable
        if 'missing' in tipo_error or 'required' in mensaje.lower():
            mensaje_amigable = 'Este campo es obligatorio'
        elif 'string_too_short' in tipo_error:
            ctx = error.get('ctx', {})
            min_length = ctx.get('min_length', 0)
            actual = ctx.get('actual_length', 0)
            mensaje_amigable = f'Debe tener al menos {min_length} caracteres (actual: {actual})'
        elif 'string_too_long' in tipo_error:
            ctx = error.get('ctx', {})
            max_length = ctx.get('max_length', 0)
            mensaje_amigable = f'No debe exceder {max_length} caracteres'
        elif 'string_pattern_mismatch' in tipo_error:
            mensaje_amigable = mensaje
        elif 'value_error' in tipo_error:
            # Usar el mensaje personalizado del validator
            mensaje_amigable = mensaje
        else:
            mensaje_amigable = mensaje
        
        errores_detallados.append({
            'campo': campo,
            'valor': valor,
            'mensaje': mensaje_amigable,
            'tipo': tipo_error
        })
    
    logger.warning(f"⚠️ Validación fallida: {len(errores_detallados)} errores encontrados")
    
    return JSONResponse(
        status_code=422,
        content={
            'success': False,
            'error': 'Validación fallida',
            'mensaje': f'Se encontraron {len(errores_detallados)} errores en los datos enviados',
            'campos_invalidos': errores_detallados
        }
    )

# ==================== ENDPOINTS BÁSICOS ====================

@app.get("/")
def home():
    """Endpoint raíz"""
    logger.info("Acceso a endpoint raíz")
    return {
        "nombre": "PGDI - Plataforma de Gestión Documental Inteligente",
        "version": Config.API_VERSION,
        "status": "operativo",
        "pydantic": "V2",
        "formatos": ["Word (principal)", "PDF", "Excel (legacy)"],
        "endpoints": {
            "documentacion": "/docs",
            "procedimiento_word": "/generar-procedimiento-word",
            "instructivo_word": "/generar-instructivo-word",
            "procedimiento_excel": "/generar-procedimiento",
            "instructivo_excel": "/generar-instructivo",
            "contar": "/contar-documentos",
            "descargas": "/download/{tipo}/{archivo}"
        }
    }

@app.get("/health")
def health_check():
    """Verificación de salud del sistema"""
    import pydantic
    return {
        "status": "healthy",
        "pydantic_version": pydantic.__version__,
        "plantillas_excel": Config.validar_plantillas_excel(),
        "plantillas_word": Config.validar_plantillas_word()
    }

# ==================== WORD (PRINCIPAL) ====================

@app.post("/generar-procedimiento-word")
def generar_procedimiento_word(data: Procedimiento):
    """
    Genera un documento de PROCEDIMIENTO en formato WORD + PDF
    
    Args:
        data: Modelo Pydantic con los datos del procedimiento
        
    Returns:
        JSON con rutas de archivos generados
    """
    print(f"\n{'='*70}")
    print(f"🔵 PETICIÓN RECIBIDA: /generar-procedimiento-word")
    print(f"   Código: {data.codigo}")
    print(f"   Versión: {data.version}")
    print(f"   Denominación: {data.denominacion}")
    print(f"{'='*70}\n")
    
    logger.info(f"📥 [API-WORD] Solicitud recibida: Procedimiento {data.codigo}")
    
    try:
        # Ejecutar generación
        logger.info(f"🔄 [API-WORD] Iniciando ejecutar_procedimiento_word...")
        resultado = ejecutar_procedimiento_word(data.model_dump())
        logger.info(f"✅ [API-WORD] ejecutar_procedimiento_word completado")
        
        logger.info(f"✅ [WORD] Procedimiento generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Procedimiento generado exitosamente",
                "formato": "Word + PDF",
                "codigo": data.codigo,
                "version": data.version,
                "denominacion": data.denominacion,
                "archivos": {
                    "word": str(resultado['ruta_word'].name),
                    "pdf": str(resultado['ruta_pdf'].name),
                    "preview": str(resultado['ruta_preview'].name)
                },
                "rutas": {
                    "word": str(resultado['ruta_word']),
                    "pdf": str(resultado['ruta_pdf']),
                    "preview": f"/preview/{resultado['ruta_preview'].name}"
                }
            }
        )
        
    except FileNotFoundError as e:
        logger.error(f"❌ Plantilla no encontrada: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "Plantilla no encontrada",
                "mensaje": "Verifique que las plantillas Word estén en la carpeta correcta"
            }
        )
        
    except PermissionError as e:
        logger.error(f"❌ Error de permisos: {e}")
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "error": "Sin permisos",
                "mensaje": "No hay permisos para guardar en la carpeta de destino"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "mensaje": str(e)
            }
        )

@app.post("/generar-instructivo-word")
def generar_instructivo_word(data: Instructivo):
    """
    Genera un documento de INSTRUCTIVO en formato WORD + PDF
    
    Args:
        data: Modelo Pydantic con los datos del instructivo
        
    Returns:
        JSON con rutas de archivos generados
    """
    logger.info(f"📥 [WORD] Solicitud recibida: Instructivo {data.codigo}")
    
    try:
        # Ejecutar generación
        resultado = ejecutar_instructivo_word(data.model_dump())
        
        logger.info(f"✅ [WORD] Instructivo generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Instructivo generado exitosamente",
                "formato": "Word + PDF",
                "codigo": data.codigo,
                "version": data.version,
                "denominacion": data.denominacion,
                "actividades": len(data.actividades),
                "archivos": {
                    "word": str(resultado['ruta_word'].name),
                    "pdf": str(resultado['ruta_pdf'].name),
                    "preview": str(resultado['ruta_preview'].name)
                },
                "rutas": {
                    "word": str(resultado['ruta_word']),
                    "pdf": str(resultado['ruta_pdf']),
                    "preview": f"/preview/{resultado['ruta_preview'].name}"
                }
            }
        )
        
    except FileNotFoundError as e:
        logger.error(f"❌ Plantilla no encontrada: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "Plantilla no encontrada",
                "mensaje": "Verifique que las plantillas Word estén en la carpeta correcta"
            }
        )
        
    except PermissionError as e:
        logger.error(f"❌ Error de permisos: {e}")
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "error": "Sin permisos",
                "mensaje": "No hay permisos para guardar en la carpeta de destino"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "mensaje": str(e)
            }
        )

# ==================== EXCEL (LEGACY - MANTENER) ====================

@app.post("/generar-procedimiento")
def generar_procedimiento_excel(data: Procedimiento):
    """
    Genera un documento de PROCEDIMIENTO en formato EXCEL (legacy)
    
    Args:
        data: Modelo Pydantic con los datos del procedimiento
        
    Returns:
        JSON con resultado de la operación
    """
    logger.info(f"📥 [EXCEL] Solicitud recibida: Procedimiento {data.codigo}")
    
    try:
        # Ejecutar generación
        ruta = ejecutar_procedimiento_excel(data.model_dump())
        
        logger.info(f"✅ [EXCEL] Procedimiento generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Procedimiento Excel generado exitosamente",
                "formato": "Excel",
                "codigo": data.codigo,
                "denominacion": data.denominacion,
                "ruta": str(ruta),
                "archivo": ruta.name
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "mensaje": str(e)
            }
        )


@app.post("/generar-instructivo")
def generar_instructivo_excel(data: Instructivo):
    """
    Genera un documento de INSTRUCTIVO en formato EXCEL (legacy)
    
    Args:
        data: Modelo Pydantic con los datos del instructivo
        
    Returns:
        JSON con resultado de la operación
    """
    logger.info(f"📥 [EXCEL] Solicitud recibida: Instructivo {data.codigo}")
    
    try:
        # Ejecutar generación
        ruta = ejecutar_instructivo_excel(data.model_dump())
        
        logger.info(f"✅ [EXCEL] Instructivo generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Instructivo Excel generado exitosamente",
                "formato": "Excel",
                "codigo": data.codigo,
                "denominacion": data.denominacion,
                "ruta": str(ruta),
                "archivo": ruta.name,
                "actividades": len(data.actividades)
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "mensaje": str(e)
            }
        )

# ==================== VISTA PREVIA Y DESCARGAS ====================

@app.get("/preview/{nombre_archivo}")
def obtener_preview(nombre_archivo: str):
    """
    Sirve el PDF de preview para visualización en navegador
    
    Args:
        nombre_archivo: Nombre del archivo PDF en carpeta preview
        
    Returns:
        Archivo PDF
    """
    ruta_preview = Config.TEMP_PREVIEW_DIR / nombre_archivo
    
    if not ruta_preview.exists():
        logger.error(f"Preview no encontrado: {nombre_archivo}")
        raise HTTPException(status_code=404, detail="Preview no encontrado")
    
    logger.info(f"📄 Sirviendo preview: {nombre_archivo}")
    
    return FileResponse(
        path=str(ruta_preview),
        media_type="application/pdf",
        filename=nombre_archivo
    )

@app.get("/download/{tipo}/{nombre_archivo}")
def descargar_archivo(tipo: str, nombre_archivo: str):
    """
    Descarga archivo Word o PDF
    
    Args:
        tipo: 'word' o 'pdf'
        nombre_archivo: Nombre completo del archivo
        
    Returns:
        Archivo para descarga
    """
    # Buscar archivo en carpetas de salida
    # Por ahora búsqueda simple, después mejorar con base de datos
    
    if tipo not in ['word', 'pdf']:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'word' o 'pdf'")
    
    # Determinar extensión
    extension = '.docx' if tipo == 'word' else '.pdf'
    
    # Buscar en carpetas de salida
    for carpeta_tipo in ['procedimientos', 'instructivos']:
        # Buscar en todas las subcarpetas de año/mes
        for archivo in Config.SALIDAS_DIR.rglob(f"**/{carpeta_tipo}/*{extension}"):
            if archivo.name == nombre_archivo or nombre_archivo in archivo.name:
                logger.info(f"📥 Descargando: {archivo.name}")
                
                return FileResponse(
                    path=str(archivo),
                    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if tipo == 'word' else "application/pdf",
                    filename=archivo.name
                )
    
    logger.error(f"Archivo no encontrado: {nombre_archivo}")
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# ==================== UTILIDADES ====================

@app.get("/contar-documentos")
def contar_documentos():
    """Cuenta los documentos generados"""
    try:
        proc_count = len(list(Config.SALIDAS_DIR.rglob("**/procedimientos/*.xlsx"))) + \
                     len(list(Config.SALIDAS_DIR.rglob("**/procedimientos/*.docx")))
        
        inst_count = len(list(Config.SALIDAS_DIR.rglob("**/instructivos/*.xlsx"))) + \
                     len(list(Config.SALIDAS_DIR.rglob("**/instructivos/*.docx")))
        
        logger.info(f"📊 Conteo - Procedimientos: {proc_count}, Instructivos: {inst_count}")
        
        return {
            "procedimientos": proc_count,
            "instructivos": inst_count,
            "total": proc_count + inst_count
        }
    except Exception as e:
        logger.error(f"❌ Error al contar documentos: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "mensaje": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Iniciando servidor en {Config.API_HOST}:{Config.API_PORT}")
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
