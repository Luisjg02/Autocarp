"""SafetyGuard module for protecting critical operating system directories and files.
"""

import os
from pathlib import Path
from typing import Tuple, List

# Carpetas del sistema prohibidas de organizar directamente
CRITICAL_SYSTEM_DIRS = {
    r"c:\windows",
    r"c:\windows\system32",
    r"c:\program files",
    r"c:\program files (x86)",
    r"c:\programdata",
    r"c:\recovery",
    r"c:\$recycle.bin",
    r"c:\boot",
}

# Archivos del sistema protegidos de movimiento
PROTECTED_SYSTEM_FILES = {
    "desktop.ini",
    "thumbs.db",
    "ntuser.dat",
    "ntuser.ini",
    "pagefile.sys",
    "hiberfil.sys",
    "swapfile.sys",
    "autorun.inf",
    ".ds_store",
}


class SafetyGuard:
    """Validador de seguridad para evitar modificaciones en archivos o carpetas críticas del sistema."""

    @staticmethod
    def is_safe_target_directory(target_path: str) -> Tuple[bool, str]:
        """Verifica si el directorio especificado es seguro para organizar."""
        path_obj = Path(target_path).resolve()

        if not path_obj.exists():
            return False, f"La carpeta especificada no existe: {target_path}"

        if not path_obj.is_dir():
            return False, f"La ruta especificada no es una carpeta: {target_path}"

        # Evitar organizar la raíz de cualquier unidad (ej. C:\, D:\) directamente
        if path_obj.parent == path_obj or len(path_obj.parts) <= 1:
            return False, "Por seguridad, no se permite reorganizar la raíz de una unidad directamente (ej. C:\\)."

        # Verificar si está en carpetas críticas del sistema
        str_path_lower = str(path_obj).lower()
        for sys_dir in CRITICAL_SYSTEM_DIRS:
            if str_path_lower == sys_dir or str_path_lower.startswith(sys_dir + os.sep):
                return False, f"Acceso denegado: '{target_path}' es una carpeta crítica del sistema operativo."

        return True, "Directorio seguro."

    @staticmethod
    def is_safe_file_to_move(filepath: Path) -> bool:
        """Verifica si un archivo individual es seguro de mover."""
        filename_lower = filepath.name.lower()

        # Omitir archivos del sistema protegidos
        if filename_lower in PROTECTED_SYSTEM_FILES:
            return False

        # Omitir archivos ocultos del sistema
        if filename_lower.startswith("."):
            return False

        return True
