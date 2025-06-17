"""Tests for the bundler module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from codebrief.tools import bundler


def test_generate_tree_content():
    """Test generate_tree_content function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.tree_generator") as mock_tree_gen:
            mock_tree_gen.generate_and_output_tree.return_value = (
                "CodeBrief/\n├── file1.py\n└── file2.py"
            )

            result = bundler.generate_tree_content(
                project_root=temp_dir, config_global_excludes=[]
            )

            assert "CodeBrief/" in result
            assert "file1.py" in result


def test_generate_tree_content_error():
    """Test generate_tree_content handles errors gracefully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.tree_generator") as mock_tree_gen:
            mock_tree_gen.generate_and_output_tree.side_effect = Exception("Tree error")

            result = bundler.generate_tree_content(
                project_root=temp_dir, config_global_excludes=[]
            )

            assert "Error generating directory tree" in result


def test_generate_git_content():
    """Test generate_git_content function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.git_provider") as mock_git:
            mock_git.get_git_context.return_value = "# Git Context\n\nMock git info"

            result = bundler.generate_git_content(project_root=temp_dir)

            assert "Mock git info" in result
            mock_git.get_git_context.assert_called_once()


def test_generate_git_content_error():
    """Test generate_git_content handles errors gracefully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.git_provider") as mock_git:
            mock_git.get_git_context.side_effect = Exception("Git error")

            result = bundler.generate_git_content(project_root=temp_dir)

            assert "Error generating Git context" in result


def test_generate_deps_content():
    """Test generate_deps_content function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.dependency_lister") as mock_deps:
            mock_deps.list_dependencies.return_value = "# Dependencies\n\nnumpy==1.0"

            result = bundler.generate_deps_content(project_root=temp_dir)

            assert "numpy==1.0" in result
            mock_deps.list_dependencies.assert_called_once()


def test_generate_deps_content_error():
    """Test generate_deps_content handles errors gracefully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("codebrief.tools.bundler.dependency_lister") as mock_deps:
            mock_deps.list_dependencies.side_effect = Exception("Deps error")

            result = bundler.generate_deps_content(project_root=temp_dir)

            assert "Error generating dependency list" in result


@patch("codebrief.tools.bundler.generate_tree_content")
@patch("codebrief.tools.bundler.generate_git_content")
@patch("codebrief.tools.bundler.generate_deps_content")
@patch("codebrief.tools.bundler.generate_flatten_content")
@patch("codebrief.tools.bundler.config_manager")
def test_create_bundle_comprehensive(
    mock_config, mock_flatten, mock_deps, mock_git, mock_tree
):
    """Test create_bundle with all sections enabled."""
    mock_config.load_config.return_value = {"global_exclude_patterns": []}
    mock_tree.return_value = "Tree content"
    mock_git.return_value = "Git content"
    mock_deps.return_value = "Deps content"
    mock_flatten.return_value = "Flatten content"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with patch("codebrief.tools.bundler.console"):
            result = bundler.create_bundle(
                project_root=temp_path,
                include_tree=True,
                include_git=True,
                include_deps=True,
                flatten_paths=[temp_path],
            )

            assert result is not None
            assert "# CodeBrief Bundle" in result
