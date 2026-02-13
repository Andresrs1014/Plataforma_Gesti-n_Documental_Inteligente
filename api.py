from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.procedimiento import Procedimiento
from models.instructivo import Instructivo
from main import ejecutar_procedimiento, ejecutar_instructivo
from config import Config
from utils.logger import configurar_logger

# Configurar logger
logger = configurar_logger("API")

# Validar plantillas al inicio
logger.info("Iniciando PGDI API...")
Config.validar_plantillas()

# Crear aplicación FastAPI
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    """Endpoint raíz"""
    logger.info("Acceso a endpoint raíz")
    return {
        "mensaje": "PGDI - Plataforma de Gestión Documental Inteligente",
        "version": Config.API_VERSION,
        "status": "operativo",
        "endpoints": {
            "documentacion": "/docs",
            "procedimiento": "/generar-procedimiento",
            "instructivo": "/generar-instructivo"
        }
    }

@app.get("/health")
def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "plantillas": Config.validar_plantillas()
    }

@app.post("/generar-procedimiento")
def generar_procedimiento(data: Procedimiento):
    """
    Genera un documento de PROCEDIMIENTO
    
    Args:
        data: Modelo Pydantic con los datos del procedimiento
        
    Returns:
        JSON con el resultado de la operación
    """
    logger.info(f"📥 Solicitud recibida: Procedimiento {data.codigo}")
    
    try:
        # Ejecutar generación
        ruta = ejecutar_procedimiento(data.dict())
        
        logger.info(f"✅ Procedimiento generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Procedimiento generado exitosamente",
                "codigo": data.codigo,
                "denominacion": data.denominacion,
                "ruta": str(ruta),
                "archivo": ruta.name
            }
        )
        
    except FileNotFoundError as e:
        logger.error(f"❌ Plantilla no encontrada: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "Plantilla no encontrada",
                "mensaje": "Verifique que las plantillas Excel estén en la carpeta correcta"
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

@app.post("/generar-instructivo")
def generar_instructivo(data: Instructivo):
    """
    Genera un documento de INSTRUCTIVO
    
    Args:
        data: Modelo Pydantic con los datos del instructivo
        
    Returns:
        JSON con el resultado de la operación
    """
    logger.info(f"📥 Solicitud recibida: Instructivo {data.codigo}")
    
    try:
        # Ejecutar generación
        ruta = ejecutar_instructivo(data.dict())
        
        logger.info(f"✅ Instructivo generado: {data.codigo}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mensaje": "Instructivo generado exitosamente",
                "codigo": data.codigo,
                "denominacion": data.denominacion,
                "ruta": str(ruta),
                "archivo": ruta.name,
                "actividades": len(data.actividades)
            }
        )
        
    except FileNotFoundError as e:
        logger.error(f"❌ Plantilla no encontrada: {e}")
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "Plantilla no encontrada",
                "mensaje": "Verifique que las plantillas Excel estén en la carpeta correcta"
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

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Iniciando servidor en {Config.API_HOST}:{Config.API_PORT}")
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
