# src/contextcraft/tools/flattener.py
"""
Code Flattening Utilities.

This module provides functions to "flatten" a directory structure by concatenating
the content of specified files into a single text output. It's designed to help
create a comprehensive context of a project's codebase, primarily for consumption
by Large Language Models (LLMs) or for project archival and review.

Core functionalities:
- Recursive traversal of directories using `os.walk`.
- Filtering of files based on include patterns (e.g., file extensions, glob patterns)
  and exclude patterns/names.
- A default list of common code/text file extensions to include if no specific
  include patterns are provided by the user.
- A default list of common development artifacts and directories (e.g., .git,
  node_modules, __pycache__) to exclude from traversal and processing.
- Prepending each file's content with a standardized marker comment indicating its
  original relative path.
- Graceful handling of binary files or files with problematic encodings by skipping
  them and issuing a warning, rather than crashing the process.
- Outputting the combined content to the console or a specified file, ensuring
  UTF-8 encoding for the output.
"""
import os # Used for os.walk to traverse directory structures.
from pathlib import Path # Core library for object-oriented path manipulation.
from typing import List, Optional, Set # Type hints for clarity and static analysis.

import typer # For typer.Exit for controlled exits from logic functions.
from rich.console import Console # For styled and rich console output.

# Initialize a Rich Console instance for any direct console output from this module.
# This allows for consistent styling of messages (e.g., errors, warnings, success).
console = Console()

# A set of default directory and file names/patterns to generally exclude from
# directory traversal (used with os.walk) and from individual file processing.
# This list aims to cover common development artifacts, version control systems,
# virtual environments, and OS-specific metadata files.
# This will be augmented by .llmignore patterns in the future.
DEFAULT_EXCLUDED_ITEMS_GENERAL: Set[str] = {
    # Version Control
    ".git", ".hg", ".svn",
    # Python specific
    "__pycache__", "*.pyc", "*.pyo", "*.pyd",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "venv", ".venv", "env", ".env",
    "pip-wheel-metadata", "*.egg-info",
    # Node.js specific
    "node_modules", "package-lock.json", "yarn.lock",
    # IDE specific
    ".vscode", ".idea", "*.iml",
    # Build artifacts & Distribution
    "dist", "build", "target", "out",
    # OS specific
    ".DS_Store", "Thumbs.db",
    # Logs and temp files (can also be handled by more specific exclude patterns by user)
    "*.log", "*.tmp", "*.swp",
}

# Default file extensions to include if no specific include patterns are given by the user.
# This list prioritizes common source code, markup, configuration, and text files.
# The patterns are typically suffixes (e.g., ".py") but can be full filenames too.
DEFAULT_INCLUDE_EXTENSIONS: List[str] = [
    # Python
    ".py", ".pyw", ".pyx", ".pyd", ".pxd",
    # JavaScript / TypeScript
    ".js", ".jsx", ".mjs", ".cjs",
    ".ts", ".tsx", ".mts", ".cts",
    # Web
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".styl",
    # Java / JVM
    ".java", ".kt", ".kts", ".scala", ".groovy", ".gradle",
    # C / C++ / Objective-C
    ".c", ".cpp", ".h", ".hpp", ".m", ".mm",
    # C# / .NET
    ".cs", ".vb",
    # Go
    ".go",
    # Rust
    ".rs",
    # Ruby
    ".rb",
    # PHP
    ".php", ".phtml",
    # Swift
    ".swift",
    # Shell / Scripting
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
    # Markup / Data Interchange / Config
    ".md", ".markdown", ".rst",
    ".txt", ".text",
    ".json", ".jsonc", ".json5",
    ".yaml", ".yml",
    ".xml", ".toml", ".ini", ".cfg", ".conf",
    ".csv", ".tsv",
    # Docker / Containerization
    "Dockerfile", ".dockerfile", "docker-compose.yml", "docker-compose.yaml",
    # SQL
    ".sql",
    # Other common text-based files
    ".env.example", ".gitattributes", ".gitmodules", ".editorconfig",
    # Readmes, licenses, contributing guides
    "README", "LICENSE", "CONTRIBUTING", "NOTICE", "CHANGELOG",
]


