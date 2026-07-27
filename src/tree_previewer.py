"""TreePreviewer module for displaying visual proposal of folder reorganization.
"""

from typing import Dict, List
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel


class TreePreviewer:
    """Renderizador gráfico de vista previa del árbol de organización con Rich."""

    def __init__(self, console: Console = None):
        self.console = console or Console()

    def render(self, target_dir_name: str, proposal_map: Dict[str, List[str]]) -> None:
        """Imprime el árbol gráfico de carpetas a crear y archivos a mover.
        
        Args:
            target_dir_name: Nombre de la carpeta siendo organizada.
            proposal_map: Diccionario {nombre_carpeta_destino: [lista_de_archivos]}.
        """
        if not proposal_map:
            self.console.print(Panel(
                "[bold yellow]No se encontraron archivos sueltos para reorganizar en esta carpeta.[/bold yellow]",
                border_style="yellow"
            ))
            return

        total_files = sum(len(files) for files in proposal_map.values())
        total_folders = len(proposal_map)

        tree = Tree(f"📁 [bold cyan]Propuesta de Organización Autocarp para:[/bold cyan] [bold yellow]{target_dir_name}[/bold yellow]")

        for folder_name, files in proposal_map.items():
            folder_node = tree.add(
                f"📂 [bold green]{folder_name}/[/bold green] [dim]({len(files)} archivos)[/dim]"
            )
            for filename in files[:15]:  # Mostrar hasta 15 por carpeta para no saturar
                folder_node.add(f"📄 [white]{filename}[/white]")

            if len(files) > 15:
                folder_node.add(f"[dim]... y {len(files) - 15} archivos más[/dim]")

        self.console.print(Panel(
            tree,
            title="[bold green]Autocarp v1.0 — Vista Previa de Reorganización[/bold green]",
            subtitle=f"[bold]Resumen:[/bold] {total_files} archivos en {total_folders} carpetas automáticas",
            border_style="blue"
        ))
