from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pathlib import Path

from models.procedimiento import Procedimiento
from models.instructivo import Instructivo

from main import (
    ejecutar_instructivo,
    ejecutar_procedimiento_excel,
    ejecutar_instructivo_excel
)

from config import Config
from utils.logger import configurar_logger

logger = configurar_logger("API")

logger.info("🚀 Iniciando PGDI API v2.1 (plantilla única INSTRUCTIVO)...")
Config.validar_plantillas_excel()
Config.validar_plantillas_word()

app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION
)

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
    errores_detallados = []

    for error in exc.errors():
        campo_path = error.get('loc', ())
        campo = '.'.join(str(x) for x in campo_path if x != 'body')
        mensaje = error.get('msg', 'Error de validación')
        tipo_error = error.get('type', 'validation_error')
        valor = error.get('input', None)

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
    return {
        "nombre": "PGDI - Plataforma de Gestión Documental Inteligente",
        "version": Config.API_VERSION,
        "status": "operativo",
        "pydantic": "V2",
        "plantilla": "INSTRUCTIVO (única)",
        "endpoints": {
            "documentacion": "/docs",
            "generar_word": "/generar-instructivo-word",
            "procedimiento_excel": "/generar-procedimiento",
            "instructivo_excel": "/generar-instructivo",
            "preview": "/preview/{archivo}",
            "descargar": "/download/{tipo}/{archivo}",
            "contar": "/contar-documentos"
        }
    }

@app.get("/health")
def health_check():
    import pydantic
    return {
        "status": "healthy",
        "pydantic_version": pydantic.__version__,
        "plantilla_word": Config.validar_plantillas_word(),
        "plantillas_excel": Config.validar_plantillas_excel()
    }

# ==================== WORD (PRINCIPAL - ENDPOINT ÚNICO) ====================

@app.post("/generar-instructivo-word")
def generar_instructivo_word(data: Procedimiento):
    """
    Genera un documento en WORD + PDF usando la plantilla única INSTRUCTIVO.docx
    Acepta el modelo Procedimiento (campos completos con validaciones)
    """
    print(f"\n{'='*70}")
    print(f"🔵 PETICIÓN RECIBIDA: /generar-instructivo-word")
    print(f"   Código:       {data.codigo}")
    print(f"   Versión:      {data.version}")
    print(f"   Denominación: {data.denominacion}")
    print(f"{'='*70}\n")

    logger.info(f"📥 [API-WORD] Solicitud recibida: {data.codigo} - {data.denominacion}")

    try:
        resultado = ejecutar_instructivo(data.model_dump())
        logger.info(f"✅ [WORD] Documento generado: {data.codigo}")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Instructivo generado exitosamente",
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
                "mensaje": "Verifique que INSTRUCTIVO.docx esté en plantillas/word/"
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
    """Genera un PROCEDIMIENTO en formato EXCEL (legacy)"""
    logger.info(f"📥 [EXCEL] Solicitud recibida: Procedimiento {data.codigo}")
    try:
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
            detail={"success": False, "error": "Error interno", "mensaje": str(e)}
        )

@app.post("/generar-instructivo")
def generar_instructivo_excel(data: Instructivo):
    """Genera un INSTRUCTIVO en formato EXCEL (legacy)"""
    logger.info(f"📥 [EXCEL] Solicitud recibida: Instructivo {data.codigo}")
    try:
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
                "archivo": ruta.name
            }
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Error interno", "mensaje": str(e)}
        )

# ==================== PREVIEW (INLINE - ABRE EN NAVEGADOR) ====================

@app.get("/preview/{nombre_archivo}")
def obtener_preview(nombre_archivo: str):
    """
    Sirve el PDF para visualización INLINE en el navegador
    ✅ Content-Disposition: inline → abre en el navegador, no descarga
    """
    ruta_preview = Config.TEMP_PREVIEW_DIR / nombre_archivo

    if not ruta_preview.exists():
        logger.error(f"Preview no encontrado: {nombre_archivo}")
        raise HTTPException(status_code=404, detail="Preview no encontrado")

    logger.info(f"📄 Sirviendo preview inline: {nombre_archivo}")

    return FileResponse(
        path=str(ruta_preview),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={nombre_archivo}"
        }
    )

# ==================== DESCARGAS ====================

@app.get("/download/{tipo}/{nombre_archivo}")
def descargar_archivo(tipo: str, nombre_archivo: str):
    """Descarga archivo Word o PDF"""
    if tipo not in ['word', 'pdf']:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'word' o 'pdf'")

    extension = '.docx' if tipo == 'word' else '.pdf'

    for carpeta_tipo in ['procedimientos', 'instructivos']:
        for archivo in Config.SALIDAS_DIR.rglob(f"**/{carpeta_tipo}/*{extension}"):
            if archivo.name == nombre_archivo or nombre_archivo in archivo.name:
                logger.info(f"📥 Descargando: {archivo.name}")
                return FileResponse(
                    path=str(archivo),
                    media_type=(
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        if tipo == 'word' else "application/pdf"
                    ),
                    headers={
                        "Content-Disposition": f"attachment; filename={archivo.name}"
                    }
                )

    logger.error(f"Archivo no encontrado: {nombre_archivo}")
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# ==================== UTILIDADES ====================

@app.get("/contar-documentos")
def contar_documentos():
    """Cuenta los documentos generados"""
    try:
        inst_word = len(list(Config.SALIDAS_DIR.rglob("**/instructivos/*.docx")))
        inst_pdf  = len(list(Config.SALIDAS_DIR.rglob("**/instructivos/*.pdf")))
        inst_xlsx = len(list(Config.SALIDAS_DIR.rglob("**/instructivos/*.xlsx")))
        proc_xlsx = len(list(Config.SALIDAS_DIR.rglob("**/procedimientos/*.xlsx")))

        logger.info(f"📊 Conteo - Instructivos: {inst_word + inst_pdf + inst_xlsx}, Procedimientos (Excel): {proc_xlsx}")

        return {
            "instructivos": {
                "word": inst_word,
                "pdf": inst_pdf,
                "excel": inst_xlsx
            },
            "procedimientos_excel": proc_xlsx,
            "total": inst_word + inst_pdf + inst_xlsx + proc_xlsx
        }

    except Exception as e:
        logger.error(f"❌ Error al contar documentos: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Error interno", "mensaje": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Iniciando servidor en {Config.API_HOST}:{Config.API_PORT}")
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
