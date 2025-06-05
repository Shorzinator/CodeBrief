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

from pathlib import Path
from typing import List, Optional

import typer # Typer is used for creating the CLI application and commands
from rich.console import Console # Rich is used for enhanced console output (colors, styles, tables, etc.)

# Import specific tool modules or functions from the 'tools' sub-package.
# The '.' indicates a relative import from the current package ('contextcraft').
from .tools import tree_generator

# Initialize a Typer application instance.
# This 'app' object will be used to register commands.
app = typer.Typer(
    name="contextcraft",  # The name of the CLI application
    help="A CLI toolkit to generate comprehensive project context for LLMs.", # Short help displayed for the app
    add_completion=False,  # Shell completion can be enabled later if desired (adds some overhead)
    # no_args_is_help=True, # Consider adding this: if no command is given, show help.
)

# Initialize a Rich Console instance for consistent styled output throughout the app.
console = Console()

@app.command() # Registers the following function as a CLI command
def hello(name: str = typer.Option("World", help="The person to greet.")):
    """
    Greets a person. (Example command)

    This command serves as a basic example to demonstrate how commands are
    defined and to test the CLI setup. It can be removed or modified
    as the application develops.
    """
    console.print(f"Hello [bold green]{name}[/bold green] from ContextCraft!")
    # Rich's print supports console markup for styling.

@app.command(name="tree") # Registers 'tree_command' as the 'tree' subcommand
def tree_command(
    root_dir: Path = typer.Argument(
        ".",  # Default value for the argument if not provided
        help="Root directory to generate tree for.", # Help text for this argument
        exists=True,  # Typer will validate that the path exists
        file_okay=False, # Path must not be a file
        dir_okay=True,   # Path must be a directory
        readable=True,   # Path must be readable
        resolve_path=True, # Converts the path to an absolute path
        show_default="Current directory", # How the default is displayed in --help
    ),
    output_file: Optional[Path] = typer.Option(
        None, # Default is None, meaning output to console
        "--output",  # Long option name
        "-o",        # Short option name
        help="Output file to save the tree. If not provided, prints to console.",
        writable=True, # If path is given, Typer checks if it's writable
        resolve_path=True, # Converts to absolute path if given
        show_default="Print to console", # How default is displayed in --help
    ),
    ignore: Optional[List[str]] = typer.Option(
        None, # Default is an empty list (no user-specified ignores beyond defaults)
        "--ignore",
        "-i",
        help=(
            "Specific directory or file names to ignore. "
            "Can be used multiple times (e.g., -i node_modules -i build)."
        ),
        show_default="Default internal exclusion list", # Describes the behavior if not specified
    ),
):
    """
    Generates and displays or saves a directory tree structure.

    This command traverses a directory starting from `ROOT_DIR` and
    creates a visual representation of its structure.

    By default, it excludes a predefined list of common development-related
    directories and files (e.g., .git, __pycache__, venv).
    Users can specify additional items to ignore by their names using the
    --ignore option. The output can be printed to the console (default)
    or saved to a specified --output file.
    """
    try:
        # Delegate the core logic to the tree_generator module.
        # This keeps the main.py cleaner and focused on CLI aspects.
        tree_generator.generate_and_output_tree(
            root_dir=root_dir,
            output_file_path=output_file,
            ignore_list=ignore,
        )
    except typer.Exit:
        # If Typer itself raises an Exit (e.g., due to failed path validation
        # in the argument processing), let it propagate to exit cleanly.
        raise
    except Exception as e:
        # Catch any other unexpected errors from the tree generation logic.
        console.print(f"[bold red]An unexpected error occurred during tree generation: {e}[/bold red]")
        # For debugging, you might want to uncomment the following lines to print the full traceback:
        # import traceback
        # console.print(f"[red]{traceback.format_exc()}[/red]")
        raise typer.Exit(code=1) # Exit with a non-zero status code to indicate failure.

# This block ensures that the Typer app runs when the script is executed directly
# (e.g., `python -m src.contextcraft.main`) or via the Poetry script entry point.
if __name__ == "__main__":
    app()