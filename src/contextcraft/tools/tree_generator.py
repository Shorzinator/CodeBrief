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

from contextlib import suppress
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

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


def _should_show_path(
    path: Path,
    root_dir_for_ignores: Path,
    llmignore_spec: Optional[pathspec.PathSpec],
    cli_ignores: Optional[List[str]],
    tool_specific_fallback_exclusions: Set[str],
) -> bool:
    """
    Determine if a path should be shown in the tree.
    """
    path_to_check_abs = path.resolve()
    root_dir_abs = root_dir_for_ignores.resolve()
    relative_path_for_spec = None
    with suppress(Exception):
        relative_path_for_spec = path_to_check_abs.relative_to(root_dir_abs)

    if llmignore_spec and relative_path_for_spec is not None:
        path_str = relative_path_for_spec.as_posix()
        if path.is_dir() and not path_str.endswith("/"):
            path_str += "/"
        # pathspec: last matching pattern wins (negation or not)
        is_ignored = llmignore_spec.match_file(path_str)
        return not is_ignored

    # Fallback: use ignore_handler for CLI and fallback exclusions
    is_ignored = ignore_handler.is_path_ignored(path, root_dir_for_ignores, llmignore_spec, cli_ignores)
    if not is_ignored and llmignore_spec is None and _should_skip_this_item_name_fallback(path.name, tool_specific_fallback_exclusions):
        is_ignored = True
    return not is_ignored


def _generate_tree_lines_recursive(
    current_dir: Path,
    root_dir_for_ignores: Path,
    llmignore_spec: Optional[pathspec.PathSpec],
    cli_ignores: Optional[List[str]],
    tool_specific_fallback_exclusions: Set[str],
    parent_prefix: str = "",
    is_root_call_for_display: bool = True,  # Is this the initial dir whose name we print?
) -> List[str]:
    lines: List[str] = []

    if is_root_call_for_display:
        lines.append(f"{current_dir.name}/")

    try:
        all_children_sorted = sorted(current_dir.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        lines.append(f"{parent_prefix}└── [dim italic](Permission Denied for {current_dir.name}/)[/dim italic]")
        return lines
    except FileNotFoundError:
        lines.append(f"{parent_prefix}└── [dim italic](Directory not found: {current_dir.name}/)[/dim italic]")
        return lines

    displayable_children: List[Path] = []
    child_to_displayed_lines: dict = {}
    for child_path in all_children_sorted:
        # Check if the path itself should be shown
        is_displayed = _should_show_path(child_path, root_dir_for_ignores, llmignore_spec, cli_ignores, tool_specific_fallback_exclusions)

        # Always recurse into directories to check for unignored children
        generated_child_lines = []
        if child_path.is_dir():
            generated_child_lines = _generate_tree_lines_recursive(
                current_dir=child_path,
                root_dir_for_ignores=root_dir_for_ignores,
                llmignore_spec=llmignore_spec,
                cli_ignores=cli_ignores,
                tool_specific_fallback_exclusions=tool_specific_fallback_exclusions,
                parent_prefix="",
                is_root_call_for_display=False,
            )

        # A directory should be shown if either:
        # 1. It's not ignored itself, or
        # 2. It has unignored children (even if the dir itself is ignored)
        should_display = is_displayed or (child_path.is_dir() and generated_child_lines)
        child_to_displayed_lines[child_path] = (should_display, generated_child_lines)
        if should_display:
            displayable_children.append(child_path)

    num_displayable = len(displayable_children)
    displayed_count = 0

    for child_path in all_children_sorted:
        is_child_displayed, generated_child_lines = child_to_displayed_lines[child_path]
        if is_child_displayed:
            displayed_count += 1
            connector = "└── " if displayed_count == num_displayable else "├── "
            line_prefix = parent_prefix + connector
            lines.append(f"{line_prefix}{child_path.name}{'/' if child_path.is_dir() else ''}")
            if child_path.is_dir() and generated_child_lines:
                child_prefix = "    " if connector == "└── " else "│   "
                for child_line in generated_child_lines:
                    lines.append(parent_prefix + child_prefix + child_line)

    return lines


def _add_nodes_to_rich_tree_recursive(
    rich_tree_node: RichTree,
    current_path_obj: Path,
    root_dir_for_ignores: Path,
    llmignore_spec: Optional[pathspec.PathSpec],
    cli_ignores: Optional[List[str]],
    tool_specific_fallback_exclusions: Set[str],
):
    """
    Recursively adds nodes to a Rich.Tree object for styled console display.
    Integrates with the ignore_handler and handles negations correctly.
    """
    try:
        all_children_sorted = sorted(current_path_obj.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        rich_tree_node.add("[dim italic](Permission Denied)[/dim italic]")
        return
    except FileNotFoundError:
        rich_tree_node.add(f"[dim italic](Directory {current_path_obj.name} not found)[/dim italic]")
        return

    # First pass: determine which children are displayable and collect results of recursion for dirs
    child_processing_results: Dict[Path, Dict[str, Any]] = {}

    for child_path in all_children_sorted:
        # Check if the path itself should be shown
        is_child_itself_displayable = _should_show_path(
            child_path, root_dir_for_ignores, llmignore_spec, cli_ignores, tool_specific_fallback_exclusions
        )

        # For directories, check if they have any displayable descendants
        has_displayable_descendants = False
        if child_path.is_dir():
            temp_dummy_branch = RichTree("dummy")
            _add_nodes_to_rich_tree_recursive(
                rich_tree_node=temp_dummy_branch,
                current_path_obj=child_path,
                root_dir_for_ignores=root_dir_for_ignores,
                llmignore_spec=llmignore_spec,
                cli_ignores=cli_ignores,
                tool_specific_fallback_exclusions=tool_specific_fallback_exclusions,
            )
            has_displayable_descendants = bool(temp_dummy_branch.children)

        # A directory should be shown if either:
        # 1. It's not ignored itself, or
        # 2. It has unignored children (even if the dir itself is ignored)
        should_display = is_child_itself_displayable or (child_path.is_dir() and has_displayable_descendants)
        child_processing_results[child_path] = {"is_displayable": should_display, "has_descendants": has_displayable_descendants}

    # Second pass: Add nodes to the tree
    displayable_children = [p for p in all_children_sorted if child_processing_results[p]["is_displayable"]]
    for i, child_path in enumerate(displayable_children):
        is_last = i == len(displayable_children) - 1
        if child_path.is_dir():
            # Use consistent tree characters
            branch_label = f"{'└── ' if is_last else '├── '}📁 {child_path.name}"
            branch = rich_tree_node.add(branch_label, guide_style="blue")
            _add_nodes_to_rich_tree_recursive(
                rich_tree_node=branch,
                current_path_obj=child_path,
                root_dir_for_ignores=root_dir_for_ignores,
                llmignore_spec=llmignore_spec,
                cli_ignores=cli_ignores,
                tool_specific_fallback_exclusions=tool_specific_fallback_exclusions,
            )
        else:
            file_label = f"{'└── ' if is_last else '├── '}📄 {child_path.name}"
            rich_tree_node.add(file_label)


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
            is_root_call_for_display=True,
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
