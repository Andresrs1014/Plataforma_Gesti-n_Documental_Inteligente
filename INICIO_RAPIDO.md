# 🚀 Inicio Rápido - PGDI

## Opciones para iniciar la aplicación

### Opción 1: Script de inicio automático (Recomendado) ⭐

#### Windows:
```bash
start.bat
```

#### Windows/Linux/Mac (Python):
```bash
python start.py
```

Estos scripts automáticamente:
- ✅ Verifican el entorno virtual
- ✅ Instalan dependencias faltantes
- ✅ Crean carpetas necesarias
- ✅ Inician el servidor

---

### Opción 2: Inicio manual

#### 1. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

#### 2. Instalar dependencias (primera vez)
```bash
pip install -r requirements.txt
```

#### 3. Iniciar servidor
```bash
uvicorn api:app --reload
```

---

## 📌 URLs importantes

Una vez iniciado el servidor:

- **Interfaz principal**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Procedimientos**: http://localhost:8000/frontend/prodecimiento.html
- **Instructivos**: http://localhost:8000/frontend/instructivo.html

---

## ⚙️ Configuración inicial (primera vez)

### 1. Crear entorno virtual
```bash
python -m venv .venv
```

### 2. Activar entorno
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Agregar plantillas
Coloca los archivos Excel en la carpeta `plantillas/`:
- `FORMATO_PROCEDIMIENTO.xlsx`
- `FORMATO_INSTRUCTIVO.xlsx`

### 5. ¡Listo! Usa el script de inicio
```bash
# Windows
start.bat

# O multiplataforma
python start.py
```

---

## 🛑 Detener el servidor

Presiona `Ctrl + C` en la terminal donde se está ejecutando el servidor.

---

## ❓ Solución de problemas

### El servidor no inicia
- Verifica que el puerto 8000 no esté en uso
- Asegúrate de tener Python 3.8 o superior
- Revisa que todas las dependencias estén instaladas

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### No genera documentos
- Verifica que existan las plantillas en `plantillas/`
- Revisa los logs en la consola del servidor

---

## 📞 Soporte

Para más información, consulta el [README.md](README.md) principal.
