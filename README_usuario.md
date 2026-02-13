# 🚀 PGDI - Plataforma de Gestión Documental Inteligente

**Versión:** 1.0.0  
**Última actualización:** 13 de febrero de 2026

---

## 📑 TABLA DE CONTENIDO

1. [¿Qué es PGDI?](#qué-es-pgdi)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación Inicial](#instalación-inicial)
4. [Estructura de Carpetas](#estructura-de-carpetas)
5. [Configuración de Plantillas Excel](#configuración-de-plantillas-excel)
6. [Configuración de Mapeo de Celdas](#configuración-de-mapeo-de-celdas)
7. [Cómo Usar el Sistema](#cómo-usar-el-sistema)
8. [Solución de Problemas](#solución-de-problemas)
9. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 ¿QUÉ ES PGDI?

PGDI es un sistema web que **automatiza la creación de documentos corporativos** para su empresa.

### ¿Qué hace?
✅ Genera **PROCEDIMIENTOS** (documentos que explican QUÉ es un proceso)  
✅ Genera **INSTRUCTIVOS** (documentos que explican CÓMO se hace un proceso)  
✅ **Estandariza** el formato de todos los documentos  
✅ **Reduce el tiempo** de documentación de horas a minutos  

### ¿Para quién es?
👥 **Líderes de proceso** que necesitan documentar procedimientos  
👥 **Coordinadores SIG** que gestionan la documentación  
👥 **Personal administrativo** que necesita crear instructivos  

---

## 💻 REQUISITOS DEL SISTEMA

### Hardware Mínimo:
- Computador con Windows 7 o superior
- 2 GB de RAM
- 500 MB de espacio libre en disco

### Software Necesario:
- ✅ Microsoft Excel 2010 o superior (para crear las plantillas)
- ✅ Navegador web moderno (Chrome, Edge, Firefox)
- ✅ Python 3.8 o superior (se instala en el proceso)

### Conexiones:
- ✅ Acceso a la carpeta de red donde se guardarán los documentos
- ✅ Permisos de escritura en dicha carpeta

---

## 🛠️ INSTALACIÓN INICIAL

### Paso 1: Descargar el Sistema

Descargue la carpeta **PGDI** completa y colóquela en: C:\PGDI\


### Paso 2: Instalar Python

1. Descargue Python desde: https://www.python.org/downloads/
2. Durante la instalación, **MARQUE LA CASILLA**: ☑️ "Add Python to PATH"
3. Haga clic en "Install Now"
4. Espere a que termine la instalación

### Paso 3: Instalar Dependencias

1. Abra una ventana de **CMD** (Símbolo del sistema)
   - Presione `Windows + R`
   - Escriba: `cmd`
   - Presione Enter

2. Navegue a la carpeta del proyecto: cd C:\PGDI

3. Instale las librerías necesarias: pip install -r requirements.txt

4. Espere a que termine (puede tardar 2-3 minutos)

### Paso 4: Verificar Instalación

Ejecute este comando para verificar: python --version

Debe mostrar algo como: `Python 3.10.x`

---

## 📂 ESTRUCTURA DE CARPETAS

Después de la instalación, su carpeta PGDI debe verse así:

C:\PGDI
│
├── 📄 api.py ← Servidor de la aplicación
├── 📄 main.py ← Procesador de documentos
├── 📄 config.py ← Configuración (EDITAR AQUÍ)
├── 📄 requirements.txt ← Lista de dependencias
├── 📄 INICIAR.bat ← Doble clic para iniciar
│
├── 📁 excel/ ← Código de procesamiento Excel
│ ├── generador.py
│ └── formateador.py
│
├── 📁 models/ ← Definición de datos
│ ├── procedimiento.py
│ └── instructivo.py
│
├── 📁 utils/ ← Herramientas auxiliares
│ ├── logger.py
│ └── validators.py
│
├── 📁 plantillas/ ← 🔴 COLOQUE AQUÍ SUS PLANTILLAS EXCEL
│ ├── FORMATO_PROCEDIMIENTO.xlsx
│ └── FORMATO_INSTRUCTIVO.xlsx
│
├── 📁 mapping/ ← 🔴 CONFIGURE AQUÍ EL MAPEO DE CELDAS
│ ├── procedimiento_map.json
│ └── instructivo_map.json
│
├── 📁 frontend/ ← Formularios web
│ ├── index.html
│ ├── procedimiento.html
│ ├── instructivo.html
│ ├── styles.css
│ └── app.js
│
├── 📁 salidas/ ← AQUÍ SE GUARDAN LOS DOCUMENTOS GENERADOS
│ ├── procedimientos/
│ └── instructivos/
│
└── 📁 logs/ ← Registro de operaciones
└── pgdi_20260213.log


---

## 📊 CONFIGURACIÓN DE PLANTILLAS EXCEL

### Paso 1: Crear Sus Plantillas

1. Abra Microsoft Excel
2. Cree un documento con el formato deseado (logos, encabezados, tablas)
3. **NO LLENE NINGÚN DATO**, solo el diseño/estructura
4. Guarde el archivo con los nombres exactos:
   - `FORMATO_PROCEDIMIENTO.xlsx`
   - `FORMATO_INSTRUCTIVO.xlsx`

### Paso 2: Colocar Plantillas en la Carpeta

1. Copie sus archivos Excel
2. Péguelos en la carpeta: `C:\PGDI\plantillas\`

### Ejemplo Visual de Plantilla:

**FORMATO_PROCEDIMIENTO.xlsx debe verse así:**

┌─────────────────────────────────────────────────────┐
│ [LOGO] PROCEDIMIENTO - [PROCESO] [CÓDIGO] │
├─────────────────────────────────────────────────────┤
│ │
│ 1. DENOMINACIÓN DEL PROCESO: │
│ [Se llenará automáticamente] │
│ │
│ 2. DENOMINACIÓN DEL DOCUMENTO: │
│ [Se llenará automáticamente] │
│ │
│ 3. OBJETIVO: │
│ [Se llenará automáticamente] │
│ │
│ 4. ALCANCE: │
│ [Se llenará automáticamente] │
│ │
│ 5. RESPONSABLES: │
│ [Se llenará automáticamente] │
│ │
├─────────────────────────────────────────────────────┤
│ CONTROL DE REGISTROS │
├──────────────┬──────────────┬──────────────────────┤
│ ELABORÓ │ REVISÓ │ APROBÓ │
├──────────────┼──────────────┼──────────────────────┤
│ [Nombre] │ [Nombre] │ [Nombre] │
│ [Cargo] │ [Cargo] │ [Cargo] │
│ [Fecha] │ [Fecha] │ [Fecha] │
└──────────────┴──────────────┴──────────────────────┘


### ⚠️ IMPORTANTE:

- ✅ **SÍ** use colores, logos, bordes, estilos
- ✅ **SÍ** organice las celdas como desee
- ❌ **NO** llene ningún dato en las celdas que se rellenarán automáticamente
- ❌ **NO** use macros o fórmulas complejas

---

## 🗺️ CONFIGURACIÓN DE MAPEO DE CELDAS

### ¿Qué es el Mapeo?

El **mapeo** le indica al sistema **en qué celda de Excel** debe escribir cada dato.

### Paso 1: Identificar las Celdas

1. Abra su plantilla `FORMATO_PROCEDIMIENTO.xlsx`
2. Identifique **qué celda** corresponde a **qué dato**

**Ejemplo:**
- El código del documento está en celda: `A1`
- El nombre del proceso está en celda: `B5`
- El objetivo está en celda: `B10`
- Etc.

### Paso 2: Crear el Archivo de Mapeo

1. Navegue a la carpeta: `C:\PGDI\mapping\`
2. Abra el archivo: `procedimiento_map.json` con Bloc de Notas
3. Edite las celdas según su plantilla

### Formato del Archivo JSON:

```json
{
  "codigo": "A1",
  "version": "E1",
  "fecha": "G1",
  "nombre_proceso": "B5",
  "denominacion": "B7",
  "objetivo": "B10",
  "alcance": "B13",
  "responsables": "B16",
  "elaboro_nombre": "B40",
  "elaboro_cargo": "C40",
  "elaboro_fecha": "D40",
  "reviso_nombre": "B41",
  "reviso_cargo": "C41",
  "reviso_fecha": "D41",
  "aprobo_nombre": "B42",
  "aprobo_cargo": "C42",
  "aprobo_fecha": "D42"
}

🎮 CÓMO USAR EL SISTEMA
Paso 1: Iniciar el Servidor
Navegue a la carpeta: C:\PGDI\

Haga doble clic en el archivo: INICIAR.bat

Verá una ventana negra con texto similar a:

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.


NO CIERRE ESTA VENTANA mientras use el sistema

Paso 2: Abrir el Sistema en el Navegador
Abra su navegador web (Chrome, Edge, Firefox)

En la barra de direcciones escriba: http://localhost:8000

Paso 3: Crear un Documento
Opción A: Crear un PROCEDIMIENTO
En la página principal, haga clic en: "Crear Procedimiento"

Llene el formulario con los datos:

Código: PROC-001-GAF (formato: XXX-000-XXX)

Versión: V1

Nombre del Proceso: GESTIÓN ADMINISTRATIVA

Denominación: PROCEDIMIENTO CONTROL DOCUMENTAL

Objetivo: Establecer los lineamientos...

Alcance: Aplica a todas las áreas...

Responsables: Líderes de proceso

Elaboró - Nombre: Juan Pérez

Elaboró - Cargo: Coordinador SIG

Revisó - Nombre: María García

Revisó - Cargo: Director Administrativo

Aprobó - Nombre: Carlos López

Aprobó - Cargo: Gerente General

Haga clic en: "Generar Procedimiento"

Verá un mensaje de confirmación: ✅ "Procedimiento generado exitosamente"

Opción B: Crear un INSTRUCTIVO
En la página principal, haga clic en: "Crear Instructivo"

Llene el formulario (similar al procedimiento)

Agregue las actividades paso a paso en la sección correspondiente

Haga clic en: "Generar Instructivo"

Paso 4: Encontrar Su Documento
Los documentos generados se guardan automáticamente en:

C:\PGDI\salidas\procedimientos\     ← Procedimientos
C:\PGDI\salidas\instructivos\       ← Instructivos

Nombre del archivo:

PROC-001-GAF_PROCEDIMIENTO_CONTROL_DOCUMENTAL_20260213_093015.xlsx
└───┬───┘ └──────────┬──────────────────┘ 
  Código          Denominación              Fecha      Hora


Paso 5: Detener el Servidor (Cuando Termine)
Vaya a la ventana negra (CMD) que dejó abierta

Presione: CTRL + C

Confirme con: S (Sí)

Cierre la ventana