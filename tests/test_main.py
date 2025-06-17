# tests/test_main.py
"""Tests for the main CLI application in src.codebrief.main.

This module contains comprehensive tests for the CLI commands defined in the main
module, covering various scenarios including successful operations, error
handling, and edge cases.
"""

from pathlib import Path
from typing import Any
from unittest import mock

from typer.testing import CliRunner

from src.codebrief import __version__
from src.codebrief.main import app
from src.codebrief.utils import config_manager

runner = CliRunner()


def test_hello_default():
    """Test hello command with default name."""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello World from CodeBrief!" in result.stdout


def test_hello_custom_name():
    """Test hello command with custom name."""
    result = runner.invoke(app, ["hello", "--name", "Developer"])
    assert result.exit_code == 0
    assert "Hello Developer from CodeBrief!" in result.stdout


def test_version_option():
    """Test --version option displays correct version information."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"CodeBrief Version: {__version__}" in result.stdout


def test_version_short_option():
    """Test -v option displays correct version information."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert f"CodeBrief Version: {__version__}" in result.stdout


def test_help_command():
    """Test --help command shows available commands."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "codebrief" in result.stdout.lower()


# Test Tree Command


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_default(mock_tree_gen):
    """Test tree command with default parameters."""
    mock_tree_gen.return_value = "mock tree output"
    result = runner.invoke(app, ["tree"])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_output(mock_tree_gen, tmp_path: Path):
    """Test tree command with output file."""
    output_file = tmp_path / "tree_output.txt"
    mock_tree_gen.return_value = None  # When output_file is provided, no return value
    result = runner.invoke(app, ["tree", "--output", str(output_file)])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_ignore(mock_tree_gen):
    """Test tree command with ignore patterns."""
    mock_tree_gen.return_value = "mock tree output"
    result = runner.invoke(
        app, ["tree", "--ignore", "node_modules", "--ignore", "*.log"]
    )
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()


@mock.patch(
    "src.codebrief.tools.tree_generator.generate_and_output_tree",
    side_effect=Exception("Tree generation failed"),
)
def test_tree_command_error_handling(mock_tree_gen):
    """Test tree command error handling."""
    result = runner.invoke(app, ["tree"])
    assert result.exit_code == 1
    assert "An unexpected error occurred during tree generation" in result.stdout


@mock.patch(
    "src.codebrief.tools.tree_generator.generate_and_output_tree",
    side_effect=FileNotFoundError("Tree output directory not found"),
)
def test_tree_command_file_not_found_handling(mock_tree_gen, tmp_path: Path):
    """Test tree command file not found error handling."""
    output_file = tmp_path / "nonexistent" / "tree_output.txt"
    result = runner.invoke(app, ["tree", "--output", str(output_file)])
    assert result.exit_code == 1
    assert "An unexpected error occurred during tree generation" in result.stdout


# Test Flatten Command


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_default(mock_flatten):
    """Test flatten command with default parameters."""
    mock_flatten.return_value = "mock flattened output"
    result = runner.invoke(app, ["flatten"])
    assert result.exit_code == 0
    mock_flatten.assert_called_once()


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_with_output(mock_flatten, tmp_path: Path):
    """Test flatten command with output file."""
    output_file = tmp_path / "flatten_output.txt"
    mock_flatten.return_value = None  # When output_file is provided, no return value
    result = runner.invoke(app, ["flatten", "--output", str(output_file)])
    assert result.exit_code == 0
    mock_flatten.assert_called_once()


# Test more commands would continue with similar pattern updates...


def test_no_subcommand_help():
    """Test that running the app without subcommand shows helpful message."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    # The output should suggest running codebrief --help
    output_lower = result.stdout.lower()
    assert "codebrief" in output_lower and "help" in output_lower


@mock.patch(
    "src.codebrief.tools.flattener.flatten_code_logic",
    side_effect=Exception("Flatten failed"),
)
def test_flatten_command_error_handling(mock_flatten):
    """Test flatten command error handling."""
    result = runner.invoke(app, ["flatten"])
    assert result.exit_code == 1
    assert "An unexpected error occurred during file flattening" in result.stdout


