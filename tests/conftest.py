"""Pytest configuration and fixtures for CodeBrief tests."""

import pytest


@pytest.fixture
def sample_project_structure(tmp_path):
    """Create a sample project structure for testing."""
    # Create directories
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Create some sample files
    (src_dir / "main.py").write_text("# Main application file\nprint('Hello World')")
    (src_dir / "utils.py").write_text("# Utility functions\ndef helper():\n    pass")
    (tests_dir / "test_main.py").write_text(
        "# Test file\ndef test_main():\n    assert True"
    )
    (tmp_path / "README.md").write_text("# Sample Project\n\nThis is a sample project.")
    (tmp_path / "pyproject.toml").write_text(
        "[tool.poetry]\nname = 'sample'\nversion = '0.1.0'"
    )

    return tmp_path