def should_include_file(
    file_path: Path,
    include_patterns: Optional[List[str]],
    exclude_patterns: Optional[List[str]],
    default_general_exclusions: Set[str],
) -> bool:
    """
    Determines if a file should be included in the flattening process
    based on include, exclude, and general exclusion criteria.

    The logic is as follows:
    1. If the file's name or its immediate parent directory's name matches any
       entry in `default_general_exclusions`, it's excluded. (This is a basic check;
       `os.walk` handles directory traversal exclusion more robustly).
    2. If `exclude_patterns` are provided, and the file matches any of these
       (either by direct name or glob pattern), it's excluded.
    3. If `include_patterns` are provided by the user, the file *must* match one of them
       (by extension, glob, or exact name).
    4. If no `include_patterns` are user-provided, `DEFAULT_INCLUDE_EXTENSIONS` are used,
       and the file *must* match one of these (typically by extension or exact name).
    5. If a file passes all exclusion checks and matches the relevant include criteria,
       it is included.

    Args:
        file_path: The `pathlib.Path` object for the file being considered.
        include_patterns: A list of user-provided glob patterns or extensions
                          (e.g., "*.py", ".js"). If None or empty,
                          `DEFAULT_INCLUDE_EXTENSIONS` is used.
        exclude_patterns: A list of user-provided glob patterns or names to explicitly exclude.
        default_general_exclusions: A set of general item names (files/dirs) to always
                                    exclude as a baseline.

    Returns:
        True if the file should be included for flattening, False otherwise.
    """
    file_name = file_path.name
    file_suffix_lower = file_path.suffix.lower()

    # 1. Check against general default exclusions for the file itself or its parent directory.
    # This is a secondary check; os.walk handles broader directory exclusions.
    if file_name in default_general_exclusions or file_path.parent.name in default_general_exclusions:
        # console.print(f"[dim]Skipping '{file_path}' due to general exclusion rule.[/dim]")
        return False

    # 2. Check against explicit user-defined exclude patterns.
    # These take precedence.
    if exclude_patterns:
        for pattern in exclude_patterns:
            if pattern.startswith("*.") and file_suffix_lower == pattern[1:].lower(): # Simple suffix glob like *.log
                return False
            elif file_path.match(pattern) or file_name == pattern: # Path.match for globs, or exact name
                # console.print(f"[dim]Excluding '{file_path}' due to exclude pattern: '{pattern}'[/dim]")
                return False

    # 3. Determine effective include patterns.
    # If user specified --include, use those. Otherwise, use defaults.
    active_include_patterns = include_patterns if include_patterns else DEFAULT_INCLUDE_EXTENSIONS

    # 4. Check against include patterns.
    # The file must match at least one include pattern if any are active.
    if active_include_patterns:
        matched_an_include_pattern = False
        for pattern in active_include_patterns:
            if pattern.startswith("."):  # Primarily for matching extensions like ".py"
                if file_suffix_lower == pattern.lower():
                    matched_an_include_pattern = True
                    break
            elif pattern.startswith("*."): # For matching glob extensions like "*.txt"
                if file_suffix_lower == pattern[1:].lower():
                    matched_an_include_pattern = True
                    break
            elif file_path.match(pattern):  # For more complex glob patterns like "src/**/*.py"
                matched_an_include_pattern = True
                break
            elif file_name == pattern:  # For exact filename matches like "Makefile"
                matched_an_include_pattern = True
                break
        
        if not matched_an_include_pattern:
            # console.print(f"[dim]Skipping '{file_path}' as it doesn't match include patterns.[/dim]")
            return False # File did not match any of the required include patterns.

    # If all checks passed, the file should be included.
    return True


