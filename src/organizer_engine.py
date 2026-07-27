"""OrganizerEngine module for scanning, analyzing, and moving files.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

from src.file_analyzer import FileAnalyzer
from src.safety_guard import SafetyGuard
from src.tree_previewer import TreePreviewer


class OrganizerEngine:
    """Motor principal de escaneo y traslado seguro de archivos para Autocarp."""

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir).resolve()
        self.analyzer = FileAnalyzer()
        self.safety = SafetyGuard()
        self.tree_previewer = TreePreviewer()

    def scan_and_propose(self) -> Dict[str, List[str]]:
        """Escanea la carpeta objetivo y genera la propuesta de mapa de carpetas y archivos.
        
        Returns:
            Dict[nombre_carpeta_destino, List[nombre_archivo]]
        """
        proposal: Dict[str, List[str]] = {}

        if not self.target_dir.exists():
            return proposal

        for item in self.target_dir.iterdir():
            # Únicamente procesar archivos sueltos en el nivel raíz de la carpeta especificada
            if item.is_file() and self.safety.is_safe_file_to_move(item):
                category_folder = self.analyzer.get_target_folder(item)
                if category_folder not in proposal:
                    proposal[category_folder] = []
                proposal[category_folder].append(item.name)

        return proposal

    def execute_organization(self, proposal: Dict[str, List[str]]) -> Tuple[int, List[str]]:
        """Ejecuta el traslado de archivos creando las carpetas destino y resolviendo colisiones de nombres.
        
        Returns:
            Tuple (archivos_movidos_count, lista_de_registros)
        """
        moved_count = 0
        logs: List[str] = []

        for folder_name, filenames in proposal.items():
            dest_dir = self.target_dir / folder_name
            dest_dir.mkdir(parents=True, exist_ok=True)

            for fname in filenames:
                src_path = self.target_dir / fname

                if not src_path.exists():
                    continue

                dest_path = dest_dir / fname

                # Resolución segura de colisiones si el archivo destino ya existe
                if dest_path.exists():
                    dest_path = self._generate_unique_destination(dest_dir, fname)

                try:
                    shutil.move(str(src_path), str(dest_path))
                    moved_count += 1
                    logs.append(f"✓ Movido: '{fname}' -> '{folder_name}/{dest_path.name}'")
                except Exception as err:
                    logs.append(f"❌ Error al mover '{fname}': {err}")

        return moved_count, logs

    def _generate_unique_destination(self, dest_dir: Path, filename: str) -> Path:
        """Genera un nombre de archivo único para evitar sobrescribir duplicados (ej. archivo(1).pdf)."""
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        counter = 1

        while True:
            candidate = dest_dir / f"{stem}({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1
