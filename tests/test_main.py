# tests/test_main.py
"""
Tests for the main CLI application in src.contextcraft.main.
Uses Typer's CliRunner for invoking commands.
"""
from pathlib import Path
from typing import Any, Dict
from unittest import mock  # For mocking underlying tool functions

import typer
from typer.testing import CliRunner

from src.contextcraft import __version__

# Import the Typer app instance from your main module
from src.contextcraft.main import app
from src.contextcraft.utils import config_manager

# Create a CliRunner instance to invoke commands
runner = CliRunner(mix_stderr=False)

# --- Test for the 'hello' command ---


def test_hello_command_default_name():
    """Test the hello command with the default name."""
    result = runner.invoke(app, ["hello"], env={"NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "Hello World from ContextCraft!" in result.stdout


def test_hello_command_with_custom_name():
    """Test the hello command with a custom name provided via --name."""
    result = runner.invoke(app, ["hello", "--name", "Developer"])
    assert result.exit_code == 0
    assert "Hello Developer from ContextCraft!" in result.stdout


def test_hello_command_help():
    """Test the --help option for the hello command."""
    result = runner.invoke(app, ["hello", "--help"])
    assert result.exit_code == 0
    assert "Usage: contextcraft hello [OPTIONS]" in result.stdout
    assert "Greets a person." in result.stdout  # Check for part of the docstring


# --- Tests for the 'tree' command ---


def test_tree_command_help():
    """Test the --help option for the tree command."""
    result = runner.invoke(app, ["tree", "--help"])
    assert result.exit_code == 0
    assert "Usage: contextcraft tree [OPTIONS] [ROOT_DIR]" in result.stdout
    assert "Generates and displays or saves a directory tree structure." in result.stdout


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_success(mock_generate_tree, tmp_path: Path):
    """Test tree command successful execution (mocking the actual tree generation)."""
    # tmp_path is a pytest fixture providing a temporary directory Path object
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 0
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(),  # Typer resolves path by default
        output_file_path=None,
        ignore_list=[],
        config_global_excludes=[],
    )


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_output_file(mock_generate_tree, tmp_path: Path):
    """Test tree command with an output file specified."""
    output_file = tmp_path / "tree_output.txt"
    result = runner.invoke(app, ["tree", str(tmp_path), "--output", str(output_file)])
    assert result.exit_code == 0
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(), output_file_path=output_file.resolve(), ignore_list=[], config_global_excludes=[]
    )


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_ignore_flags(mock_generate_tree, tmp_path: Path):
    """Test tree command with ignore flags."""
    result = runner.invoke(app, ["tree", str(tmp_path), "--ignore", "venv", "--ignore", "*.pyc"])
    assert result.exit_code == 0
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(), output_file_path=None, ignore_list=["venv", "*.pyc"], config_global_excludes=[]
    )


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree", side_effect=Exception("Tree generation failed!"))
def test_tree_command_handles_exception(mock_generate_tree_error, tmp_path: Path):
    """Test that tree command handles exceptions from the underlying tool and exits non-zero."""
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 1  # As defined in main.py's except block
    assert "An unexpected error occurred during tree generation: Tree generation failed!" in result.stdout
    mock_generate_tree_error.assert_called_once()


def test_tree_command_invalid_root_dir():
    """Test tree command with a non-existent root directory."""
    # Typer should handle `exists=True` and exit before our code is called.
    # The exit code from Typer for validation errors is typically 2.
    result = runner.invoke(app, ["tree", "non_existent_directory_for_testing"])
    assert result.exit_code != 0  # Typer's validation error, often 2
    assert "Invalid value for 'ROOT_DIR'" in result.stderr or "does not exist" in result.stderr  # Typer's error message


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree", side_effect=typer.Exit(code=5))
def test_tree_command_propagates_typer_exit(mock_generate_tree_typer_exit, tmp_path: Path):
    """Test that tree command propagates typer.Exit from the underlying tool."""
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 5  # Should be the code from the raised typer.Exit
    mock_generate_tree_typer_exit.assert_called_once()
    # Assert that no "An unexpected error occurred" message is printed for typer.Exit
    assert "An unexpected error occurred" not in result.stdout
    assert "An unexpected error occurred" not in result.stderr


# --- Tests for the 'flatten' command ---


def test_flatten_command_help():
    """Test the --help option for the flatten command."""
    result = runner.invoke(app, ["flatten", "--help"])
    assert result.exit_code == 0
    assert "Usage: contextcraft flatten [OPTIONS] [ROOT_DIR]" in result.stdout
    assert "Flattens specified files from a directory" in result.stdout


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_success(mock_flatten_logic, tmp_path: Path):
    """Test flatten command successful execution (mocking actual flattening)."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once_with(root_dir_path=tmp_path.resolve(), output_file_path=None, include_patterns=[], exclude_patterns=[])


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_with_options(mock_flatten_logic, tmp_path: Path):
    """Test flatten command with include, exclude, and output options."""
    output_f = tmp_path / "flat.txt"
    result = runner.invoke(
        app, ["flatten", str(tmp_path), "--output", str(output_f), "--include", "*.py", "--include", "*.md", "--exclude", "temp/*"]
    )
    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once_with(
        root_dir_path=tmp_path.resolve(), output_file_path=output_f.resolve(), include_patterns=["*.py", "*.md"], exclude_patterns=["temp/*"]
    )


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic", side_effect=Exception("Flattening failed!"))
def test_flatten_command_handles_exception(mock_flatten_error, tmp_path: Path):
    """Test that flatten command handles exceptions and exits non-zero."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 1
    assert "An unexpected error occurred during code flattening: Flattening failed!" in result.stdout
    mock_flatten_error.assert_called_once()


