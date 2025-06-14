# tests/test_main.py
"""Tests for the main CLI application in src.contextcraft.main.
Uses Typer's CliRunner for invoking commands.
"""
from pathlib import Path
from typing import Any
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
    # Check for key content without depending on exact formatting
    assert "hello" in result.stdout.lower()
    assert "options" in result.stdout.lower()
    assert "greets a person" in result.stdout.lower()  # Check for part of the docstring


# --- Tests for the 'tree' command ---


def test_tree_command_help():
    """Test the --help option for the tree command."""
    result = runner.invoke(app, ["tree", "--help"])
    assert result.exit_code == 0
    # Check for key content without depending on exact formatting
    assert "tree" in result.stdout.lower()
    assert "options" in result.stdout.lower()
    assert "root_dir" in result.stdout.lower()
    assert "generate and display or save a directory tree" in result.stdout.lower()


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
        root_dir=tmp_path.resolve(),
        output_file_path=output_file.resolve(),
        ignore_list=[],
        config_global_excludes=[],
    )


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_ignore_flags(mock_generate_tree, tmp_path: Path):
    """Test tree command with ignore flags."""
    result = runner.invoke(
        app, ["tree", str(tmp_path), "--ignore", "venv", "--ignore", "*.pyc"]
    )
    assert result.exit_code == 0
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=None,
        ignore_list=["venv", "*.pyc"],
        config_global_excludes=[],
    )


@mock.patch(
    "src.contextcraft.tools.tree_generator.generate_and_output_tree",
    side_effect=Exception("Tree generation failed!"),
)
def test_tree_command_handles_exception(mock_generate_tree_error, tmp_path: Path):
    """Test that tree command handles exceptions from the underlying tool and exits non-zero."""
    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 1  # As defined in main.py's except block
    assert (
        "An unexpected error occurred during tree generation: Tree generation failed!"
        in result.stdout
    )
    mock_generate_tree_error.assert_called_once()


def test_tree_command_invalid_root_dir():
    """Test tree command with a non-existent root directory."""
    # Typer should handle `exists=True` and exit before our code is called.
    # The exit code from Typer for validation errors is typically 2.
    result = runner.invoke(app, ["tree", "non_existent_directory_for_testing"])
    assert result.exit_code != 0  # Typer's validation error, often 2
    assert (
        "Invalid value for 'ROOT_DIR'" in result.stderr
        or "does not exist" in result.stderr
    )  # Typer's error message


@mock.patch(
    "src.contextcraft.tools.tree_generator.generate_and_output_tree",
    side_effect=typer.Exit(code=5),
)
def test_tree_command_propagates_typer_exit(
    mock_generate_tree_typer_exit, tmp_path: Path
):
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
    # Check for key content without depending on exact formatting
    assert "flatten" in result.stdout.lower()
    assert "options" in result.stdout.lower()
    assert "root_dir" in result.stdout.lower()
    assert "flatten specified files from a directory" in result.stdout.lower()


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_success(mock_flatten_logic, tmp_path: Path):
    """Test flatten command successful execution (mocking actual flattening)."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=None,
        include_patterns=[],
        exclude_patterns=[],
        config_global_excludes=[],
    )


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_with_options(mock_flatten_logic, tmp_path: Path):
    """Test flatten command with include, exclude, and output options."""
    output_f = tmp_path / "flat.txt"
    result = runner.invoke(
        app,
        [
            "flatten",
            str(tmp_path),
            "--output",
            str(output_f),
            "--include",
            "*.py",
            "--include",
            "*.md",
            "--exclude",
            "temp/*",
        ],
    )
    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=output_f.resolve(),
        include_patterns=["*.py", "*.md"],
        exclude_patterns=["temp/*"],
        config_global_excludes=[],
    )


@mock.patch(
    "src.contextcraft.tools.flattener.flatten_code_logic",
    side_effect=Exception("Flattening failed!"),
)
def test_flatten_command_handles_exception(mock_flatten_error, tmp_path: Path):
    """Test that flatten command handles exceptions and exits non-zero."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 1
    assert (
        "An unexpected error occurred during file flattening: Flattening failed!"
        in result.stdout
    )
    mock_flatten_error.assert_called_once()


