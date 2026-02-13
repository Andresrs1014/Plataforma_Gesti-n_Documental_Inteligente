from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime
from utils.validators import ValidadorDatos

class Procedimiento(BaseModel):
    """Modelo de datos para PROCEDIMIENTO"""
    
    # Identificación
    codigo: str = Field(..., description="Código del procedimiento (ej: PROC-001-GAF)")
    version: str = Field(..., description="Versión (ej: V1)")
    fecha: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    # Información principal
    nombre_proceso: str = Field(..., min_length=3, description="Nombre del proceso")
    denominacion: str = Field(..., min_length=5, description="Denominación del documento")
    objetivo: str = Field(..., min_length=10, description="Objetivo del procedimiento")
    alcance: str = Field(..., min_length=10, description="Alcance del procedimiento")
    responsables: str = Field(..., min_length=3, description="Responsables")
    
    # Términos y definiciones (opcional)
    terminos: Optional[Dict[str, str]] = Field(default_factory=dict, description="Diccionario de términos")
    
    # Condiciones generales (opcional)
    condiciones: Optional[List[str]] = Field(default_factory=list, description="Lista de condiciones")
    
    # Control de registros
    elaboro_nombre: str = Field(..., min_length=3, description="Nombre quien elaboró")
    elaboro_cargo: str = Field(..., min_length=3, description="Cargo quien elaboró")
    elaboro_fecha: Optional[str] = Field(default=None, description="Fecha elaboración")
    
    reviso_nombre: str = Field(..., min_length=3, description="Nombre quien revisó")
    reviso_cargo: str = Field(..., min_length=3, description="Cargo quien revisó")
    reviso_fecha: Optional[str] = Field(default=None, description="Fecha revisión")
    
    aprobo_nombre: str = Field(..., min_length=3, description="Nombre quien aprobó")
    aprobo_cargo: str = Field(..., min_length=3, description="Cargo quien aprobó")
    aprobo_fecha: Optional[str] = Field(default=None, description="Fecha aprobación")
    
    # Validaciones
    @validator('codigo')
    def validar_codigo(cls, v):
        """Valida y normaliza el código"""
        v = ValidadorDatos.normalizar_codigo(v)
        if not ValidadorDatos.validar_codigo(v):
            raise ValueError('Código inválido. Formato esperado: XXX-000-XXX (ej: PROC-001-GAF)')
        return v
    
    @validator('version')
    def validar_version(cls, v):
        """Valida y normaliza la versión"""
        v = v.upper().strip()
        if not ValidadorDatos.validar_version(v):
            raise ValueError('Versión inválida. Formato esperado: V1, V2, V3, etc.')
        return v
    
    @validator('fecha', 'elaboro_fecha', 'reviso_fecha', 'aprobo_fecha')
    def validar_fecha(cls, v):
        """Valida formato de fecha"""
        if v and not ValidadorDatos.validar_fecha(v):
            raise ValueError('Fecha inválida. Formato esperado: YYYY-MM-DD (ej: 2026-02-13)')
        return v
    
    @validator('nombre_proceso', 'denominacion', 'objetivo', 'alcance', 'responsables')
    def limpiar_textos(cls, v):
        """Limpia espacios en blanco"""
        return ValidadorDatos.limpiar_texto(v)
    
    class Config:
        schema_extra = {
            "example": {
                "codigo": "PROC-001-GAF",
                "version": "V1",
                "fecha": "2026-02-13",
                "nombre_proceso": "GESTIÓN ADMINISTRATIVA",
                "denominacion": "PROCEDIMIENTO CONTROL DE DOCUMENTOS",
                "objetivo": "Establecer lineamientos para el control documental",
                "alcance": "Aplica a todas las áreas de la empresa",
                "responsables": "Líderes de proceso",
                "elaboro_nombre": "Juan Pérez",
                "elaboro_cargo": "Coordinador SIG",
                "reviso_nombre": "María García",
                "reviso_cargo": "Director Administrativo",
                "aprobo_nombre": "Carlos López",
                "aprobo_cargo": "Gerente General"
            }
        }
