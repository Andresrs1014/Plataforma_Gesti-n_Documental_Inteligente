# Plataforma de Gestión Documental Inteligente (PGDI)

Sistema para la generación automatizada de documentos procedimentales e instructivos en formato estandarizado.

## 📋 Descripción

PGDI es una plataforma web que permite crear y generar documentos procedimentales e instructivos de manera estandarizada, utilizando plantillas Excel predefinidas. El sistema cuenta con una interfaz web intuitiva y una API REST para la generación de documentos.

## 🚀 Características

- Generación automatizada de procedimientos
- Generación automatizada de instructivos
- Interfaz web intuitiva
- API REST para integración con otros sistemas
- Formateo estandarizado de documentos
- Exportación a formato Excel

## 🛠️ Tecnologías

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Procesamiento**: openpyxl para manejo de archivos Excel

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd Plataforma_Gestión_Documental_Inteligente
```

2. Crea un entorno virtual de Python:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```

4. Instala las dependencias:
```bash
pip install fastapi uvicorn openpyxl python-multipart
```

## 🖥️ Uso

### Iniciar el servidor

```bash
python -m uvicorn api:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

### Acceder a la interfaz web

Abre en tu navegador:
- Procedimientos: `http://localhost:8000/frontend/prodecimiento.html`
- Instructivos: `http://localhost:8000/frontend/instructivo.html`

### Documentación de la API

FastAPI genera documentación automática:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Estructura del Proyecto

```
Plataforma_Gestión_Documental_Inteligente/
├── api.py                  # API REST con FastAPI
├── main.py                 # Funciones principales
├── excel/                  # Módulo de procesamiento Excel
│   ├── generador.py       # Generación de documentos
│   └── formateador.py     # Formateo de celdas
├── frontend/              # Interfaz web
│   ├── index.html
│   ├── prodecimiento.html
│   ├── instructivo.html
│   ├── app.js
│   └── styles.css
├── plantillas/            # Plantillas Excel (agregar aquí)
└── salidas/               # Documentos generados (ignorado en git)
```

## 📝 Nota sobre Plantillas

Las plantillas Excel deben colocarse en la carpeta `plantillas/`:
- `FORMATO_PROCEDIMIENTO.xlsx`
- `FORMATO_INSTRUCTIVO.xlsx`

Estos archivos no están incluidos en el repositorio. Solicítalos al administrador del sistema.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu nueva característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso interno. Todos los derechos reservados.

## 👤 Autor

Desarrollado para la gestión documental organizacional.

---

**Nota**: Los archivos generados se almacenan en la carpeta `salidas/` y no son rastreados por git.