# --- Test for main app help ---
def test_app_help():
    """Test the main application's --help output."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for key content without depending on exact formatting
    assert "contextcraft" in result.stdout.lower()
    assert "options" in result.stdout.lower()
    assert "command" in result.stdout.lower()
    assert "hello" in result.stdout.lower()
    assert "tree" in result.stdout.lower()
    assert "flatten" in result.stdout.lower()


@mock.patch(
    "src.contextcraft.tools.flattener.flatten_code_logic",
    side_effect=typer.Exit(code=6),
)
def test_flatten_command_propagates_typer_exit(
    mock_flatten_logic_typer_exit, tmp_path: Path
):
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
    assert (
        f"ContextCraft Version: {__version__}" in result.stdout
    )  # Check for the full string


def test_app_version_short_flag():
    """Test the -v (short) flag for version."""
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert f"ContextCraft Version: {__version__}" in result.stdout


# ---  Tests for config default output filenames ---


def create_pyproject_with_config(
    tmp_path: Path, contextcraft_config: dict[str, Any]
) -> Path:
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
    create_pyproject_with_config(
        tmp_path, {"default_output_filename_tree": config_output_filename}
    )

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
    create_pyproject_with_config(
        tmp_path, {"default_output_filename_tree": config_output_filename}
    )

    cli_output_path = tmp_path / cli_output_filename

    result = runner.invoke(
        app, ["tree", str(tmp_path), "--output", str(cli_output_path)]
    )

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    assert kwargs.get("output_file_path") == cli_output_path.resolve()
    assert (
        "Using default output file from config" not in result.stdout
    )  # Should not print this if CLI overrides


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_uses_config_default_output(mock_flatten_logic, tmp_path: Path):
    """Test `flatten` uses default_output_filename_flatten from config."""
    config_output_filename = "configured_flat.md"
    create_pyproject_with_config(
        tmp_path, {"default_output_filename_flatten": config_output_filename}
    )

    result = runner.invoke(app, ["flatten", str(tmp_path)])

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    expected_output_path = (tmp_path / config_output_filename).resolve()
    assert kwargs.get("output_file_path") == expected_output_path
    assert "Using default output file from config" in result.stdout


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_cli_output_overrides_config(
    mock_flatten_logic, tmp_path: Path
):
    """Test `flatten` --output CLI flag overrides configured default."""
    config_output_filename = "configured_flat.md"
    cli_output_filename = "cli_flat.md"
    create_pyproject_with_config(
        tmp_path, {"default_output_filename_flatten": config_output_filename}
    )

    cli_output_path = tmp_path / cli_output_filename

    result = runner.invoke(
        app, ["flatten", str(tmp_path), "--output", str(cli_output_path)]
    )

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    assert kwargs.get("output_file_path") == cli_output_path.resolve()
    assert "Using default output file from config" not in result.stdout


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_no_output_options_prints_to_console(
    mock_generate_tree, tmp_path: Path
):
    """Test `tree` prints to console if no CLI/config output is set (mocking actual generation)."""
    # Use a clean tmp_path without a pyproject.toml defining default output
    # Mock the tree generation to avoid actual tree printing, just check it was called correctly

    # Create a dummy file so the directory isn't empty, for a more realistic tree call
    (tmp_path / "dummy.txt").touch()
    result = runner.invoke(app, ["tree", str(tmp_path)])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    assert (
        kwargs.get("output_file_path") is None
    )  # Crucial: should be None for console output
    # We can't easily assert console output here because it's the mocked function's job.
    # We trust generate_and_output_tree to print to console if output_file_path is None.


# --- Tests for config global_exclude_patterns ---


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_uses_config_global_excludes(mock_generate_tree, tmp_path: Path):
    """Test `tree` command applies global_exclude_patterns from config."""
    config_data = {"global_exclude_patterns": ["*.log", "build/"]}
    create_pyproject_with_config(tmp_path, config_data)

    result = runner.invoke(app, ["tree", str(tmp_path)])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    # ignore_list is for CLI --ignore, config_global_excludes is separate
    assert kwargs.get("ignore_list") == []
    assert kwargs.get("config_global_excludes") == ["*.log", "build/"]


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_cli_ignore_augments_config_global_excludes(
    mock_generate_tree, tmp_path: Path
):
    """Test `tree` CLI --ignore adds to config's global_exclude_patterns."""
    config_data = {"global_exclude_patterns": ["*.log"]}
    create_pyproject_with_config(tmp_path, config_data)

    cli_ignore_val = "temp/"
    result = runner.invoke(app, ["tree", str(tmp_path), "--ignore", cli_ignore_val])

    assert result.exit_code == 0
    mock_generate_tree.assert_called_once()
    args, kwargs = mock_generate_tree.call_args
    assert kwargs.get("ignore_list") == [cli_ignore_val]  # CLI ignores
    assert kwargs.get("config_global_excludes") == ["*.log"]  # Config excludes

    # Note: The actual merging/precedence of these lists happens inside ignore_handler.is_path_ignored.
    # Here, we are just verifying that main.py passes them correctly to the tool function.


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_uses_config_global_excludes(mock_flatten_logic, tmp_path: Path):
    """Test `flatten` command applies global_exclude_patterns from config."""
    config_data = {"global_exclude_patterns": ["__pycache__/", "*.tmp"]}
    create_pyproject_with_config(tmp_path, config_data)

    result = runner.invoke(app, ["flatten", str(tmp_path)])

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    assert kwargs.get("exclude_patterns") == []  # CLI --exclude
    assert kwargs.get("config_global_excludes") == ["__pycache__/", "*.tmp"]


