from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
import re


class Termino(BaseModel):
    """Modelo para términos y definiciones"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del término")
    definicion: str = Field(..., min_length=10, max_length=500, description="Definición del término")
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre_termino(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('El nombre del término no puede estar vacío')
        if len(v.strip()) < 2:
            raise ValueError('El nombre del término debe tener al menos 2 caracteres')
        return v.strip()
    
    @field_validator('definicion')
    @classmethod
    def validar_definicion(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('La definición no puede estar vacía')
        if len(v.strip()) < 10:
            raise ValueError('La definición debe tener al menos 10 caracteres')
        return v.strip()


class Condicion(BaseModel):
    """Modelo para condiciones generales"""
    descripcion: str = Field(..., min_length=10, max_length=1000, description="Descripción de la condición")
    
    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('La descripción de la condición no puede estar vacía')
        if len(v.strip()) < 10:
            raise ValueError('La descripción debe tener al menos 10 caracteres')
        return v.strip()


class Procedimiento(BaseModel):
    """
    Modelo Pydantic V2 para PROCEDIMIENTO con validaciones completas
    """
    
    # Configuración del modelo (V2)
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Auto-trim de espacios
        validate_assignment=True,    # Validar en asignación
        json_schema_extra={
            "example": {
                "codigo": "PROC-001-GAF",
                "version": "V1",
                "fecha": "2026-02-17",
                "nombre_proceso": "GESTIÓN ADMINISTRATIVA Y FINANCIERA",
                "denominacion": "PROCEDIMIENTO DE SELECCIÓN Y EVALUACIÓN DE PROVEEDORES",
                "objetivo": "Establecer los lineamientos necesarios para la selección y evaluación de proveedores",
                "alcance": "Aplica a todas las áreas de la organización que requieran adquirir bienes o servicios",
                "responsables": "Gestión Administrativa y Líderes de Proceso",
                "terminos": [
                    {
                        "nombre": "Proveedor",
                        "definicion": "Entidad externa que ofrece bienes o servicios a la organización"
                    }
                ],
                "condiciones": [
                    {
                        "descripcion": "Todas las áreas deben seguir este procedimiento sin excepción"
                    }
                ],
                "formatos_normas": "Formato FR-001-GAF, Norma ISO 9001:2015",
                "elaboro_nombre": "Juan Pérez",
                "elaboro_cargo": "Analista",
                "reviso_nombre": "María González",
                "reviso_cargo": "Coordinadora",
                "aprobo_nombre": "Carlos Ramírez",
                "aprobo_cargo": "Director"
            }
        }
    )

    
    # ========== IDENTIFICACIÓN ==========
    codigo: str = Field(
        ..., 
        min_length=8,
        max_length=50,
        description="Código del procedimiento. Formato: PROC-XXX-YYY",
        examples=["PROC-001-GAF", "PROC-023-TIC"]
    )
    
    version: str = Field(
        default="V1",
        min_length=2,
        max_length=10,
        description="Versión del documento. Formato: V + número",
        examples=["V1", "V2", "V10"]
    )
    
    fecha: str = Field(
        ...,
        description="Fecha del documento en formato YYYY-MM-DD",
        examples=["2026-02-17"]
    )
    
    # ========== INFORMACIÓN PRINCIPAL ==========
    nombre_proceso: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Nombre del proceso al que pertenece",
        examples=["GESTIÓN ADMINISTRATIVA Y FINANCIERA"]
    )
    
    denominacion: str = Field(
        ...,
        min_length=10,
        max_length=300,
        description="Denominación completa del procedimiento",
        examples=["PROCEDIMIENTO DE SELECCIÓN Y EVALUACIÓN DE PROVEEDORES"]
    )
    
    objetivo: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Objetivo del procedimiento (mínimo 20 caracteres)",
        examples=["Establecer los lineamientos para la selección de proveedores..."]
    )
    
    alcance: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Alcance del procedimiento (mínimo 20 caracteres)",
        examples=["Aplica a todas las áreas de la organización..."]
    )
    
    responsables: str = Field(
        ...,
        min_length=5,
        max_length=300,
        description="Responsables del procedimiento",
        examples=["Gestión Administrativa y Líderes de Proceso"]
    )
    
    area_realiza: Optional[str] = Field(
        default="",
        max_length=200,
        description="Área que realiza el procedimiento (aparece en el encabezado del documento)",
        examples=["GESTIÓN ADMINISTRATIVA"]
    )
    
    # ========== TÉRMINOS Y CONDICIONES ==========
    terminos: List[Termino] = Field(
        default_factory=list,
        description="Lista de términos y definiciones"
    )
    
    condiciones: List[Condicion] = Field(
        default_factory=list,
        description="Lista de condiciones generales"
    )
    
    # ========== FORMATOS Y NORMAS ==========
    formatos_normas: Optional[str] = Field(
        default="",
        max_length=2000,
        description="Formatos, normas y requisitos legales aplicables"
    )
    
    # ========== CONTROL DE REGISTROS ==========
    elaboro_nombre: Optional[str] = Field(default="", max_length=200)
    elaboro_cargo: Optional[str] = Field(default="", max_length=200)
    elaboro_fecha: Optional[str] = Field(default="")
    
    reviso_nombre: Optional[str] = Field(default="", max_length=200)
    reviso_cargo: Optional[str] = Field(default="", max_length=200)
    reviso_fecha: Optional[str] = Field(default="")
    
    aprobo_nombre: Optional[str] = Field(default="", max_length=200)
    aprobo_cargo: Optional[str] = Field(default="", max_length=200)
    aprobo_fecha: Optional[str] = Field(default="")
    
    descripcion_cambio: Optional[str] = Field(
        default="Versión inicial",
        max_length=500
    )
    
    # ========== VALIDADORES DE CAMPO (V2) ==========
    
    @field_validator('codigo')
    @classmethod
    def validar_codigo(cls, v: str) -> str:
        """Valida formato del código: PROC-XXX-YYY"""
        if not v:
            raise ValueError('El código es obligatorio')
        
        # Patrón: PROC-XXX-YYY (donde XXX son números y YYY son letras)
        patron = r'^PROC-\d{3}-[A-Z]{3,}$'
        
        if not re.match(patron, v.upper()):
            raise ValueError(
                'Formato inválido. Debe ser PROC-XXX-YYY '
                '(Ej: PROC-001-GAF, PROC-023-TIC)'
            )
        
        return v.upper()
    
    @field_validator('version')
    @classmethod
    def validar_version(cls, v: str) -> str:
        """Valida formato de versión: V + número"""
        if not v:
            raise ValueError('La versión es obligatoria')
        
        # Patrón: V seguido de número
        patron = r'^V\d+$'
        
        if not re.match(patron, v.upper()):
            raise ValueError(
                'Formato inválido. Debe ser V seguido de número '
                '(Ej: V1, V2, V10)'
            )
        
        return v.upper()
    
    @field_validator('fecha', 'elaboro_fecha', 'reviso_fecha', 'aprobo_fecha')
    @classmethod
    def validar_fecha(cls, v: str, info) -> str:
        """Valida formato de fecha y que no sea futura"""
        field_name = info.field_name
        
        if not v:
            # Solo es obligatorio el campo 'fecha'
            if field_name == 'fecha':
                raise ValueError('La fecha es obligatoria')
            return v
        
        try:
            fecha_obj = datetime.strptime(v, '%Y-%m-%d')
            
            # Validar que no sea fecha futura
            if fecha_obj > datetime.now():
                raise ValueError('La fecha no puede ser futura')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e):
                raise ValueError('Formato inválido. Debe ser YYYY-MM-DD (Ej: 2026-02-17)')
            raise
    
    @field_validator('nombre_proceso')
    @classmethod
    def validar_nombre_proceso(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('El nombre del proceso es obligatorio')
        if len(v.strip()) < 5:
            raise ValueError('El nombre del proceso debe tener al menos 5 caracteres')
        return v.strip().upper()
    
    @field_validator('denominacion')
    @classmethod
    def validar_denominacion(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('La denominación es obligatoria')
        if len(v.strip()) < 10:
            raise ValueError('La denominación debe tener al menos 10 caracteres')
        return v.strip()
    
    @field_validator('objetivo')
    @classmethod
    def validar_objetivo(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('El objetivo es obligatorio')
        if len(v.strip()) < 20:
            raise ValueError('El objetivo debe tener al menos 20 caracteres para ser descriptivo')
        return v.strip()
    
    @field_validator('alcance')
    @classmethod
    def validar_alcance(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('El alcance es obligatorio')
        if len(v.strip()) < 20:
            raise ValueError('El alcance debe tener al menos 20 caracteres para ser descriptivo')
        return v.strip()
    
    @field_validator('responsables')
    @classmethod
    def validar_responsables(cls, v: str) -> str:
        if not v or v.strip() == '':
            raise ValueError('Los responsables son obligatorios')
        if len(v.strip()) < 5:
            raise ValueError('Los responsables deben tener al menos 5 caracteres')
        return v.strip()
    
    # ========== VALIDADOR DE MODELO (V2) ==========
    
    @model_validator(mode='after')
    def validar_terminos_unicos(self) -> 'Procedimiento':
        """Valida que no haya términos duplicados"""
        if not self.terminos:
            return self
        
        nombres = [t.nombre.lower() for t in self.terminos]
        duplicados = [nombre for nombre in nombres if nombres.count(nombre) > 1]
        
        if duplicados:
            raise ValueError(f'Términos duplicados encontrados: {", ".join(set(duplicados))}')
        
        return self
