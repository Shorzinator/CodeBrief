# src/contextcraft/tools/tree_generator.py
"""
Directory Tree Generation Utilities.

This module provides functions to generate a textual or Rich-enhanced representation
of a directory's structure. It supports excluding specified files and directories
and can output the tree to the console or a file.

Core functionalities:
- Recursive traversal of directories.
- Filtering of items based on .llmignore files, CLI arguments, core system
  exclusions, and a default set of common development artifacts.
- Generation of plain text tree for file output.
- Generation of a Rich `Tree` object for styled console output.
"""

from pathlib import Path
from typing import List, Optional, Set

import pathspec  # For type hinting the llmignore_spec
import typer
from rich.console import Console
from rich.tree import Tree as RichTree

# Import the ignore handler utility
from ..utils import ignore_handler  # Assuming utils is in the parent package

console = Console()

# DEFAULT_EXCLUDED_ITEMS: This set can act as a fallback or for items
# not typically in .llmignore but that this tool should generally skip
# if no other rules apply. Its role is reduced now that .llmignore is primary.
# It's checked if ignore_handler.is_path_ignored returns False and no specific
# llmignore file was found. Consider removing or significantly reducing this list
# if .llmignore + CORE_SYSTEM_EXCLUSIONS in ignore_handler is sufficient.
DEFAULT_EXCLUDED_ITEMS_TOOL_SPECIFIC: Set[str] = {
    # Items that might be specific to tree generation context,
    # e.g., the output file name if not handled by other means.
    # For now, let's keep the original list and see how it plays out.
    # Version Control (already in ignore_handler.CORE_SYSTEM_EXCLUSIONS but good for direct name check)
    ".git",
    ".hg",
    ".svn",
    # Python specific
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "venv",
    ".venv",
    "env",
    ".env",
    "pip-wheel-metadata",
    "*.egg-info",
    # Node.js specific
    "node_modules",
    "package-lock.json",
    "yarn.lock",
    # IDE specific
    ".vscode",
    ".idea",
    "*.iml",
    # Build artifacts & Distribution
    "dist",
    "build",
    "target",
    "out",
    # OS specific
    ".DS_Store",
    "Thumbs.db",
    # Logs and temp files (better handled by .llmignore or CLI)
    # "*.log", "*.tmp", "*.swp", # Commenting out, as .llmignore is better for patterns
    # "project_tree.txt", # This should be handled dynamically if it's the output file
}


def _should_skip_this_item_name_fallback(item_name: str, fallback_exclusions: Set[str]) -> bool:
    """
    Fallback check against a simple set of names/basic patterns.
    Used if .llmignore spec doesn't exist or doesn't cover everything.
    """
    if item_name in fallback_exclusions:
        return True
    return any(pattern.startswith("*.") and item_name.endswith(pattern[1:]) for pattern in fallback_exclusions)


def _generate_tree_lines_recursive(
    current_dir: Path,
    root_dir_for_ignores: Path,
    llmignore_spec: Optional[pathspec.PathSpec],
    cli_ignores: Optional[List[str]],
    tool_specific_fallback_exclusions: Set[str],
    parent_prefix: str = "",
    is_root: bool = True,
) -> List[str]:
    """
    Recursively generates plain text directory tree lines for file output.
    Now integrates with the ignore_handler.

    Args:
        current_dir: The directory currently being processed.
        root_dir_for_ignores: The main root directory of the command, base for .llmignore.
        llmignore_spec: Parsed .llmignore specification.
        cli_ignores: List of ignore patterns from CLI arguments.
        tool_specific_fallback_exclusions: Fallback set of names to ignore.
        parent_prefix: Indentation and connectors from the parent.
        is_root: True if this is the initial call for the root directory.

    Returns:
        A list of strings representing the tree lines.
    """
    lines: List[str] = []

    if is_root:
        lines.append(f"{current_dir.name}/")

    try:
        children_to_process: List[Path] = []
        for child_path in current_dir.iterdir():
            # Primary check using the comprehensive ignore_handler
            if not ignore_handler.is_path_ignored(
                path_to_check=child_path,
                root_dir=root_dir_for_ignores,
                ignore_spec=llmignore_spec,
                cli_ignore_patterns=cli_ignores,
            ) and not (llmignore_spec is None and _should_skip_this_item_name_fallback(child_path.name, tool_specific_fallback_exclusions)):
                # Fallback check if no llmignore_spec or if it's a very specific tool need
                children_to_process.append(child_path)

        sorted_children = sorted(children_to_process, key=lambda x: (x.is_file(), x.name.lower()))

    except PermissionError:
        lines.append(f"{parent_prefix}└── [dim italic](Permission Denied for {current_dir.name}/)[/dim italic]")
        return lines
    except FileNotFoundError:
        lines.append(f"{parent_prefix}└── [dim italic](Directory not found: {current_dir.name}/)[/dim italic]")
        return lines

    for i, child in enumerate(sorted_children):
        connector = "└── " if i == len(sorted_children) - 1 else "├── "
        line_prefix_for_child = parent_prefix + connector

        if child.is_dir():
            lines.append(f"{line_prefix_for_child}{child.name}/")
            child_contents_prefix_extension = "    " if connector == "└── " else "│   "
            lines.extend(
                _generate_tree_lines_recursive(
                    current_dir=child,
                    root_dir_for_ignores=root_dir_for_ignores,
                    llmignore_spec=llmignore_spec,
                    cli_ignores=cli_ignores,
                    tool_specific_fallback_exclusions=tool_specific_fallback_exclusions,
                    parent_prefix=parent_prefix + child_contents_prefix_extension,
                    is_root=False,
                )
            )
        else:
            lines.append(f"{line_prefix_for_child}{child.name}")
    return lines


