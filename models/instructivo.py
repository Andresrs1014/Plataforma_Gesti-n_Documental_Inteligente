from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime
from utils.validators import ValidadorDatos

class ActividadInstructivo(BaseModel):
    """Modelo para una actividad del instructivo"""
    # 4 campos obligatorios y 1 opcional
    numero: int = Field(..., description="Número de la actividad")
    actividad: str = Field(..., min_length=3, description="Nombre de la actividad")
    descripcion: str = Field(..., min_length=10, description="Descripción detallada")
    responsable: str = Field(..., min_length=3, description="Responsable de ejecutarla")
    registro: Optional[str] = Field(default="N/A", description="Registro o documento asociado")

class Instructivo(BaseModel):
    """Modelo de datos para INSTRUCTIVO"""
    
    # Identificación
    # 2 campos obligatorios y 1 opcional
    codigo: str = Field(..., description="Código del instructivo (ej: INS-001-GAF)")
    version: str = Field(..., description="Versión (ej: V1)")
    fecha: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d")) # -> Importante no usasr datime.now() directamente para evitar problemas de serialización, usar lambda o método estático
    
    # Información principal
    nombre_proceso: str = Field(..., min_length=3)
    denominacion: str = Field(..., min_length=5)
    objetivo: str = Field(..., min_length=10)
    alcance: str = Field(..., min_length=10)
    responsables: str = Field(..., min_length=3)
    area_realiza: Optional[str] = Field(default="", description="Área que realiza el instructivo (encabezado del documento)")
    
    # Términos y definiciones
    terminos: Optional[Dict[str, str]] = Field(default_factory=dict)
    
    # Condiciones generales
    condiciones: Optional[List[str]] = Field(default_factory=list)
    
    # Matriz de actividades (PASO A PASO)
    actividades: List[ActividadInstructivo] = Field(..., min_length=1, description="Lista de actividades detalladas")
    
    # Control de registros
    elaboro_nombre: str = Field(..., min_length=3)
    elaboro_cargo: str = Field(..., min_length=3)
    elaboro_fecha: Optional[str] = None
    
    reviso_nombre: str = Field(..., min_length=3)
    reviso_cargo: str = Field(..., min_length=3)
    reviso_fecha: Optional[str] = None
    
    aprobo_nombre: str = Field(..., min_length=3)
    aprobo_cargo: str = Field(..., min_length=3)
    aprobo_fecha: Optional[str] = None
    
    # Validaciones (iguales a Procedimiento)
    @validator('codigo')
    def validar_codigo(cls, v):
        v = ValidadorDatos.normalizar_codigo(v)
        if not ValidadorDatos.validar_codigo(v):
            raise ValueError('Código inválido. Formato esperado: INS-000-XXX')
        return v
    
    @validator('version')
    def validar_version(cls, v):
        v = v.upper().strip()
        if not ValidadorDatos.validar_version(v):
            raise ValueError('Versión inválida. Formato esperado: V1, V2, etc.')
        return v
    
    @validator('fecha', 'elaboro_fecha', 'reviso_fecha', 'aprobo_fecha')
    def validar_fecha(cls, v):
        if v and not ValidadorDatos.validar_fecha(v):
            raise ValueError('Fecha inválida. Formato esperado: YYYY-MM-DD')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "codigo": "INS-004-GAF",
                "version": "V1",
                "fecha": "2026-02-13",
                "nombre_proceso": "GESTIÓN ADMINISTRATIVA",
                "denominacion": "INSTRUCTIVO MANEJO DE ARCHIVO",
                "objetivo": "Garantizar el debido manejo del archivo",
                "alcance": "Aplica a todas las áreas",
                "responsables": "Líderes de proceso",
                "actividades": [
                    {
                        "numero": 1,
                        "actividad": "Archivo activo",
                        "descripcion": "Organizar archivo activo en AZ debidamente marcado",
                        "responsable": "Líderes de proceso",
                        "registro": "Ubicación física o digital"
                    }
                ],
                "elaboro_nombre": "Liseth Pinzón",
                "elaboro_cargo": "Coordinador SIG",
                "reviso_nombre": "Sonia Gomez",
                "reviso_cargo": "Director Administrativo",
                "aprobo_nombre": "Juan Carlos Angarita",
                "aprobo_cargo": "Gerente General"
            }
        }
