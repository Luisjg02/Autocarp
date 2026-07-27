"""Punto de entrada principal para Autocarp v1.0.

Uso:
    python main.py [ruta_de_carpeta]
"""

import sys
import os
from pathlib import Path

# Configurar codificación UTF-8 en salida de consola Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Asegurar que el directorio raíz del proyecto está en PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from src.cli import AutocarpCLI


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    cli = AutocarpCLI()
    cli.run(target_dir=target_dir)


if __name__ == "__main__":
    main()