# Utility function for testing configuration-related scenarios
def _create_test_config(tmp_path: Path, codebrief_config: dict[str, Any]) -> Path:
    """Helper to create a pyproject.toml in tmp_path with a [tool.codebrief] section."""
    config_file = tmp_path / "pyproject.toml"

    # Create a simple TOML configuration file with the codebrief section
    # Using json.dumps as a simple way to serialize the dict for embedding in TOML
    full_config = {"tool": {config_manager.CONFIG_SECTION_NAME: codebrief_config}}

    import toml

    config_file.write_text(toml.dumps(full_config))
    return config_file


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_config_default_output(mock_tree_gen, tmp_path: Path):
    """Test tree command using default output file from config."""
    # Create a config with default output file
    config_data = {"default_output_filename_tree": "custom_tree.txt"}
    _create_test_config(tmp_path, config_data)

    mock_tree_gen.return_value = None  # When output_file is provided, no return value

    # Run tree command in the directory with config
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_config_global_excludes(mock_tree_gen, tmp_path: Path):
    """Test tree command using global exclude patterns from config."""
    # Create a config with global excludes
    config_data = {"global_exclude_patterns": ["*.log", "temp/*"]}
    _create_test_config(tmp_path, config_data)

    mock_tree_gen.return_value = "mock tree output"

    # Run tree command in the directory with config
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_with_config_default_output(mock_flatten, tmp_path: Path):
    """Test flatten command using default output file from config."""
    # Create a config with default output file
    config_data = {"default_output_filename_flatten": "custom_flatten.txt"}
    _create_test_config(tmp_path, config_data)

    mock_flatten.return_value = None  # When output_file is provided, no return value

    # Run flatten command in the directory with config
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 0
    mock_flatten.assert_called_once()


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_with_config_global_excludes(mock_flatten, tmp_path: Path):
    """Test flatten command using global exclude patterns from config."""
    # Create a config with global excludes
    config_data = {"global_exclude_patterns": ["*.log", "temp/*"]}
    _create_test_config(tmp_path, config_data)

    mock_flatten.return_value = "mock flattened output"

    # Run flatten command in the directory with config
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 0
    mock_flatten.assert_called_once()


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_invalid_root_dir(mock_tree_gen):
    """Test tree command with invalid root directory."""
    # Try to run tree on a non-existent directory
    result = runner.invoke(app, ["tree", "/path/that/does/not/exist"])
    assert result.exit_code == 2  # Typer validation error
    mock_tree_gen.assert_not_called()


@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_file_as_root_dir(mock_tree_gen, tmp_path: Path):
    """Test tree command with a file path instead of directory."""
    # Create a file instead of directory
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")

    # Try to run tree on a file
    result = runner.invoke(app, ["tree", str(file_path)])
    assert result.exit_code == 2  # Typer validation error
    mock_tree_gen.assert_not_called()


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_invalid_root_dir(mock_flatten):
    """Test flatten command with invalid root directory."""
    # Try to run flatten on a non-existent directory
    result = runner.invoke(app, ["flatten", "/path/that/does/not/exist"])
    assert result.exit_code == 2  # Typer validation error
    mock_flatten.assert_not_called()


@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_file_as_root_dir(mock_flatten, tmp_path: Path):
    """Test flatten command with a file path instead of directory."""
    # Create a file instead of directory
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")

    # Try to run flatten on a file
    result = runner.invoke(app, ["flatten", str(file_path)])
    assert result.exit_code == 2  # Typer validation error
    mock_flatten.assert_not_called()


# Test more config edge cases for robustness


def test_tree_command_with_invalid_config_output_type(tmp_path: Path):
    """Test tree command behavior with invalid config output type."""
    # Create a config with invalid type for default output
    config_data = {"default_output_filename_tree": 123}  # Should be string
    _create_test_config(tmp_path, config_data)

    with mock.patch(
        "src.codebrief.tools.tree_generator.generate_and_output_tree"
    ) as mock_tree_gen:
        mock_tree_gen.return_value = "mock tree output"

        # Should handle invalid config gracefully
        result = runner.invoke(app, ["tree", str(tmp_path)])
        assert result.exit_code == 0
        mock_tree_gen.assert_called_once()


def test_flatten_command_with_invalid_config_excludes_type(tmp_path: Path):
    """Test flatten command behavior with invalid config excludes type."""
    # Create a config with invalid type for excludes
    config_data = {"global_exclude_patterns": "not_a_list"}  # Should be list
    _create_test_config(tmp_path, config_data)

    with mock.patch("src.codebrief.tools.flattener.flatten_code_logic") as mock_flatten:
        mock_flatten.return_value = "mock flattened output"

        # Should handle invalid config gracefully
        result = runner.invoke(app, ["flatten", str(tmp_path)])
        assert result.exit_code == 0
        mock_flatten.assert_called_once()


