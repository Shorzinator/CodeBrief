# src/codebrief/main.py
"""Main CLI entry point for the CodeBrief application.

This module uses Typer to define and manage CLI commands. It orchestrates
functionalities from other modules, like generating directory trees or
flattening code.

The application provides a toolkit for developers to generate structured project
context, suitable for Large Language Models (LLMs) or general understanding.
"""

import warnings
from pathlib import Path
from typing import List, Optional

import pyperclip
import typer
from rich.console import Console

from . import __version__
from .tools import bundler, dependency_lister, flattener, git_provider, tree_generator
from .utils import config_manager


def version_callback(value: bool) -> None:
    """Show version information and exit."""
    if value:
        console.print(
            f"[bold green]CodeBrief[/bold green] Version: [bold cyan]{__version__}[/bold cyan]"
        )
        raise typer.Exit()


app = typer.Typer(
    name="codebrief",
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
) -> None:
    """
    A CLI toolkit to generate comprehensive project context for LLMs.

    CodeBrief helps you create detailed project context files for use with
    Large Language Models (LLMs). It can generate directory trees, flatten code
    files, extract git information, list dependencies, and create comprehensive
    bundles combining multiple outputs.
    """
    if ctx.invoked_subcommand is None:
        console.print(
            "[dim]Run [bold]codebrief --help[/bold] to see available commands.[/dim]"
        )


console = Console()


def _copy_to_clipboard_with_feedback(content: str) -> None:
    """Copy content to clipboard with user feedback."""
    try:
        pyperclip.copy(content)
        console.print("📋 Output successfully copied to clipboard!")
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to copy to clipboard: {e}[/yellow]")


@app.command()
def hello(name: str = typer.Option("World", help="The person to greet.")) -> None:
    """Greets a person. (Example command)"""
    console.print(f"Hello {name} from CodeBrief!")


@app.command(name="tree")
def tree_command(
    ctx: typer.Context,
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
    to_clipboard: bool = typer.Option(
        False,
        "--to-clipboard",
        "-c",
        help="Copy output to clipboard instead of printing to console. Only applies when no output file is specified.",
    ),
) -> None:
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
        tree_output = tree_generator.generate_and_output_tree(
            root_dir=root_dir,
            output_file_path=actual_output_path,
            ignore_list=cli_ignore_list,
            config_global_excludes=cfg_global_excludes,
        )

        # Handle clipboard functionality when no output file is specified
        if actual_output_path is None and tree_output is not None:
            if to_clipboard:
                _copy_to_clipboard_with_feedback(tree_output)
            else:
                console.print(tree_output, markup=False)

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
    ctx: typer.Context,
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
    to_clipboard: bool = typer.Option(
        False,
        "--to-clipboard",
        "-c",
        help="Copy output to clipboard instead of printing to console. Only applies when no output file is specified.",
    ),
) -> None:
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
        flattened_output = flattener.flatten_code_logic(
            root_dir=root_dir,
            output_file_path=actual_output_path,
            include_patterns=cli_include,
            exclude_patterns=cli_exclude,
            config_global_excludes=cfg_global_excludes,
        )

        # Handle clipboard functionality when no output file is specified
        if actual_output_path is None and flattened_output is not None:
            if to_clipboard:
                _copy_to_clipboard_with_feedback(flattened_output)
            else:
                # Use print() instead of console.print() to avoid Rich markup parsing of file contents
                print(flattened_output)

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
    ctx: typer.Context,
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
    to_clipboard: bool = typer.Option(
        False,
        "--to-clipboard",
        "-c",
        help="Copy output to clipboard instead of printing to console. Only applies when no output file is specified.",
    ),
) -> None:
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
        deps_output = dependency_lister.list_dependencies(
            project_path=project_path,
            output_file=actual_output_path,
        )

        # Handle clipboard functionality when no output file is specified
        if actual_output_path is None and deps_output is not None:
            if to_clipboard:
                _copy_to_clipboard_with_feedback(deps_output)
            else:
                # The dependency_lister already prints to console, but we need to handle clipboard case
                console.print("\n--- Project Dependencies ---")
                from rich.markdown import Markdown

                console.print(Markdown(deps_output))

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


