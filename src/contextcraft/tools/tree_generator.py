# src/contextcraft/tools/tree_generator.py
"""
Directory Tree Generation Utilities.

This module provides functions to generate a textual or Rich-enhanced representation
of a directory's structure. It supports excluding specified files and directories
and can output the tree to the console or a file.

Core functionalities:
- Recursive traversal of directories.
- Filtering of items based on a predefined exclusion list and user-provided ignores.
- Generation of plain text tree for file output.
- Generation of a Rich `Tree` object for styled console output.
"""

import os # Used by os.walk in some implementations, though pathlib is preferred here.
from pathlib import Path # Core library for object-oriented path manipulation.
from typing import Set, List, Optional # Type hints for clarity and static analysis.

import typer # Used for typer.Exit for controlled exits.
from rich.console import Console # For styled console output.
from rich.tree import Tree as RichTree # Rich's specific Tree widget for console display.

# Initialize a Rich Console instance for any direct console output from this module.
console = Console()

# A set of default directory and file names/patterns to exclude from the tree.
# This list aims to cover common development artifacts, version control systems,
# virtual environments, and OS-specific metadata files.
# This will be augmented by .llmignore patterns in the future.
DEFAULT_EXCLUDED_ITEMS: Set[str] = {
    # Version Control
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
    "package-lock.json", # Often very large, may not be needed for tree
    "yarn.lock",        # Same as above
    # IDE specific
    ".vscode",
    ".idea",
    "*.iml",
    # Build artifacts & Distribution
    "dist",
    "build",
    "target", # Common in Java/Rust
    "out",
    # OS specific
    ".DS_Store", # macOS
    "Thumbs.db", # Windows
    # Logs and temp files
    "*.log",
    "*.tmp",
    "*.swp", # Vim swap files
    "project_tree.txt"
}


def _generate_tree_lines_recursive(
    current_dir: Path,
    parent_prefix: str = "",
    excluded_items: Optional[Set[str]] = None,
    is_root: bool = True,
) -> List[str]:
    """
    Recursively generates plain text directory tree lines for file output.

    This function walks the directory structure from `current_dir` and creates
    a list of strings, each representing a line in the traditional 'tree' command output.
    It uses simple prefix characters (│, ├──, └──) to denote structure.

    Args:
        current_dir: The pathlib.Path object for the directory currently being processed.
        parent_prefix: The string prefix (indentation and connectors) inherited from the parent level.
        excluded_items: A set of item names (files/directories) to exclude.
                         If None, `DEFAULT_EXCLUDED_ITEMS` is used.
        is_root: Boolean flag indicating if the current_dir is the root of the tree traversal.
                 This is used to correctly print the root directory's name.

    Returns:
        A list of strings, where each string is a line of the generated tree.

    Raises:
        Does not explicitly raise exceptions but relies on `Path.iterdir()` which can
        raise `PermissionError` or `FileNotFoundError` if issues occur during iteration.
        These are expected to be caught by the caller.
    """
    # Ensure excluded_items is initialized if not provided
    if excluded_items is None:
        # Use a copy to avoid modifying the global default set if this function
        # were to alter it (though it currently doesn't).
        excluded_items = DEFAULT_EXCLUDED_ITEMS.copy()

    lines: List[str] = []

    # Add the current directory's name as the first line if it's the root of this sub-tree call.
    if is_root:
        lines.append(f"{current_dir.name}/")

    try:
        # Retrieve children, filter out excluded items, and sort them.
        # Sorting key: directories first, then files, then alphabetically (case-insensitive).
        children = sorted(
            [
                child
                for child in current_dir.iterdir() # Iterate over items in the current directory
                if child.name not in excluded_items # Apply exclusion filter
            ],
            key=lambda x: (x.is_file(), x.name.lower()),
        )
    except PermissionError:
        # If access to the directory is denied, add a note and return.
        # The formatting [dim italic] is Rich console markup, which will be plain text in the file.
        lines.append(f"{parent_prefix}└── [dim italic](Permission Denied for {current_dir.name}/)[/dim italic]")
        return lines
    except FileNotFoundError:
        # If the directory itself is not found (e.g., deleted during traversal), note it.
        lines.append(f"{parent_prefix}└── [dim italic](Directory not found: {current_dir.name}/)[/dim italic]")
        return lines

    # Iterate over the sorted and filtered children to build the tree lines.
    for i, child in enumerate(children):
        # Determine the connector prefix based on whether this is the last item in the list.
        connector = "└── " if i == len(children) - 1 else "├── "
        line_prefix_for_child = parent_prefix + connector # Prefix for the child's line

        if child.is_dir():
            lines.append(f"{line_prefix_for_child}{child.name}/") # Append directory name with a slash
            # Prepare the prefix for items *inside* this child directory.
            # If current child is the last one (└──), its children don't need the vertical bar │.
            # Otherwise (├──), its children do need the vertical bar.
            child_contents_prefix_extension = "    " if connector == "└── " else "│   "
            # Recursively call for the subdirectory.
            lines.extend(
                _generate_tree_lines_recursive(
                    child, # The subdirectory to process
                    parent_prefix + child_contents_prefix_extension, # New prefix for its children
                    excluded_items, # Pass along the exclusion set
                    is_root=False,  # Subsequent calls are not for the overall root
                )
            )
        else:
            # If it's a file, just append its name with the current prefix.
            lines.append(f"{line_prefix_for_child}{child.name}")
    return lines