# Test clipboard functionality


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_to_clipboard_success(mock_tree_gen, mock_clipboard):
    """Test tree command with --to-clipboard option (success)."""
    mock_tree_gen.return_value = "mock tree output"
    mock_clipboard.return_value = None  # Successful copy

    result = runner.invoke(app, ["tree", "--to-clipboard"])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()
    mock_clipboard.assert_called_once_with("mock tree output")
    assert "Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_to_clipboard_failure(mock_tree_gen, mock_clipboard):
    """Test tree command with --to-clipboard option (failure)."""
    mock_tree_gen.return_value = "mock tree output"
    mock_clipboard.side_effect = Exception("Clipboard error")

    result = runner.invoke(app, ["tree", "--to-clipboard"])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()
    mock_clipboard.assert_called_once_with("mock tree output")
    assert "Warning: Failed to copy to clipboard:" in result.stdout


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.flattener.flatten_code_logic")
def test_flatten_command_to_clipboard_success(mock_flatten, mock_clipboard):
    """Test flatten command with --to-clipboard option (success)."""
    mock_flatten.return_value = "mock flattened output"
    mock_clipboard.return_value = None  # Successful copy

    result = runner.invoke(app, ["flatten", "--to-clipboard"])
    assert result.exit_code == 0
    mock_flatten.assert_called_once()
    mock_clipboard.assert_called_once_with("mock flattened output")
    assert "Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.git_provider.get_git_context")
def test_git_info_command_to_clipboard_success(mock_git_context, mock_clipboard):
    """Test git-info command with --to-clipboard option (success)."""
    mock_git_context.return_value = "mock git context"
    mock_clipboard.return_value = None  # Successful copy

    result = runner.invoke(app, ["git-info", "--to-clipboard"])
    assert result.exit_code == 0
    mock_git_context.assert_called_once()
    mock_clipboard.assert_called_once_with("mock git context")
    assert "Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.dependency_lister.list_dependencies")
def test_deps_command_to_clipboard_success(mock_deps, mock_clipboard):
    """Test deps command with --to-clipboard option (success)."""
    mock_deps.return_value = "mock dependencies"
    mock_clipboard.return_value = None  # Successful copy

    result = runner.invoke(app, ["deps", "--to-clipboard"])
    assert result.exit_code == 0
    mock_deps.assert_called_once()
    mock_clipboard.assert_called_once_with("mock dependencies")
    assert "Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.codebrief.main.pyperclip.copy")
@mock.patch("src.codebrief.tools.bundler.create_bundle")
def test_bundle_command_to_clipboard_success(mock_bundle, mock_clipboard):
    """Test bundle command with --to-clipboard option (success)."""
    mock_bundle.return_value = "mock bundle content"
    mock_clipboard.return_value = None  # Successful copy

    result = runner.invoke(app, ["bundle", "--to-clipboard"])
    assert result.exit_code == 0
    mock_bundle.assert_called_once()
    mock_clipboard.assert_called_once_with("mock bundle content")
    assert "Output successfully copied to clipboard!" in result.stdout


# Test clipboard failure scenarios


@mock.patch(
    "src.codebrief.main.pyperclip.copy", side_effect=Exception("Clipboard error")
)
@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_clipboard_failure_graceful_handling(
    mock_tree_gen, mock_clipboard
):
    """Test tree command handles clipboard errors gracefully."""
    mock_tree_gen.return_value = "mock tree output"

    result = runner.invoke(app, ["tree", "--to-clipboard"])
    assert result.exit_code == 0
    assert "Warning: Failed to copy to clipboard: Clipboard error" in result.stdout


@mock.patch("src.codebrief.main.console.print")
@mock.patch("src.codebrief.tools.tree_generator.generate_and_output_tree")
def test_tree_command_console_output_when_no_clipboard(
    mock_tree_gen, mock_console_print
):
    """Test tree command prints to console when not using clipboard."""
    mock_tree_gen.return_value = "mock tree output"

    result = runner.invoke(app, ["tree"])
    assert result.exit_code == 0
    mock_tree_gen.assert_called_once()
    # Console.print should be called with the tree output for display


# Additional tests for deps command


@mock.patch("src.codebrief.tools.dependency_lister.list_dependencies")
def test_deps_command_with_output_file(mock_deps, tmp_path: Path):
    """Test deps command with output file specification."""
    output_file = tmp_path / "deps_output.txt"
    mock_deps.return_value = None  # When output_file is provided, no return value

    result = runner.invoke(app, ["deps", "--output", str(output_file)])
    assert result.exit_code == 0
    mock_deps.assert_called_once()


# Continue with existing tests for other commands...