@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_cli_exclude_augments_config_global_excludes(
    mock_flatten_logic, tmp_path: Path
):
    """Test `flatten` CLI --exclude adds to config's global_exclude_patterns."""
    config_data = {"global_exclude_patterns": ["node_modules/"]}
    create_pyproject_with_config(tmp_path, config_data)

    cli_exclude_val = "*.css"
    result = runner.invoke(
        app, ["flatten", str(tmp_path), "--exclude", cli_exclude_val]
    )

    assert result.exit_code == 0
    mock_flatten_logic.assert_called_once()
    args, kwargs = mock_flatten_logic.call_args
    assert kwargs.get("exclude_patterns") == [cli_exclude_val]  # CLI excludes
    assert kwargs.get("config_global_excludes") == ["node_modules/"]


# --- More comprehensive integration tests (without mocking tool logic) ---
# These will test the actual output when config excludes are active.


def test_tree_integration_with_config_excludes(tmp_path: Path):
    """Actual tree output test with config global_exclude_patterns."""
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    create_pyproject_with_config(
        project_dir, {"global_exclude_patterns": ["*.log", "temp/"]}
    )

    (project_dir / "file.py").touch()
    (project_dir / "data.log").touch()  # Should be excluded by config
    (project_dir / "temp").mkdir()
    (project_dir / "temp" / "file_in_temp.txt").touch()  # Should be excluded by config
    (project_dir / "src").mkdir()
    (project_dir / "src" / "main.py").touch()

    output_file = project_dir / "tree_with_config_excludes.txt"

    # Run tree command targeting the project_dir where pyproject.toml is
    result = runner.invoke(
        app, ["tree", str(project_dir), "--output", str(output_file)]
    )
    assert result.exit_code == 0

    assert output_file.exists()
    content = output_file.read_text().strip()

    # Check that files that should be included are present
    assert "file.py" in content
    assert "src" in content
    assert "main.py" in content
    assert "pyproject.toml" in content

    # Check that excluded files are NOT present
    assert "data.log" not in content  # Should be excluded by *.log
    assert "temp" not in content  # Should be excluded by temp/
    assert "file_in_temp.txt" not in content  # Should be excluded by temp/