def _add_nodes_to_rich_tree_recursive(
    rich_tree_node: RichTree,
    current_path_obj: Path,
    excluded_items: Optional[Set[str]] = None
):
    """
    Recursively adds nodes to a Rich.Tree object for styled console display.

    This function populates a given Rich `Tree` node with children from the
    `current_path_obj`. It uses emojis and styling for a more visually appealing
    console output.

    Args:
        rich_tree_node: The parent Rich.Tree node to which children will be added.
        current_path_obj: The pathlib.Path object for the directory whose contents are being added.
        excluded_items: A set of item names to exclude. If None, `DEFAULT_EXCLUDED_ITEMS` is used.

    Raises:
        Relies on `Path.iterdir()` which can raise `PermissionError` or `FileNotFoundError`.
        These are handled by adding a note to the RichTree.
    """
    if excluded_items is None:
        excluded_items = DEFAULT_EXCLUDED_ITEMS.copy()

    try:
        # Retrieve children, filter, and sort as in the text-based generator.
        children = sorted(
            [
                child
                for child in current_path_obj.iterdir()
                if child.name not in excluded_items
            ],
            key=lambda x: (x.is_file(), x.name.lower()),
        )
    except PermissionError:
        rich_tree_node.add("[dim italic](Permission Denied)[/dim italic]")
        return
    except FileNotFoundError: # Should be less likely if root_dir check passed
        rich_tree_node.add(f"[dim italic](Directory {current_path_obj.name} not found)[/dim italic]")
        return

    # Add each child to the RichTree.
    for child in children:
        if child.is_dir():
            # Create a new branch (sub-tree) for directories.
            # Use a folder emoji and make the name a clickable link (in supporting terminals).
            branch = rich_tree_node.add(
                f":file_folder: [link file://{child.resolve()}]{child.name}",
                guide_style="blue", # Style for the guide lines of this branch
            )
            # Recursively populate this new branch.
            _add_nodes_to_rich_tree_recursive(branch, child, excluded_items)
        else:
            # Add files as leaf nodes with a page emoji.
            rich_tree_node.add(f":page_facing_up: {child.name}")


def generate_and_output_tree(
    root_dir: Path,
    output_file_path: Optional[Path] = None,
    ignore_list: Optional[List[str]] = None,
):
    """
    Main logic function for generating and outputting the directory tree.

    This function is typically called by a Typer command. It orchestrates
    the tree generation process, deciding whether to output to a file (plain text)
    or to the console (using Rich Tree). It also handles the initial setup of
    excluded items, including the special case of not listing the output file itself.

    Args:
        root_dir: The root directory (as a pathlib.Path object) from which to generate the tree.
        output_file_path: Optional path to a file where the tree should be saved.
                          If None, the tree is printed to the console.
        ignore_list: An optional list of additional item names (strings) to exclude.
                     These are combined with `DEFAULT_EXCLUDED_ITEMS`.

    Raises:
        typer.Exit: If critical errors occur, such as inability to write to the output file
                    or if the root directory is invalid (though Typer often catches this first).
    """
    # Initial validation of root_dir (Typer usually handles this with `exists=True`, etc.,
    # but this provides a fallback or can be used if called directly).
    if not root_dir.is_dir():
        console.print(f"[bold red]Error: Root directory '{root_dir}' not found or is not a directory.[/bold red]")
        raise typer.Exit(code=1)

    # Prepare the set of all items to be excluded.
    current_excluded_set = DEFAULT_EXCLUDED_ITEMS.copy()
    if ignore_list:
        current_excluded_set.update(ignore_list)
        # Future enhancement: This is where .llmignore patterns would be processed and added.

    # If outputting to a file, and that file is within the traversed directory,
    # ensure the output file itself is not listed in the tree.
    if output_file_path:
        # Resolve paths to absolute to ensure correct comparison with `is_relative_to`.
        abs_output_file = output_file_path.resolve()
        abs_root_dir = root_dir.resolve()
        # Check if the output file is inside the root directory (or its subdirectories)
        # and if its name isn't already in the exclusion set.
        if abs_output_file.is_relative_to(abs_root_dir) and \
           abs_output_file.name not in current_excluded_set:
            # console.print(f"[dim]Note: Excluding output file '{abs_output_file.name}' from tree view.[/dim]")
            current_excluded_set.add(abs_output_file.name)

    # --- Output Generation ---
    if output_file_path:
        # Generate plain text lines for file output using the recursive helper.
        tree_lines = _generate_tree_lines_recursive(
            root_dir,
            excluded_items=current_excluded_set,
            is_root=True # Initial call is for the root
        )
        try:
            # Write the generated lines to the specified output file.
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(tree_lines))
            console.print(f"Directory tree saved to [cyan]{output_file_path.resolve()}[/cyan]")
        except IOError as e:
            # Handle potential errors during file writing.
            console.print(f"[bold red]Error writing to output file '{output_file_path}': {e}[/bold red]")
            raise typer.Exit(code=1)
    else:
        # Generate and print a RichTree for console output.
        # Define the label for the root node of the RichTree.
        rich_tree_root_label = f":file_folder: [link file://{root_dir.resolve()}]{root_dir.name}"
        # Create the main RichTree object.
        rich_tree_root = RichTree(
            rich_tree_root_label,
            guide_style="bold bright_blue", # Style for the connecting guide lines
        )
        # Recursively populate the RichTree starting from the root directory.
        _add_nodes_to_rich_tree_recursive(rich_tree_root, root_dir, current_excluded_set)
        # Print the fully constructed RichTree to the console.
        console.print(rich_tree_root)