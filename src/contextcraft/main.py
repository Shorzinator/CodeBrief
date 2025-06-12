# src/contextcraft/main.py
"""
Main Command Line Interface (CLI) entry point for the ContextCraft application.

This module uses Typer to define and manage CLI commands. It serves as the orchestrator,
importing and invoking functionalities from other modules within the `contextcraft` package,
such as tools for generating directory trees or flattening code.

The application aims to provide a toolkit for developers to easily generate
structured context from their projects, suitable for use with Large Language Models (LLMs)
or for general project understanding.
"""

import warnings
from pathlib import Path
from typing import List, Optional

import typer  # Typer is used for creating the CLI application and commands
from rich.console import (
    Console,  # Rich is used for enhanced console output (colors, styles, tables, etc.)
)

from src.contextcraft.utils import config_manager

from . import __version__

# Import specific tool modules or functions from the 'tools' sub-package.
# The '.' indicates a relative import from the current package ('contextcraft').
from .tools import dependency_lister, flattener, tree_generator


# Callback function for the version option
def version_callback(value: bool):
    if value:
        console.print(f"ContextCraft Version: {__version__}")
        raise typer.Exit()


# Initialize a Typer application instance.
# This 'app' object will be used to register commands.
app = typer.Typer(
    name="contextcraft",  # The name of the CLI application
    help="A CLI toolkit to generate comprehensive project context for LLMs.",  # Short help displayed for the app
    add_completion=False,  # Shell completion can be enabled later if desired (adds some overhead)
    # no_args_is_help=True, # Consider adding this: if no command is given, show help.
)

# Add a top-level Typer Option for --version
# Note: We declare it at the app level, not as a command parameter.
# It's a bit unusual to put it directly in the Typer() constructor, usually it's a parameter to the main callback.
# A common way is to have a main function that Typer calls, and add it there.
# For a simple app like this, we can add it as a global parameter using a callback.


@app.callback(invoke_without_command=True)  # invoke_without_command needed if you have other global options
def main_options(
    ctx: typer.Context,  # Context object, useful if you have subcommands
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True,  # Eager means it runs before other processing, good for --version
    ),
):
    """
    ContextCraft: A CLI toolkit to generate comprehensive project context for LLMs.
    (Main app callback docstring, can be omitted if simple)
    """
    # If version_callback was called, it would have exited.
    # If other global options were present, they'd be processed here.
    # If no command is given and invoke_without_command=True, this function runs.
    # If a command IS given, this callback still runs first (due to how Typer handles callbacks),
    # then the command runs.
    if ctx.invoked_subcommand is None and not version:  # If no subcommand was called and version wasn't requested
        # Optionally, print help if no command is given and no other global option like version was processed
        # console.print(ctx.get_help())
        # typer.Exit()
        # Allow Typer to show help by default or handle via no_args_is_help in app constructor
        pass  # pragma: no cover


# Initialize a Rich Console instance for consistent styled output throughout the app.
console = Console()


@app.command()  # Registers the following function as a CLI command
def hello(name: str = typer.Option("World", help="The person to greet.")):
    """
    Greets a person. (Example command)

    This command serves as a basic example to demonstrate how commands are
    defined and to test the CLI setup. It can be removed or modified
    as the application develops.
    """
    console.print(f"Hello [bold green]{name}[/bold green] from ContextCraft!")
    # Rich's print supports console markup for styling.