def _add_nodes_to_rich_tree_recursive(
    rich_tree_node: RichTree,
    current_path_obj: Path,
    # --- New parameters for ignore handling ---
    root_dir_for_ignores: Path,
    llmignore_spec: Optional[pathspec.PathSpec],
    cli_ignores: Optional[List[str]],
    tool_specific_fallback_exclusions: Set[str],
):
    """
    Recursively adds nodes to a Rich.Tree object for console display.
    Now integrates with the ignore_handler.
    """
    try:
        children_to_process: List[Path] = []
        for child_path in current_path_obj.iterdir():
            if not ignore_handler.is_path_ignored(
                path_to_check=child_path,
                root_dir=root_dir_for_ignores,
                ignore_spec=llmignore_spec,
                cli_ignore_patterns=cli_ignores,
            ) and not (llmignore_spec is None and _should_skip_this_item_name_fallback(child_path.name, tool_specific_fallback_exclusions)):
                children_to_process.append(child_path)

        sorted_children = sorted(children_to_process, key=lambda x: (x.is_file(), x.name.lower()))

    except PermissionError:
        rich_tree_node.add("[dim italic](Permission Denied)[/dim italic]")
        return
    except FileNotFoundError:
        rich_tree_node.add(f"[dim italic](Directory {current_path_obj.name} not found)[/dim italic]")
        return

    for child in sorted_children:
        if child.is_dir():
            branch = rich_tree_node.add(
                f":file_folder: [link file://{child.resolve()}]{child.name}",
                guide_style="blue",
            )
            _add_nodes_to_rich_tree_recursive(
                rich_tree_node=branch,
                current_path_obj=child,
                root_dir_for_ignores=root_dir_for_ignores,  # Pass through
                llmignore_spec=llmignore_spec,  # Pass through
                cli_ignores=cli_ignores,  # Pass through
                tool_specific_fallback_exclusions=tool_specific_fallback_exclusions,  # Pass through
            )
        else:
            rich_tree_node.add(f":page_facing_up: {child.name}")


def generate_and_output_tree(
    root_dir: Path,
    output_file_path: Optional[Path] = None,
    ignore_list: Optional[List[str]] = None,  # This is from CLI --ignore
):
    """
    Main logic function for generating and outputting the directory tree.
    Integrates .llmignore handling.
    """
    if not root_dir.is_dir():
        console.print(f"[bold red]Error: Root directory '{root_dir}' not found or is not a directory.[/bold red]")
        raise typer.Exit(code=1)

    # Load .llmignore patterns from the specified root_dir
    llmignore_spec = ignore_handler.load_ignore_patterns(root_dir)
    if llmignore_spec:
        console.print(f"[dim]Using .llmignore patterns from '{root_dir / ignore_handler.LLMIGNORE_FILENAME}'[/dim]")

    # Prepare the final set of CLI ignores, including the output file if necessary
    effective_cli_ignores = list(ignore_list) if ignore_list else []
    if output_file_path:
        abs_output_file = output_file_path.resolve()
        if abs_output_file.is_relative_to(root_dir.resolve()) and abs_output_file.name not in effective_cli_ignores:
            # Add output file name to CLI ignores for this run to prevent it from appearing in its own tree
            effective_cli_ignores.append(abs_output_file.name)
            console.print(f"[dim]Output file '{abs_output_file.name}' will be dynamically ignored for this run.[/dim]")

    # Use the tool-specific fallback exclusions
    # These are less critical if .llmignore is comprehensive.
    current_tool_specific_exclusions = DEFAULT_EXCLUDED_ITEMS_TOOL_SPECIFIC.copy()

    if output_file_path:
        tree_lines = _generate_tree_lines_recursive(
            current_dir=root_dir,
            root_dir_for_ignores=root_dir,
            llmignore_spec=llmignore_spec,
            cli_ignores=effective_cli_ignores,
            tool_specific_fallback_exclusions=current_tool_specific_exclusions,
            parent_prefix="",
            is_root=True,
        )
        try:
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            with output_file_path.open(mode="w", encoding="utf-8") as f:
                f.write("\n".join(tree_lines))
            console.print(f"Directory tree saved to [cyan]{output_file_path.resolve()}[/cyan]")
        except OSError as e:
            console.print(f"[bold red]Error writing to output file '{output_file_path}': {e}[/bold red]")
            raise typer.Exit(code=1) from e
    else:
        rich_tree_root_label = f":file_folder: [link file://{root_dir.resolve()}]{root_dir.name}"
        rich_tree_root = RichTree(
            rich_tree_root_label,
            guide_style="bold bright_blue",
        )
        _add_nodes_to_rich_tree_recursive(
            rich_tree_node=rich_tree_root,
            current_path_obj=root_dir,
            root_dir_for_ignores=root_dir,
            llmignore_spec=llmignore_spec,
            cli_ignores=effective_cli_ignores,
            tool_specific_fallback_exclusions=current_tool_specific_exclusions,
        )
        console.print(rich_tree_root)
