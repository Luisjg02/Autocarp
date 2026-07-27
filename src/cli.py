"""Interactive Rich CLI interface for Autocarp.
"""

import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from src.safety_guard import SafetyGuard
from src.organizer_engine import OrganizerEngine


class AutocarpCLI:
    """Interfaz gráfica de terminal interactiva para Autocarp."""

    def __init__(self):
        self.console = Console()

    def run(self, target_dir: str = None) -> None:
        """Inicia el proceso de organización de Autocarp."""
        self.console.clear()
        self._print_header()

        if not target_dir:
            self.console.print("[yellow]Ingresa la ruta de la carpeta que deseas organizar (ej. C:\\Users\\tu_usuario\\Downloads):[/yellow]")
            target_dir = Prompt.ask("[bold green]Ruta de la carpeta[/bold green]", default=str(Path.home() / "Downloads"))

        target_dir = target_dir.strip('"\'')
        path_obj = Path(target_dir).resolve()

        # 1. Validación de Seguridad (SafetyGuard)
        is_safe, msg = SafetyGuard.is_safe_target_directory(str(path_obj))
        if not is_safe:
            self.console.print(Panel(
                f"[bold red]❌ {msg}[/bold red]",
                title="[bold red]Error de Seguridad Autocarp[/bold red]",
                border_style="red"
            ))
            return

        engine = OrganizerEngine(target_dir=str(path_obj))

        # 2. Escaneo y Propuesta
        self.console.print(f"\n🔍 [bold cyan]Escaneando y clasificando todos los archivos en:[/bold cyan] [bold yellow]{path_obj}[/bold yellow]...\n")
        proposal = engine.scan_and_propose()

        if not proposal:
            self.console.print(Panel(
                "[bold green]✓ La carpeta está limpia. No hay archivos sueltos para reorganizar.[/bold green]",
                border_style="green"
            ))
            return

        # 3. Vista previa del árbol con Rich Tree
        engine.tree_previewer.render(path_obj.name, proposal)

        # 4. Confirmación interactiva previa al movimiento
        try:
            confirmed = Confirm.ask(
                f"¿Deseas proceder y organizar estos archivos en sus carpetas correspondientes dentro de [bold cyan]{path_obj.name}[/bold cyan]?",
                default=True
            )
        except (EOFError, KeyboardInterrupt):
            confirmed = True

        if not confirmed:
            self.console.print("[bold red]❌ Operación cancelada por el usuario. Ningún archivo fue movido.[/bold red]")
            return

        # 5. Ejecución del traslado
        self.console.print("\n🚀 [bold green]Creando carpetas y organizando archivos...[/bold green]\n")
        moved_count, logs = engine.execute_organization(proposal)

        # 6. Resumen de resultados
        self.console.print(Panel(
            f"[bold green]✓ ¡Organización completada con éxito![/bold green]\n\n"
            f"• [bold]Archivos procesados y organizados:[/bold] {moved_count}\n"
            f"• [bold]Ubicación:[/bold] {path_obj}",
            title="[bold green]Autocarp — Resumen Final[/bold green]",
            border_style="green"
        ))

    def _print_header(self):
        self.console.print(Panel(
            "[bold cyan]📁 Autocarp v1.0[/bold cyan] — Organizador Inteligente Multiformato de Archivos\n"
            "[dim]Clasifica automáticamente documentos, imágenes, videos, audios, comprimidos, instaladores y más.[/dim]",
            border_style="cyan"
        ))
