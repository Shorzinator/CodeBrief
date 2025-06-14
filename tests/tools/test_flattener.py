# tests/tools/test_flattener.py
"""Tests for the src.contextcraft.tools.flattener module.
Focuses on the flatten_code_logic function and its interactions.
"""
from pathlib import Path
from typing import Optional

import pytest

from src.contextcraft.tools import flattener
from src.contextcraft.utils import ignore_handler


@pytest.fixture()
def create_project_structure(tmp_path: Path):
    def _create_files(structure: dict[str, Optional[str]]):
        for rel_path_str, content in structure.items():
            full_path = tmp_path / rel_path_str
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if content is not None:
                full_path.write_text(content, encoding="utf-8")
            else:
                full_path.mkdir(exist_ok=True)
        return tmp_path

    return _create_files


# Test for the include criteria helper function
@pytest.mark.parametrize(
    ("file_name", "cli_include_patterns", "expected"),
    [
        ("foo.py", ["*.py"], True),
        ("foo.txt", ["*.py"], False),
        ("foo.txt", ["*.txt"], True),
        ("foo.txt", ["foo.txt"], True),
        ("foo.txt", ["bar.txt"], False),
        ("foo.txt", ["foo*"], True),
        ("data.json", ["*.json", "*.yaml"], True),
        ("config.ini", ["*.json", "*.yaml"], False),
        ("Makefile", ["Makefile"], True),
        ("script.sh", [".sh"], True),
        ("foo.py", None, True),  # Uses DEFAULT_INCLUDE_PATTERNS
        ("foo.py", [], True),  # Uses DEFAULT_INCLUDE_PATTERNS
        ("image.jpg", None, False),  # .jpg not in DEFAULT_INCLUDE_PATTERNS
        ("README", None, True),  # README in DEFAULT_INCLUDE_PATTERNS
        ("README.md", None, True),  # .md in DEFAULT_INCLUDE_PATTERNS
    ],
)
def test_file_matches_include_criteria(file_name, cli_include_patterns, expected):
    file_path = Path(file_name)
    # The flattener.DEFAULT_INCLUDE_PATTERNS will be used internally by the function if cli_include_patterns is None/empty
    result = flattener._file_matches_include_criteria(file_path, cli_include_patterns)
    assert result is expected


# Tests for flatten_code_logic
def test_flatten_basic(create_project_structure):
    project_root = create_project_structure(
        {
            "file1.py": "print('File 1')",
            "src/file2.js": "// File 2",
            "nodocs.txt": "No docs here",
        }
    )
    output_file = project_root / "output_flat.txt"
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.py", "*.js"],
    )
    content = output_file.read_text()
    assert "# --- File: file1.py ---" in content
    assert "print('File 1')" in content
    assert f"# --- File: {Path('src/file2.js').as_posix()} ---" in content
    assert "// File 2" in content
    assert "nodocs.txt" not in content


def test_flatten_with_llmignore(create_project_structure):
    project_root = create_project_structure(
        {
            ignore_handler.LLMIGNORE_FILENAME: "*.log\nignored_dir/\n!ignored_dir/keep_this.py",
            "app.py": "print('app')",
            "data.log": "this is a log",
            "ignored_dir/secret.txt": "secret stuff",
            "ignored_dir/another.py": "print('ignored_dir py')",
            "ignored_dir/keep_this.py": "print('keep me')",
        }
    )
    output_file = project_root / "output_flat.txt"
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.py"],  # Only include .py files
    )
    content = output_file.read_text()
    assert "# --- File: app.py ---" in content
    assert f"# --- File: {Path('ignored_dir/keep_this.py').as_posix()} ---" in content
    assert "print('keep me')" in content
    assert "data.log" not in content
    assert "secret.txt" not in content
    assert f"# --- File: {Path('ignored_dir/another.py').as_posix()} ---" not in content


