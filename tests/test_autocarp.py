"""Pruebas unitarias para Autocarp."""

import pytest
from pathlib import Path
from src.file_analyzer import FileAnalyzer
from src.safety_guard import SafetyGuard
from src.organizer_engine import OrganizerEngine


def test_file_classification():
    assert FileAnalyzer.get_target_folder(Path("documento.pdf")) == "Documentos_PDF"
    assert FileAnalyzer.get_target_folder(Path("contrato.docx")) == "Documentos_Texto"
    assert FileAnalyzer.get_target_folder(Path("foto.jpg")) == "Imagenes_y_Fotos"
    assert FileAnalyzer.get_target_folder(Path("video.mp4")) == "Videos"
    assert FileAnalyzer.get_target_folder(Path("cancion.mp3")) == "Audio_y_Musica"
    assert FileAnalyzer.get_target_folder(Path("balance.xlsx")) == "Hojas_de_Calculo"
    assert FileAnalyzer.get_target_folder(Path("archivo.zip")) == "Archivos_Comprimidos"
    assert FileAnalyzer.get_target_folder(Path("setup.exe")) == "Ejecutables_e_Instaladores"
    assert FileAnalyzer.get_target_folder(Path("script.py")) == "Codigo_y_Scripts"


def test_safety_guard_blocks_system_dirs():
    is_safe, msg = SafetyGuard.is_safe_target_directory("C:\\Windows")
    assert is_safe is False
    assert "crítica" in msg or "seguridad" in msg

    is_safe_root, msg_root = SafetyGuard.is_safe_target_directory("C:\\")
    assert is_safe_root is False


def test_safety_guard_allows_user_dir(tmp_path):
    is_safe, msg = SafetyGuard.is_safe_target_directory(str(tmp_path))
    assert is_safe is True


def test_organizer_engine_execution(tmp_path):
    # Crear archivos de prueba variados en el directorio temporal
    (tmp_path / "factura.pdf").write_text("dummy pdf")
    (tmp_path / "vacaciones.jpg").write_text("dummy image")
    (tmp_path / "datos.csv").write_text("dummy csv")
    (tmp_path / "programa.exe").write_text("dummy exe")

    engine = OrganizerEngine(target_dir=str(tmp_path))
    proposal = engine.scan_and_propose()

    assert "Documentos_PDF" in proposal
    assert "Imagenes_y_Fotos" in proposal
    assert "Hojas_de_Calculo" in proposal
    assert "Ejecutables_e_Instaladores" in proposal

    moved_count, logs = engine.execute_organization(proposal)
    assert moved_count == 4

    # Verificar que los archivos se movieron a sus carpetas correspondientes
    assert (tmp_path / "Documentos_PDF" / "factura.pdf").exists()
    assert (tmp_path / "Imagenes_y_Fotos" / "vacaciones.jpg").exists()
    assert (tmp_path / "Hojas_de_Calculo" / "datos.csv").exists()
    assert (tmp_path / "Ejecutables_e_Instaladores" / "programa.exe").exists()


def test_filename_collision_resolution(tmp_path):
    # Crear carpeta destino y un archivo existente
    pdf_dir = tmp_path / "Documentos_PDF"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    (pdf_dir / "reporte.pdf").write_text("existente")

    # Crear nuevo archivo con el mismo nombre en la raíz
    (tmp_path / "reporte.pdf").write_text("nuevo")

    engine = OrganizerEngine(target_dir=str(tmp_path))
    proposal = engine.scan_and_propose()
    moved_count, logs = engine.execute_organization(proposal)

    assert moved_count == 1
    # El archivo original se mantiene y el nuevo toma un nombre único (ej. reporte(1).pdf)
    assert (pdf_dir / "reporte.pdf").exists()
    assert (pdf_dir / "reporte(1).pdf").exists()
