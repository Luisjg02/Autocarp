# 📂 Autocarp

**Autocarp** es un organizador inteligente y seguro de archivos para cualquier carpeta o disco de tu computadora. Analiza todo tipo de archivos (documentos, imágenes, videos, audios, archivos comprimidos, ejecutable, hojas de cálculo, código, etc.), genera una vista previa del árbol de directorios sugeridos y clasifica los archivos en carpetas automáticas y ordenadas.

---

## 🌟 Características Principales
1. **Soporte Multiformato Completo:** No se limita a código. Analiza imágenes (`.png`, `.jpg`, `.svg`, `.raw`), documentos (`.pdf`, `.docx`, `.txt`), multimedia (`.mp4`, `.mp3`, `.mkv`), archivos comprimidos (`.zip`, `.rar`, `.7z`), ejecutable e instaladores (`.exe`, `.msi`), hojas de cálculo (`.xlsx`, `.csv`), presentaciones (`.pptx`) y más.
2. **Protección de Sistema (Safety Guard):** Protege carpetas del sistema operativo (`C:\Windows`, `C:\Program Files`), archivos del sistema (`desktop.ini`, `NTUSER.DAT`) y archivos ocultos de configuración.
3. **Vista Previa de Árbol (Tree Preview):** Muestra una vista previa visual con `Rich Tree` antes de mover cualquier archivo.
4. **Resolución de Colisiones de Nombres:** Si existen archivos con el mismo nombre en la carpeta destino, les asigna nombres únicos automáticamente (ej. `documento(1).pdf`) para evitar sobrescribir datos.
5. **Registro de Movimientos:** Mantiene un registro detallado de los movimientos realizados.

---

## 🚀 Uso e Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar Autocarp especificando la carpeta a organizar (ej. Downloads)
python main.py "C:\Users\5060\Downloads"

# O ejecutar interactivamente
python main.py
```

---

## 🧪 Pruebas Unitarias

```bash
pytest
```