# tests/tools/test_flattener.py
def test_flatten_binary_file_skip(create_project_structure, capsys):
    project_root = create_project_structure({"text_file.txt": "hello"})
    binary_file_path = project_root / "binary_file.bin"
    binary_file_path.write_bytes(b"\x00\x01\xFF\xFE")

    output_file = project_root / "output_flat.txt"
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.txt", "*.bin"],
    )

    content = output_file.read_text()
    captured = capsys.readouterr()

    assert "# --- File: text_file.txt ---" in content
    assert (
        f"# --- Skipped binary or non-UTF-8 file: {Path('binary_file.bin').as_posix()} ---"
        in content
    )
    assert "Warning: Skipping binary or non-UTF-8 file" in captured.out


def test_flatten_with_cli_exclude(create_project_structure):
    project_root = create_project_structure(
        {
            "main.py": "main content",
            "utils.py": "utils content",
            "tests/test_main.py": "test content",
        }
    )
    output_file = project_root / "output_flat.txt"
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.py"],
        exclude_patterns=["tests/*"],  # CLI exclude
    )
    content = output_file.read_text()
    assert "# --- File: main.py ---" in content
    assert "# --- File: utils.py ---" in content
    assert f"# --- File: {Path('tests/test_main.py').as_posix()} ---" not in content


def test_flatten_interaction_llmignore_and_cli_exclude(create_project_structure):
    project_root = create_project_structure(
        {
            ignore_handler.LLMIGNORE_FILENAME: "*.log\ntemp_data/",
            "src/app.py": "app code",
            "src/app.log": "app log",
            "temp_data/file.txt": "temp data",
            "config.ini": "config data",
        }
    )
    output_file = project_root / "output_flat.txt"
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.py", "*.ini"],  # Include .py and .ini
        exclude_patterns=["config.ini"],  # CLI exclude for config.ini
    )
    content = output_file.read_text()
    assert "# --- File: src/app.py ---" in content
    assert "config.ini" not in content  # Excluded by CLI
    assert "app.log" not in content  # Excluded by .llmignore
    assert "temp_data/file.txt" not in content  # Excluded by .llmignore


def test_flatten_default_general_exclusions_when_no_llmignore(
    create_project_structure, monkeypatch
):
    """Test that DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK is used when no .llmignore."""
    # Ensure DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK has some testable items
    monkeypatch.setattr(
        flattener,
        "DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK",
        {"__pycache__", "*.log"},
    )

    project_root = create_project_structure(
        {
            "main.py": "main",
            "__pycache__/test.pyc": "pyc",  # Should be skipped by fallback
            "app.log": "log content",  # Should be skipped by fallback pattern
        }
    )
    output_file = project_root / "output_flat.txt"
    # No .llmignore file is created for this test
    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.py", "*.log", "*.pyc"],  # Try to include them
    )
    content = output_file.read_text()
    assert "# --- File: main.py ---" in content
    assert "__pycache__" not in content
    assert "app.log" not in content  # `Path(file_name).match(pattern)` will catch *.log


def test_flatten_output_file_exclusion(create_project_structure):
    """Test that the output file itself is excluded if it's within the root_dir."""
    project_root = create_project_structure({"file1.txt": "content1"})
    output_file = project_root / "output_flat.txt"  # Output file inside root_dir

    flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=output_file,
        include_patterns=["*.txt"],
    )
    content = output_file.read_text()
    assert "# --- File: file1.txt ---" in content
    assert "output_flat.txt" not in content  # Ensure it didn't try to read itself


def test_flatten_to_console_output(create_project_structure, capsys):
    """Test flattening content to console when output_file_path is None."""
    project_root = create_project_structure(
        {"file_a.txt": "Content of A", "file_b.txt": "Content of B"}
    )
    result = flattener.flatten_code_logic(
        root_dir=project_root,
        output_file_path=None,  # Output to console
        include_patterns=["file_a.txt", "file_b.txt"],
    )
    captured = capsys.readouterr()
    # Function should return string when no output file specified
    assert result is not None
    assert "# --- File: file_a.txt ---" in result
    assert "Content of A" in result
    assert "# --- File: file_b.txt ---" in result
    assert "Content of B" in result
    # Summary message should be in console output
    assert "--- Flattened 2 file(s)." in captured.out