def test_flatten_integration_with_config_excludes(tmp_path: Path):
    """Actual flatten output test with config global_exclude_patterns."""
    project_dir = tmp_path / "proj"
    project_dir.mkdir()

    create_pyproject_with_config(
        project_dir, {"global_exclude_patterns": ["ignored.py", "docs/"]}
    )

    (project_dir / "app.py").write_text("print('app')")
    (project_dir / "ignored.py").write_text("print('ignored')")  # Excluded by config
    (project_dir / "docs").mkdir()
    (project_dir / "docs" / "index.md").write_text("# Docs")  # Excluded by config
    (project_dir / "utils.py").write_text("print('utils')")

    output_file = project_dir / "flatten_with_config_excludes.txt"

    # Run flatten; rely on default include patterns (which should include .py)
    result = runner.invoke(
        app, ["flatten", str(project_dir), "--output", str(output_file)]
    )
    assert result.exit_code == 0

    assert output_file.exists()
    content = output_file.read_text()

    assert "# --- File: app.py ---" in content
    assert "print('app')" in content
    assert "# --- File: utils.py ---" in content
    assert "print('utils')" in content

    # Check that the actual ignored files are not included (check for file headers)
    assert "# --- File: ignored.py ---" not in content
    assert "# --- File: docs/index.md ---" not in content
    assert "print('ignored')" not in content  # Content from ignored.py
    assert "# Docs" not in content  # Content from docs/index.md


# --- Test for exceptions with markup-like chars in the message ---


class ProblematicError(Exception):
    def __str__(self):
        return "Error with [square brackets] and maybe a backslash \\!"


@mock.patch(
    "src.contextcraft.tools.flattener.flatten_code_logic",
    side_effect=ProblematicError(),
)
def test_flatten_command_handles_exception_with_markup_chars(
    mock_flatten_error, tmp_path: Path
):
    """Test flatten command handles exceptions with markup-like chars in the message."""
    result = runner.invoke(app, ["flatten", str(tmp_path)])
    assert result.exit_code == 1

    # Verify the original error message is printed (now without markup parsing)
    assert "Error with [square brackets] and maybe a backslash \\!" in result.stdout
    # Check that no MarkupError occurred and the core message is there:
    assert "An unexpected error occurred during file flattening:" in result.stdout
    mock_flatten_error.assert_called_once()


