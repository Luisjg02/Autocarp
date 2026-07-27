"""FileAnalyzer module for multi-format file classification.

Classifies files into intuitive, clean target folders based on extension, MIME type, and format category.
"""

import mimetypes
from pathlib import Path
from typing import Dict


# Mapeo de extensiones a categorías ordenadas en español
EXTENSION_CATEGORY_MAP: Dict[str, str] = {
    # Documentos PDF
    ".pdf": "Documentos_PDF",

    # Documentos de Texto y Procesadores
    ".docx": "Documentos_Texto",
    ".doc": "Documentos_Texto",
    ".txt": "Documentos_Texto",
    ".rtf": "Documentos_Texto",
    ".odt": "Documentos_Texto",
    ".epub": "Documentos_Texto",
    ".pages": "Documentos_Texto",

    # Hojas de Cálculo
    ".xlsx": "Hojas_de_Calculo",
    ".xls": "Hojas_de_Calculo",
    ".csv": "Hojas_de_Calculo",
    ".ods": "Hojas_de_Calculo",

    # Presentaciones
    ".pptx": "Presentaciones",
    ".ppt": "Presentaciones",
    ".odp": "Presentaciones",
    ".key": "Presentaciones",

    # Imágenes y Fotografías
    ".jpg": "Imagenes_y_Fotos",
    ".jpeg": "Imagenes_y_Fotos",
    ".png": "Imagenes_y_Fotos",
    ".gif": "Imagenes_y_Fotos",
    ".webp": "Imagenes_y_Fotos",
    ".svg": "Imagenes_y_Fotos",
    ".bmp": "Imagenes_y_Fotos",
    ".tiff": "Imagenes_y_Fotos",
    ".ico": "Imagenes_y_Fotos",
    ".raw": "Imagenes_y_Fotos",
    ".heic": "Imagenes_y_Fotos",

    # Videos y Películas
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",
    ".webm": "Videos",
    ".m4v": "Videos",

    # Audio y Música
    ".mp3": "Audio_y_Musica",
    ".wav": "Audio_y_Musica",
    ".flac": "Audio_y_Musica",
    ".aac": "Audio_y_Musica",
    ".ogg": "Audio_y_Musica",
    ".m4a": "Audio_y_Musica",

    # Archivos Comprimidos
    ".zip": "Archivos_Comprimidos",
    ".rar": "Archivos_Comprimidos",
    ".7z": "Archivos_Comprimidos",
    ".tar": "Archivos_Comprimidos",
    ".gz": "Archivos_Comprimidos",
    ".bz2": "Archivos_Comprimidos",
    ".iso": "Archivos_Comprimidos",

    # Ejecutables e Instaladores
    ".exe": "Ejecutables_e_Instaladores",
    ".msi": "Ejecutables_e_Instaladores",
    ".apk": "Ejecutables_e_Instaladores",
    ".appimage": "Ejecutables_e_Instaladores",
    ".dmg": "Ejecutables_e_Instaladores",
    ".deb": "Ejecutables_e_Instaladores",

    # Código y Scripts
    ".py": "Codigo_y_Scripts",
    ".js": "Codigo_y_Scripts",
    ".ts": "Codigo_y_Scripts",
    ".html": "Codigo_y_Scripts",
    ".css": "Codigo_y_Scripts",
    ".json": "Codigo_y_Scripts",
    ".xml": "Codigo_y_Scripts",
    ".sql": "Codigo_y_Scripts",
    ".cpp": "Codigo_y_Scripts",
    ".c": "Codigo_y_Scripts",
    ".cs": "Codigo_y_Scripts",
    ".java": "Codigo_y_Scripts",
    ".php": "Codigo_y_Scripts",
    ".sh": "Codigo_y_Scripts",
    ".ps1": "Codigo_y_Scripts",

    # Diseños y Modelos 3D
    ".psd": "Disenos_y_3D",
    ".ai": "Disenos_y_3D",
    ".fig": "Disenos_y_3D",
    ".blend": "Disenos_y_3D",
    ".stl": "Disenos_y_3D",
    ".obj": "Disenos_y_3D",

    # Tipografías
    ".ttf": "Fuentes_Tipograficas",
    ".otf": "Fuentes_Tipograficas",
    ".woff": "Fuentes_Tipograficas",
    ".woff2": "Fuentes_Tipograficas",
}


class FileAnalyzer:
    """Clasificador multiformato de archivos."""

    @staticmethod
    def get_target_folder(filepath: Path) -> str:
        """Determina la carpeta de destino correspondiente para un archivo dado.
        
        Args:
            filepath: Ruta del archivo.
            
        Returns:
            Nombre de la carpeta de destino recomendada.
        """
        ext = filepath.suffix.lower()

        if ext in EXTENSION_CATEGORY_MAP:
            return EXTENSION_CATEGORY_MAP[ext]

        # Fallback a inspección MIME si la extensión no está en el mapa
        mime_type, _ = mimetypes.guess_type(str(filepath))
        if mime_type:
            main_type = mime_type.split("/")[0]
            if main_type == "image":
                return "Imagenes_y_Fotos"
            elif main_type == "video":
                return "Videos"
            elif main_type == "audio":
                return "Audio_y_Musica"
            elif main_type == "text":
                return "Documentos_Texto"

        return "Otros_Archivos"