@app.command(name="git-info")
def git_info_command(
    ctx: typer.Context,
    project_root: Path = typer.Argument(
        ".",
        help="Root directory of the Git repository. Config is read from here.",
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
            "Output file for Git context. Overrides config. "
            "If not set, prints to console."
        ),
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
    log_count: int = typer.Option(
        5,
        "--log-count",
        "-l",
        help="Number of recent commits to include in the output.",
        min=1,
        max=50,
        show_default=True,
    ),
    full_diff: bool = typer.Option(
        False,
        "--full-diff",
        help="Include full diff output for uncommitted changes.",
        show_default=True,
    ),
    diff_options: Optional[str] = typer.Option(
        None,
        "--diff-options",
        help=(
            "Additional options to pass to git diff command. "
            "Example: '--stat' for summary, 'HEAD~3' for specific range."
        ),
        show_default="None",
    ),
    to_clipboard: bool = typer.Option(
        False,
        "--to-clipboard",
        "-c",
        help="Copy output to clipboard instead of printing to console. Only applies when no output file is specified.",
    ),
) -> None:
    """Extract Git context information from a repository."""
    config = config_manager.load_config(project_root)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_git_info"):
        cfg_output_filename = config["default_output_filename_git_info"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = project_root / cfg_output_filename
            console.print(
                "[dim]Using default output file from config: "
                f"{actual_output_path.resolve()}[/dim]"
            )
        else:
            warnings.warn(
                "Config Warning: 'default_output_filename_git_info' should be a "
                f"string, got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    try:
        git_context = git_provider.get_git_context(
            project_root=project_root,
            diff_options=diff_options,
            log_count=log_count,
            full_diff=full_diff,
        )

        if actual_output_path:
            try:
                with open(actual_output_path, "w", encoding="utf-8") as f:
                    f.write(git_context)
                console.print(
                    f"[green]Successfully extracted Git context to: '{actual_output_path.resolve()}'[/green]"
                )
            except Exception as e:
                console.print(
                    f"[bold red]Error writing to '{actual_output_path}': {e}[/bold red]"
                )
                raise typer.Exit(code=1) from e
        else:
            # Handle clipboard functionality when no output file is specified
            if to_clipboard:
                _copy_to_clipboard_with_feedback(git_context)
            else:
                console.print(git_context)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            "[bold red]An unexpected error occurred during Git context extraction: [/bold red]",
            end="",
        )
        console.print(str(e), markup=False)
        raise typer.Exit(code=1) from e


@app.command(name="bundle")
def bundle_command(
    ctx: typer.Context,
    project_root: Path = typer.Argument(
        ".",
        help="Root directory of the project to bundle. Config is read from here.",
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
            "Output file for the context bundle. Overrides config. "
            "If not set, prints to console."
        ),
        writable=True,
        resolve_path=True,
        show_default="None (uses config or console)",
    ),
    exclude_tree: bool = typer.Option(
        False,
        "--exclude-tree",
        help="Exclude directory tree from the bundle.",
        show_default=True,
    ),
    exclude_git: bool = typer.Option(
        False,
        "--exclude-git",
        help="Exclude Git context from the bundle.",
        show_default=True,
    ),
    exclude_deps: bool = typer.Option(
        False,
        "--exclude-deps",
        help="Exclude project dependencies from the bundle.",
        show_default=True,
    ),
    flatten_paths: Optional[list[str]] = typer.Option(
        None,
        "--flatten",
        "-f",
        help=(
            "Additional paths to flatten and include in bundle. "
            "Can be used multiple times. Defaults to project root."
        ),
        show_default="None (includes project root)",
    ),
    git_log_count: int = typer.Option(
        5,
        "--git-log-count",
        help="Number of recent commits to include in Git context.",
        min=1,
        max=50,
        show_default=True,
    ),
    git_full_diff: bool = typer.Option(
        False,
        "--git-full-diff",
        help="Include full diff output in Git context.",
        show_default=True,
    ),
    git_diff_options: Optional[str] = typer.Option(
        None,
        "--git-diff-options",
        help=(
            "Additional options to pass to git diff command in Git context. "
            "Example: '--stat' for summary."
        ),
        show_default="None",
    ),
    to_clipboard: bool = typer.Option(
        False,
        "--to-clipboard",
        "-c",
        help="Copy output to clipboard instead of printing to console. Only applies when no output file is specified.",
    ),
) -> None:
    """Create a comprehensive context bundle with multiple tool outputs."""
    config = config_manager.load_config(project_root)

    actual_output_path: Optional[Path] = None
    if output_file:
        actual_output_path = output_file
    elif config.get("default_output_filename_bundle"):
        cfg_output_filename = config["default_output_filename_bundle"]
        if isinstance(cfg_output_filename, str):
            actual_output_path = project_root / cfg_output_filename
            console.print(
                "[dim]Using default output file from config: "
                f"{actual_output_path.resolve()}[/dim]"
            )
        else:
            warnings.warn(
                "Config Warning: 'default_output_filename_bundle' should be a "
                f"string, got {type(cfg_output_filename)}. Outputting to console.",
                UserWarning,
                stacklevel=2,
            )

    # Prepare flatten paths
    flatten_path_list: List[Path] = []
    if flatten_paths:
        for path_str in flatten_paths:
            path_obj = Path(path_str)
            if not path_obj.is_absolute():
                path_obj = project_root / path_obj
            if path_obj.exists():
                flatten_path_list.append(path_obj.resolve())
            else:
                console.print(
                    f"[yellow]Warning: Flatten path '{path_obj}' does not exist, skipping.[/yellow]"
                )
    else:
        # Default to project root
        flatten_path_list.append(project_root)

    try:
        bundle_output = bundler.create_bundle(
            project_root=project_root,
            output_file_path=actual_output_path,
            include_tree=not exclude_tree,
            include_git=not exclude_git,
            include_deps=not exclude_deps,
            flatten_paths=flatten_path_list,
            git_log_count=git_log_count,
            git_full_diff=git_full_diff,
            git_diff_options=git_diff_options,
        )

        # Handle clipboard functionality when no output file is specified
        if actual_output_path is None and bundle_output is not None:
            if to_clipboard:
                _copy_to_clipboard_with_feedback(bundle_output)
            else:
                # Print to console using Rich for better formatting
                from rich.markdown import Markdown

                markdown_obj = Markdown(bundle_output)
                console.print(markdown_obj)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            "[bold red]An unexpected error occurred during bundle creation: [/bold red]",
            end="",
        )
        console.print(str(e), markup=False)
        raise typer.Exit(code=1) from e


# This block ensures that the Typer app runs when the script is executed directly
# (e.g., `python -m src.codebrief.main`) or via the Poetry script entry point.
if __name__ == "__main__":  # pragma: no cover
    app()