# --- Tests for clipboard functionality ---


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_clipboard_flag(
    mock_generate_tree, mock_clipboard_copy, tmp_path: Path
):
    """Test tree command with --to-clipboard flag copies output to clipboard."""
    mock_tree_output = "Sample tree output"
    mock_generate_tree.return_value = mock_tree_output

    result = runner.invoke(app, ["tree", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    # Verify tree generator was called correctly
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=None,
        ignore_list=[],
        config_global_excludes=[],
    )

    # Verify clipboard copy was called with tree output
    mock_clipboard_copy.assert_called_once_with(mock_tree_output)

    # Verify success message is shown
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_with_short_clipboard_flag(
    mock_generate_tree, mock_clipboard_copy, tmp_path: Path
):
    """Test tree command with -c flag (short form) copies output to clipboard."""
    mock_tree_output = "Sample tree output"
    mock_generate_tree.return_value = mock_tree_output

    result = runner.invoke(app, ["tree", str(tmp_path), "-c"])
    assert result.exit_code == 0

    mock_clipboard_copy.assert_called_once_with(mock_tree_output)
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.flattener.flatten_code_logic")
def test_flatten_command_with_clipboard_flag(
    mock_flatten_logic, mock_clipboard_copy, tmp_path: Path
):
    """Test flatten command with --to-clipboard flag copies output to clipboard."""
    mock_flatten_output = "Sample flattened output"
    mock_flatten_logic.return_value = mock_flatten_output

    result = runner.invoke(app, ["flatten", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    mock_flatten_logic.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=None,
        include_patterns=[],
        exclude_patterns=[],
        config_global_excludes=[],
    )

    mock_clipboard_copy.assert_called_once_with(mock_flatten_output)
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.git_provider.get_git_context")
def test_git_info_command_with_clipboard_flag(
    mock_git_context, mock_clipboard_copy, tmp_path: Path
):
    """Test git-info command with --to-clipboard flag copies output to clipboard."""
    mock_git_output = "Sample git context output"
    mock_git_context.return_value = mock_git_output

    result = runner.invoke(app, ["git-info", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    mock_git_context.assert_called_once_with(
        project_root=tmp_path.resolve(),
        diff_options=None,
        log_count=5,
        full_diff=False,
    )

    mock_clipboard_copy.assert_called_once_with(mock_git_output)
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.dependency_lister.list_dependencies")
def test_deps_command_with_clipboard_flag(
    mock_list_deps, mock_clipboard_copy, tmp_path: Path
):
    """Test deps command with --to-clipboard flag copies output to clipboard."""
    mock_deps_output = "Sample dependencies output"
    mock_list_deps.return_value = mock_deps_output

    result = runner.invoke(app, ["deps", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    mock_list_deps.assert_called_once_with(
        project_path=tmp_path.resolve(),
        output_file=None,
    )

    mock_clipboard_copy.assert_called_once_with(mock_deps_output)
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.main.pyperclip.copy")
@mock.patch("src.contextcraft.tools.bundler.create_bundle")
def test_bundle_command_with_clipboard_flag(
    mock_create_bundle, mock_clipboard_copy, tmp_path: Path
):
    """Test bundle command with --to-clipboard flag copies output to clipboard."""
    mock_bundle_output = "Sample bundle output"
    mock_create_bundle.return_value = mock_bundle_output

    result = runner.invoke(app, ["bundle", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    mock_create_bundle.assert_called_once()
    mock_clipboard_copy.assert_called_once_with(mock_bundle_output)
    assert "📋 Output successfully copied to clipboard!" in result.stdout


@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_clipboard_flag_ignored_when_output_file_specified(
    mock_generate_tree, tmp_path: Path
):
    """Test that --to-clipboard flag is ignored when --output file is specified."""
    output_file = tmp_path / "tree_output.txt"
    mock_generate_tree.return_value = None  # Returns None when output file is specified

    result = runner.invoke(
        app, ["tree", str(tmp_path), "--output", str(output_file), "--to-clipboard"]
    )
    assert result.exit_code == 0

    # Verify tree generator was called with output file
    mock_generate_tree.assert_called_once_with(
        root_dir=tmp_path.resolve(),
        output_file_path=output_file.resolve(),
        ignore_list=[],
        config_global_excludes=[],
    )

    # Verify clipboard success message is NOT shown since output went to file
    assert "📋 Output successfully copied to clipboard!" not in result.stdout


@mock.patch(
    "src.contextcraft.main.pyperclip.copy", side_effect=Exception("Clipboard error")
)
@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_clipboard_error_handling(
    mock_generate_tree, mock_clipboard_copy, tmp_path: Path
):
    """Test that clipboard errors are handled gracefully with warning message."""
    mock_tree_output = "Sample tree output"
    mock_generate_tree.return_value = mock_tree_output

    result = runner.invoke(app, ["tree", str(tmp_path), "--to-clipboard"])
    assert result.exit_code == 0

    # Verify clipboard copy was attempted
    mock_clipboard_copy.assert_called_once_with(mock_tree_output)

    # Verify error warning is shown
    assert "Warning: Failed to copy to clipboard: Clipboard error" in result.stdout


@mock.patch("src.contextcraft.main.console.print")
@mock.patch("src.contextcraft.tools.tree_generator.generate_and_output_tree")
def test_tree_command_normal_console_output_without_clipboard_flag(
    mock_generate_tree, mock_console_print, tmp_path: Path
):
    """Test tree command without --to-clipboard flag prints to console normally."""
    mock_tree_output = "Sample tree output"
    mock_generate_tree.return_value = mock_tree_output

    result = runner.invoke(app, ["tree", str(tmp_path)])
    assert result.exit_code == 0

    # Verify console.print was called with the tree output (markup=False)
    mock_console_print.assert_called_with(mock_tree_output, markup=False)

    # Verify clipboard success message is NOT shown
    assert "📋 Output successfully copied to clipboard!" not in result.stdout


@mock.patch("src.contextcraft.tools.dependency_lister.list_dependencies")
def test_deps_command_normal_console_output_without_clipboard_flag(
    mock_list_deps, tmp_path: Path
):
    """Test deps command without --to-clipboard flag prints to console normally."""
    mock_deps_output = "Sample dependencies output"
    mock_list_deps.return_value = mock_deps_output

    result = runner.invoke(app, ["deps", str(tmp_path)])
    assert result.exit_code == 0

    # For deps command, we expect the console output to be handled by the command
    # since it has its own formatting with Markdown
    assert "--- Project Dependencies ---" in result.stdout