def flatten_code_logic(
    root_dir_path: Path,
    output_file_path: Optional[Path] = None,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> None:
    """
    Main logic function for flattening files within a directory into a single text output.

    It traverses the `root_dir_path`, filters files based on include/exclude criteria,
    reads their content, prepends a path header, and concatenates everything.
    The result is either printed to the console or saved to `output_file_path`.

    Args:
        root_dir_path: The `pathlib.Path` object for the root directory from which to start flattening.
        output_file_path: Optional `pathlib.Path` to save the flattened content.
                          If None, the content is printed to the console.
        include_patterns: Optional list of user-specified include patterns (extensions, globs, filenames).
                          If None or empty, `DEFAULT_INCLUDE_EXTENSIONS` are used by `should_include_file`.
        exclude_patterns: Optional list of user-specified exclude patterns (names, globs).
                          These are evaluated by `should_include_file`.

    Raises:
        typer.Exit: If critical errors occur, such as the root directory not being valid
                    or issues writing to the output file.
    """
    # Validate that the root directory exists and is indeed a directory.
    if not root_dir_path.is_dir():
        console.print(f"[bold red]Error: Root directory '{root_dir_path}' not found or is not a directory.[/bold red]")
        raise typer.Exit(code=1)

    # Prepare the set of general exclusions for os.walk's directory pruning.
    # This prevents traversal into directories like .git, node_modules, etc.
    current_general_exclusions_for_walk = DEFAULT_EXCLUDED_ITEMS_GENERAL.copy()

    # If an output file is specified and it's within the root directory,
    # ensure its name is added to the general exclusions to prevent it from being read.
    # Note: `should_include_file` might also catch this, but `os.walk` pruning is more efficient.
    if output_file_path:
        abs_output_file = output_file_path.resolve()
        abs_root_dir = root_dir_path.resolve()
        if abs_output_file.is_relative_to(abs_root_dir):
            # Add the output file's name to prevent it from being processed if it's directly in a walked dir.
            current_general_exclusions_for_walk.add(abs_output_file.name)
            # If the output file is, e.g. `out/bundle.txt`, add `out` to dir exclusions for os.walk
            # This ensures os.walk doesn't even enter the 'out' directory if output is there.
            try:
                output_parent_relative_to_root = abs_output_file.parent.relative_to(abs_root_dir)
                if output_parent_relative_to_root.parts: # Check if parent is not root itself
                    first_part_of_output_path = output_parent_relative_to_root.parts[0]
                    current_general_exclusions_for_walk.add(first_part_of_output_path)
            except ValueError: # output_file_path.parent is not under root_dir_path
                pass


    flattened_content_parts: List[str] = [] # Stores parts of the final output string
    files_processed_count = 0
    files_skipped_binary_count = 0

    console.print(f"[dim]Starting flattening process in '{root_dir_path.resolve()}'...[/dim]")

    # Traverse the directory tree using os.walk.
    # topdown=True allows modification of `dirs` list to prune search.
    for current_subdir_str, dirs, files in os.walk(root_dir_path, topdown=True):
        # Prune directories from traversal if their names are in general exclusions.
        dirs[:] = [d_name for d_name in dirs if d_name not in current_general_exclusions_for_walk]

        current_subdir_path = Path(current_subdir_str)

        # Process each file in the current directory.
        for file_name in sorted(files): # Sort files for deterministic output order
            file_path = current_subdir_path / file_name

            # Determine if the file should be included based on combined criteria.
            if not should_include_file(
                file_path, include_patterns, exclude_patterns, DEFAULT_EXCLUDED_ITEMS_GENERAL
            ):
                continue # Skip this file if it doesn't meet criteria.

            # Calculate the relative path for the file header.
            try:
                relative_path_str = str(file_path.relative_to(root_dir_path))
            except ValueError: # Should not happen if os.walk starts from root_dir_path
                relative_path_str = str(file_path)


            # Add a standardized header comment for the file.
            flattened_content_parts.append(f"\n\n# --- File: {relative_path_str} ---")
            try:
                # Attempt to read the file as UTF-8, ignoring undecodable characters.
                # This is a balance between getting content and avoiding crashes on
                # files with minor encoding issues or embedded binary data.
                with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                    content = infile.read()
                    flattened_content_parts.append(content)
                files_processed_count += 1
            except UnicodeDecodeError: # This catch is a fallback. errors='ignore' should handle most.
                warning_msg = f"Skipping binary or non-UTF-8 file: {file_path}"
                console.print(f"[yellow]Warning: {warning_msg}[/yellow]")
                flattened_content_parts.append(f"# --- {warning_msg} ---")
                files_skipped_binary_count +=1
            except Exception as e: # Catch other potential IOErrors.
                error_msg = f"Error reading file {file_path}: {e}"
                console.print(f"[red]{error_msg}[/red]")
                flattened_content_parts.append(f"# --- {error_msg} ---")
                # Optionally, increment a 'files_errored_count' here.

    # Join all collected parts into the final output string.
    # Use strip to remove leading/trailing newlines that might result from the initial "\n\n".
    final_output_str = "\n".join(flattened_content_parts).strip()

    # Output the result to a file or console.
    if output_file_path:
        try:
            output_file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure parent dir exists
            with open(output_file_path, "w", encoding="utf-8") as outfile:
                outfile.write(final_output_str)
            console.print(
                f"[green]Successfully flattened {files_processed_count} file(s) "
                f"to '{output_file_path.resolve()}'[/green]"
            )
            if files_skipped_binary_count > 0:
                console.print(f"[yellow]Skipped {files_skipped_binary_count} binary/non-UTF-8 file(s).[/yellow]")
        except IOError as e:
            console.print(f"[bold red]Error writing to output file '{output_file_path}': {e}[/bold red]")
            raise typer.Exit(code=1)
    else:
        # Print to console. For very large outputs, Rich's print handles it well.
        # If syntax highlighting were desired for a specific language, Rich's Syntax could be used here,
        # but the combined output is multi-language, so plain print is appropriate.
        console.print(final_output_str)
        console.print(
            f"[blue]\n--- Flattened {files_processed_count} file(s). "
            f"Skipped {files_skipped_binary_count} binary/non-UTF-8 file(s). ---[/blue]"
        )