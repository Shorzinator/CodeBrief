# src/contextcraft/main.py
"""Main CLI entry point for the ContextCraft application.

This module uses Typer to define and manage CLI commands. It orchestrates
functionalities from other modules, like generating directory trees or
flattening code.

The application provides a toolkit for developers to generate structured project
context, suitable for Large Language Models (LLMs) or general understanding.
"""

import warnings
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from src.contextcraft.utils import config_manager

from . import __version__
from .tools import dependency_lister, flattener, tree_generator


def version_callback(value: bool):
    """Exit after showing the version."""
    if value:
        console.print(f"ContextCraft Version: {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="contextcraft",
    help="A CLI toolkit to generate comprehensive project context for LLMs.",
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def main_options(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """ContextCraft: A CLI toolkit to generate project context for LLMs."""
    if ctx.invoked_subcommand is None and not version:
        pass  # pragma: no cover


console = Console()


@app.command()
def hello(name: str = typer.Option("World", help="The person to greet.")):
    """Greets a person. (Example command)"""
    console.print(f"Hello [bold green]{name}[/bold green] from ContextCraft!")


@app.command(name="tree")
def tree_command(
    root_dir: Path = typer.Argument(
        ".",
        help="Root directory to generate tree for. Config is read from here.",
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
        help=(
            "Output file to save the tree. Overrides config default. "
            "If not set, prints to console."
        ),
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
    ignore: Optional[list[str]] = typer.Option(
        None,
        "--ignore",
        "-i",
        help=(
            "Directory/file names to ignore. Can be used multiple times. "
            "Adds to .llmignore and config exclusions."
        ),
        show_default="None (uses .llmignore and config)",
    ),
):
    """Generate and display or save a directory tree structure."""
    config = config_manager.load_config(root_dir)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_tree"):
        cfg_output_filename = config["default_output_filename_tree"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = root_dir / cfg_output_filename
            console.print(
                "[dim]Using default output file from config: "
                f"{actual_output_path.resolve()}[/dim]"
            )
        else:
            warnings.warn(
                "Config Warning: 'default_output_filename_tree' should be a "
                f"string, got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    cli_ignore_list = ignore if ignore else []

    cfg_global_excludes = config.get("global_exclude_patterns", [])
    if not isinstance(cfg_global_excludes, list):
        warnings.warn(
            "Config Warning: 'global_exclude_patterns' should be a list. "
            "Using empty list.",
            UserWarning,
            stacklevel=2,
        )
        cfg_global_excludes = []

    try:
        tree_generator.generate_and_output_tree(
            root_dir=root_dir,
            output_file_path=actual_output_path,
            ignore_list=cli_ignore_list,
            config_global_excludes=cfg_global_excludes,
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            "[bold red]An unexpected error occurred during tree generation: [/bold red]",
            end="",
        )
        console.print(str(e), markup=False)
        raise typer.Exit(code=1) from e


@app.command(name="flatten")
def flatten_command(
    root_dir: Path = typer.Argument(
        ".",
        help="Root directory to flatten. Config is read from here.",
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
        help=(
            "Output file for flattened content. Overrides config. "
            "If not set, prints to console."
        ),
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
    include: Optional[list[str]] = typer.Option(
        None,
        "--include",
        "-inc",
        help=(
            "File inclusion criteria (e.g., '.py', '*.js', 'Makefile'). "
            "Use multiple times. Defaults to common code/text file types."
        ),
        show_default="None (uses config or tool defaults)",
    ),
    exclude: Optional[list[str]] = typer.Option(
        None,
        "--exclude",
        "-exc",
        help=(
            "Files or patterns to exclude (e.g., '*.log', 'dist/*'). "
            "Takes precedence over includes. Use multiple times."
        ),
        show_default="None (uses .llmignore and config)",
    ),
):
    """Flatten specified files from a directory into a single text output."""
    config = config_manager.load_config(root_dir)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_flatten"):
        cfg_output_filename = config["default_output_filename_flatten"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = root_dir / cfg_output_filename
            console.print(
                "[dim]Using default output file from config: "
                f"{actual_output_path.resolve()}[/dim]"
            )
        else:
            warnings.warn(
                "Config Warning: 'default_output_filename_flatten' should be a "
                f"string, got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    cli_include = include if include else []
    cli_exclude = exclude if exclude else []

    cfg_global_excludes = config.get("global_exclude_patterns", [])
    if not isinstance(cfg_global_excludes, list):
        warnings.warn(
            "Config Warning: 'global_exclude_patterns' should be a list. "
            "Using empty list.",
            UserWarning,
            stacklevel=2,
        )
        cfg_global_excludes = []

    try:
        flattener.flatten_code_logic(
            root_dir=root_dir,
            output_file_path=actual_output_path,
            include_patterns=cli_include,
            exclude_patterns=cli_exclude,
            config_global_excludes=cfg_global_excludes,
        )
    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            "[bold red]An unexpected error occurred during file flattening: [/bold red]",
            end="",
        )
        console.print(str(e), markup=False)
        raise typer.Exit(code=1) from e


@app.command(name="deps")
def deps_command(
    project_path: Path = typer.Argument(
        ".",
        help="Project directory to analyze. Config is read from here.",
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
        help=(
            "Output file for dependency list. Overrides config. "
            "If not set, prints to console."
        ),
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
):
    """List project dependencies from various package manager files."""
    config = config_manager.load_config(project_path)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_deps"):
        cfg_output_filename = config["default_output_filename_deps"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = project_path / cfg_output_filename
            console.print(
                "[dim]Using default output file from config: "
                f"{actual_output_path.resolve()}[/dim]"
            )
        else:
            warnings.warn(
                "Config Warning: 'default_output_filename_deps' should be a "
                f"string, got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    try:
        dependency_lister.list_dependencies(
            project_path=project_path,
            output_file=actual_output_path,
        )
    except FileNotFoundError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(
            "[bold red]An unexpected error occurred during dependency listing: [/bold red]",
            end="",
        )
        console.print(str(e), markup=False)
        raise typer.Exit(code=1) from e


# This block ensures that the Typer app runs when the script is executed directly
# (e.g., `python -m src.contextcraft.main`) or via the Poetry script entry point.
if __name__ == "__main__":  # pragma: no cover
    app()