# --- Test for main app help ---
def test_app_help():
    """Test the main application's --help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: contextcraft [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "hello" in result.stdout
    assert "tree" in result.stdout
    assert "flatten" in result.stdout


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic", side_effect=typer.Exit(code=6))
def test_flatten_command_propagates_typer_exit(mock_flatten_logic_typer_exit, tmp_path: Path):
    """Test that flatten command propagates typer.Exit from the underlying tool."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 6  # Should be the code from the raised typer.Exit
    mock_flatten_logic_typer_exit.assert_called_once()
    assert "An unexpected error occurred" not in result.stdout
    assert "An unexpected error occurred" not in result.stderr


# --- Test for the version command ---
def test_app_version():
    """Test the --version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"ContextCraft Version: {__version__}" in result.stdout  # Check for the full string


def test_app_version_short_flag():
    """Test the -v (short) flag for version."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert f"ContextCraft Version: {__version__}" in result.stdout


# ---  Tests for config default output filenames ---


def create_pyproject_with_config(tmp_path: Path, contextcraft_config: Dict[str, Any]) -> Path:
    """Helper to create a pyproject.toml in tmp_path with a [tool.contextcraft] section."""
    pyproject_file = tmp_path / "pyproject.toml"

    # Use the 'toml' package for writing, as it's a definite dependency now.
    import toml as toml_writer

    full_config = {"tool": {config_manager.CONFIG_SECTION_NAME: contextcraft_config}}
    pyproject_file.write_text(toml_writer.dumps(full_config), encoding="utf-8")
    return pyproject_file


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_uses_config_default_output(mock_generate_tree, tmp_path: Path):
    """Test `tree` uses default_output_filename_tree from config when --output not given."""
    config_output_filename = "configured_tree.txt"
    create_pyproject_with_config(tmp_path, {"default_output_filename_tree": config_output_filename})

    # Run the command with tmp_path as the root_dir (where pyproject.toml is)
    result = runner.invoke(app, ["tree", str(tmp_path)])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    # Check the output_file_path argument passed to the mocked function
    args, kwargs = mock_generate_tree.call_args
    expected_output_path = (tmp_path / config_output_filename).resolve()
    assert kwargs.get("output_file_path") == expected_output_path
    assert "Using default output file from config" in result.stdout


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_cli_output_overrides_config(mock_generate_tree, tmp_path: Path):
    """Test `tree` --output CLI flag overrides configured default."""
    config_output_filename = "configured_tree.txt"
    cli_output_filename = "cli_specified_tree.txt"
    create_pyproject_with_config(tmp_path, {"default_output_filename_tree": config_output_filename})

    cli_output_path = tmp_path / cli_output_filename

    result = runner.invoke(app, ["tree", str(tmp_path), "--output", str(cli_output_path)])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    assert kwargs.get("output_file_path") == cli_output_path.resolve()
    assert "Using default output file from config" not in result.stdout  # Should not print this if CLI overrides


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_uses_config_default_output(mock_flatten_logic, tmp_path: Path):
    """Test `flatten` uses default_output_filename_flatten from config."""
    config_output_filename = "configured_flat.md"
    create_pyproject_with_config(tmp_path, {"default_output_filename_flatten": config_output_filename})

    result = runner.invoke(app, ["flatten", str(tmp_path)])

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    expected_output_path = (tmp_path / config_output_filename).resolve()
    assert kwargs.get("output_file_path") == expected_output_path
    assert "Using default output file from config" in result.stdout


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_cli_output_overrides_config(mock_flatten_logic, tmp_path: Path):
    """Test `flatten` --output CLI flag overrides configured default."""
    config_output_filename = "configured_flat.md"
    cli_output_filename = "cli_flat.md"
    create_pyproject_with_config(tmp_path, {"default_output_filename_flatten": config_output_filename})

    cli_output_path = tmp_path / cli_output_filename

    result = runner.invoke(app, ["flatten", str(tmp_path), "--output", str(cli_output_path)])

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    assert kwargs.get("output_file_path") == cli_output_path.resolve()
    assert "Using default output file from config" not in result.stdout


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_no_output_options_prints_to_console(mock_generate_tree, tmp_path: Path):
    """Test `tree` prints to console if no CLI/config output is set (mocking actual generation)."""
    # Use a clean tmp_path without a pyproject.toml defining default output
    # Mock the tree generation to avoid actual tree printing, just check it was called correctly

    # Create a dummy file so the directory isn't empty, for a more realistic tree call
    (tmp_path / "dummy.txt").touch()
    result = runner.invoke(app, ["tree", str(tmp_path)])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    assert kwargs.get("output_file_path") is None  # Crucial: should be None for console output
    # We can't easily assert console output here because it's the mocked function's job.
    # We trust generate_and_output_tree to print to console if output_file_path is None.