@app.command(name="tree")  # Registers 'tree_command' as the 'tree' subcommand
def tree_command(
    # ... (root_dir argument remains the same) ...
    root_dir: Path = typer.Argument(
        ".",
        help="Root directory to generate tree for. Config file is read from here.",  # Updated help
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        show_default="Current directory",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to save the tree. Overrides config default. If neither is set, prints to console.",  # Updated help
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",  # Updated show_default
    ),
    ignore: Optional[List[str]] = typer.Option(
        None,
        "--ignore",
        "-i",
        help=(
            "Specific directory or file names to ignore. "
            "Can be used multiple times (e.g., -i node_modules -i build). "
            "Adds to .llmignore and config exclusions."
        ),  # Updated help
        show_default="None (uses .llmignore and config)",  # Updated show_default
    ),
):
    """
    Generates and displays or saves a directory tree structure.
    Uses .llmignore, pyproject.toml config, and CLI options for behavior.
    """
    # Load configuration from pyproject.toml in the root_dir
    # For commands operating on a root_dir, it's logical to load config from that root_dir.
    # If root_dir is '.', pyproject.toml is searched in the current working directory.
    config = config_manager.load_config(root_dir)  # Pass the target root_dir

    actual_output_path: Optional[Path] = None
    if output_file:  # CLI option takes highest precedence for output file
        actual_output_path = output_file
    elif config.get("default_output_filename_tree"):
        # Construct path relative to the root_dir where pyproject.toml was found
        # This ensures output files defined in config are placed relative to project root
        cfg_output_filename = config["default_output_filename_tree"]
        if isinstance(cfg_output_filename, str):  # Basic type check from config
            actual_output_path = root_dir / cfg_output_filename  # Paths in config are relative to project root
            console.print(f"[dim]Using default output file from config: {actual_output_path.resolve()}[/dim]")
        else:
            # This warning might also be handled within load_config if we make it stricter
            warnings.warn(
                f"Config Warning: 'default_output_filename_tree' should be a string, " f"got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    cli_ignore_list = ignore if ignore else []

    cfg_global_excludes = config.get("global_exclude_patterns", [])
    if not isinstance(cfg_global_excludes, list):
        warnings.warn("Config Warning: 'global_exclude_patterns' should be a list. Using empty list.", UserWarning, stacklevel=2)
        cfg_global_excludes = []

    try:
        tree_generator.generate_and_output_tree(
            root_dir=root_dir,
            output_file_path=actual_output_path,  # Use the resolved path
            ignore_list=cli_ignore_list,  # Pass CLI ignores
            config_global_excludes=cfg_global_excludes,
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred during tree generation: {e}[/bold red]")
        raise typer.Exit(code=1) from e


@app.command(name="flatten")
def flatten_command(
    root_dir: Path = typer.Argument(
        ".",
        help="Root directory to flatten files from. Config file is read from here.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,  # Converts to an absolute path internally
        show_default="Current directory",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to save the flattened content. Overrides config default. If neither, prints to console.",
        writable=True,  # Typer checks if the path (if given) is writable
        resolve_path=True,  # Converts to an absolute path if provided
        show_default="None (uses config or console)",
    ),
    include: Optional[List[str]] = typer.Option(
        None,
        "--include",
        "-inc",
        help=(
            "Specify file inclusion criteria. Can be file extensions (e.g., '.py'), "
            "glob patterns (e.g., '*.js', 'src/**/*.ts'), or exact filenames (e.g., 'Makefile'). "
            "Use multiple times for multiple criteria (e.g., -inc '*.py' -inc '*.md'). "
            "If not provided, a default list of common code/text file types is used."
        ),
        show_default="None (uses config or tool defaults)",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "--exclude",
        "-exc",
        help=(
            "Specify files or patterns to exclude. Can be glob patterns (e.g., '*.log', 'dist/*') "
            "or exact filenames. Exclusions apply after general default exclusions (like .git, venv) "
            "and take precedence over include patterns. Use multiple times for multiple criteria."
        ),
        show_default="None (uses .llmignore and config)",
    ),
):
    """
    Flattens specified files from a directory into a single text output.

    This command recursively searches the `ROOT_DIR` for files that match the
    inclusion criteria (either user-defined via --include or a default set of
    common code/text file types) and do not match exclusion criteria
    (user-defined via --exclude or default general exclusions like .git, venv).

    The content of each processed file is concatenated into the output,
    with each file's content being prefixed by a standardized header comment
    indicating its original relative path (e.g., `# --- File: src/main.py ---`).

    This is useful for creating a single context bundle for LLMs, archiving
    key project files, or performing global searches/reviews.
    """
    config = config_manager.load_config(root_dir)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_flatten"):
        cfg_output_filename = config["default_output_filename_flatten"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = root_dir / cfg_output_filename
            console.print(f"[dim]Using default output file from config: {actual_output_path.resolve()}[/dim]")
        else:
            warnings.warn(
                f"Config Warning: 'default_output_filename_flatten' should be a string, " f"got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    # TODO LATER: Logic for include_patterns precedence: CLI > Config > Tool Default
    actual_include_patterns = include  # For now, just CLI or None

    # TODO LATER: Logic for exclude_patterns precedence: Merge CLI + Config + .llmignore handled by ignore_handler
    actual_exclude_patterns = exclude  # For now, just CLI or None

    cfg_global_excludes = config.get("global_exclude_patterns", [])
    if not isinstance(cfg_global_excludes, list):
        warnings.warn("Config Warning: 'global_exclude_patterns' should be a list. Using empty list.", UserWarning, stacklevel=2)
        cfg_global_excludes = []

    try:
        flattener.flatten_code_logic(
            root_dir_path=root_dir,
            output_file_path=actual_output_path,
            include_patterns=actual_include_patterns,
            exclude_patterns=actual_exclude_patterns,
            # config_global_include_patterns=config.get("global_include_patterns", []), # For later
            # config_global_exclude_patterns=config.get("global_exclude_patterns", [])  # For later
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred during code flattening: {e}[/bold red]")
        raise typer.Exit(code=1) from e


@app.command(name="deps")
def deps_command(
    project_path: Path = typer.Argument(
        ".",
        help="Project directory to analyze for dependencies. Config file is read from here.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        show_default="Current directory",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to save the dependency list. Overrides config default. If neither is set, prints to console.",
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
):
    """
    Lists project dependencies from various package manager files.

    This command analyzes the project directory for supported dependency files
    (pyproject.toml, requirements.txt, package.json) and extracts dependency
    information. The output is formatted as structured Markdown, suitable for
    inclusion in context bundles or documentation.

    Supported file formats:
    - Python: pyproject.toml (Poetry and PEP 621), requirements.txt files
    - Node.js: package.json

    Dependencies are grouped by language, file type, and dependency group
    (main, dev, test, etc.) for clear organization.
    """
    # Load configuration from pyproject.toml in the project_path
    config = config_manager.load_config(project_path)

    actual_output_path: Optional[Path] = None
    if output_file:  # CLI option takes highest precedence for output file
        actual_output_path = output_file
    elif config.get("default_output_filename_deps"):
        # Construct path relative to the project_path where pyproject.toml was found
        cfg_output_filename = config["default_output_filename_deps"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = project_path / cfg_output_filename
            console.print(f"[dim]Using default output file from config: {actual_output_path.resolve()}[/dim]")
        else:
            warnings.warn(
                f"Config Warning: 'default_output_filename_deps' should be a string, "
                f"got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    try:
        dependency_lister.list_dependencies_logic(
            project_path=project_path,
            actual_output_path=actual_output_path,
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred during dependency listing: {e}[/bold red]")
        raise typer.Exit(code=1) from e


# This block ensures that the Typer app runs when the script is executed directly
# (e.g., `python -m src.contextcraft.main`) or via the Poetry script entry point.
if __name__ == "__main__":  # pragma: no cover
    app()
