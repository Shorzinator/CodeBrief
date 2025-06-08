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

import os  # Used for os.walk to traverse directory structures.
from pathlib import Path  # Core library for object-oriented path manipulation.
from typing import List, Optional, Set  # Type hints for clarity and static analysis.

import typer  # For typer.Exit for controlled exits from logic functions.
from rich.console import Console  # For styled and rich console output.

from ..utils import ignore_handler

# Initialize a Rich Console instance for any direct console output from this module.
# This allows for consistent styling of messages (e.g., errors, warnings, success).
console = Console()

# A set of default directory and file names/patterns to generally exclude from
# directory traversal (used with os.walk) and from individual file processing.
# This list aims to cover common development artifacts, version control systems,
# virtual environments, and OS-specific metadata files.
# This will be augmented by .llmignore patterns in the future.
DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK: Set[str] = {
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
    # Logs and temp files (can also be handled by more specific exclude patterns by user)
    "*.log",
    "*.tmp",
    "*.swp",
}

# Default file extensions to include if no specific include patterns are given by the user.
# This list prioritizes common source code, markup, configuration, and text files.
# The patterns are typically suffixes (e.g., ".py") but can be full filenames too.
DEFAULT_INCLUDE_PATTERNS: List[str] = [
    # Python
    ".py",
    ".pyw",
    ".pyx",
    ".pyd",
    ".pxd",
    # JavaScript / TypeScript
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    # Web
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".styl",
    # Java / JVM
    ".java",
    ".kt",
    ".kts",
    ".scala",
    ".groovy",
    ".gradle",
    # C / C++ / Objective-C
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".m",
    ".mm",
    # C# / .NET
    ".cs",
    ".vb",
    # Go
    ".go",
    # Rust
    ".rs",
    # Ruby
    ".rb",
    # PHP
    ".php",
    ".phtml",
    # Swift
    ".swift",
    # Shell / Scripting
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".bat",
    ".cmd",
    # Markup / Data Interchange / Config
    ".md",
    ".markdown",
    ".rst",
    ".txt",
    ".text",
    ".json",
    ".jsonc",
    ".json5",
    ".yaml",
    ".yml",
    ".xml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".csv",
    ".tsv",
    # Docker / Containerization
    "Dockerfile",
    ".dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    # SQL
    ".sql",
    # Other common text-based files
    ".env.example",
    ".gitattributes",
    ".gitmodules",
    ".editorconfig",
    # Readmes, licenses, contributing guides
    "README",
    "LICENSE",
    "CONTRIBUTING",
    "NOTICE",
    "CHANGELOG",
]


def _file_matches_include_criteria(
    file_path: Path,
    cli_include_patterns: Optional[List[str]],
) -> bool:
    """
    Determines if a file should be included based *only* on --include CLI patterns
    or `DEFAULT_INCLUDE_PATTERNS` if no CLI patterns are given.
    This function assumes all exclusion/ignore checks have already been performed.

    Args:
        file_path: The `pathlib.Path` object for the file being considered.
        cli_include_patterns: A list of user-provided glob patterns, extensions, or filenames
                              from the --include CLI option.

    Returns:
        True if the file matches the inclusion criteria, False otherwise.
    """
    file_name = file_path.name
    file_suffix_lower = file_path.suffix.lower()

    active_patterns = cli_include_patterns if cli_include_patterns else DEFAULT_INCLUDE_PATTERNS

    if not active_patterns:  # Should ideally not happen if DEFAULT_INCLUDE_PATTERNS is populated
        return True  # Default to include if no include rules are active at all

    for pattern in active_patterns:
        if pattern.startswith("."):  # Match by extension (e.g., ".py")
            if file_suffix_lower == pattern.lower():
                return True
        elif pattern.startswith("*."):  # Match by glob extension (e.g., "*.txt")
            if file_suffix_lower == pattern[1:].lower():
                return True
        # For non-extension patterns, treat as exact filename or simple filename glob
        elif Path(file_name).match(pattern):  # Handles exact name and simple globs like "file*.txt", "Makefile"
            return True
        # Note: Complex path-based include globs (e.g., "src/**/*.py") are not explicitly handled
        # by this helper. If needed, the main loop would have to pass relative_path_to_root
        # and this helper would need another argument, or Path.match would be used on an
        # absolute file_path carefully if patterns are also absolute or resolvable.
        # For now, include patterns are mostly for extensions and filenames/filename_globs.

    return False


def _directory_has_unignored_files(
    dir_path: Path,
    root_dir: Path,
    llmignore_spec,
    cli_ignores,
) -> bool:
    """
    Recursively checks if a directory contains any files that are NOT ignored by the ignore logic.
    Returns True if at least one un-ignored file is found.
    """
    for current_root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = Path(current_root) / file
            if not ignore_handler.is_path_ignored(file_path, root_dir, llmignore_spec, cli_ignores):
                return True
    return False


def flatten_code_logic(
    root_dir_path: Path,
    output_file_path: Optional[Path] = None,
    include_patterns: Optional[List[str]] = None,  # CLI --include
    exclude_patterns: Optional[List[str]] = None,  # CLI --exclude (acts as additional ignores)
) -> None:
    """
    Main logic function for flattening files within a directory into a single text output.
    Integrates .llmignore handling and fallback default exclusions.

    Args:
        root_dir_path: The root directory from which to start flattening.
        output_file_path: Optional path to save the flattened content. If None, prints to console.
        include_patterns: List of patterns from CLI --include.
        exclude_patterns: List of patterns from CLI --exclude, treated as additional ignore patterns.
    """
    if not root_dir_path.is_dir():
        console.print(f"[bold red]Error: Root directory '{root_dir_path}' not found or is not a directory.[/bold red]")
        raise typer.Exit(code=1)

    llmignore_spec = ignore_handler.load_ignore_patterns(root_dir_path)
    if llmignore_spec and output_file_path:  # Only print if outputting to file, to reduce console noise
        # (Consider making console messages like this conditional on a verbosity flag later)
        llmignore_file_path = root_dir_path / ignore_handler.LLMIGNORE_FILENAME
        if llmignore_file_path.exists():  # Check if it actually exists, load_ignore_patterns can return None if empty
            console.print(f"[dim]Using .llmignore patterns from '{llmignore_file_path}'[/dim]")
        elif output_file_path:  # Only print this if not using llmignore and outputting to file
            console.print(f"[dim]No .llmignore file found or it's empty in '{root_dir_path}'. Using default general exclusions.[/dim]")
    elif not llmignore_spec and output_file_path:  # No llmignore, outputting to file
        console.print(f"[dim]No .llmignore file found or it's empty in '{root_dir_path}'. Using default general exclusions.[/dim]")

    effective_cli_ignores = list(exclude_patterns) if exclude_patterns else []
    if output_file_path:
        abs_output_file = output_file_path.resolve()
        abs_root_dir = root_dir_path.resolve()
        if abs_output_file.is_relative_to(abs_root_dir) and abs_output_file.name not in effective_cli_ignores:
            effective_cli_ignores.append(abs_output_file.name)

    flattened_content_parts: List[str] = []
    files_processed_count = 0
    files_skipped_binary_count = 0

    if output_file_path:  # Only print if outputting to file
        console.print(f"[dim]Starting flattening process in '{root_dir_path.resolve()}'...[/dim]")

    # We need to keep 'dirs' in the loop because we modify it in-place to control os.walk's traversal.
    # The modification happens in the directory pruning logic below.
    # - dirs is modified in-place to control os.walk traversal
    for current_subdir_str, dirs, files in os.walk(root_dir_path, topdown=True):
        current_subdir_path = Path(current_subdir_str)

        # Directory pruning logic
        dirs_to_prune_indices = []
        for i, dir_name in enumerate(dirs):
            dir_path_abs = current_subdir_path / dir_name

            # Primary prune via ignore_handler (checks CORE, .llmignore, CLI excludes)
            if ignore_handler.is_path_ignored(
                path_to_check=dir_path_abs,
                root_dir=root_dir_path,
                ignore_spec=llmignore_spec,
                cli_ignore_patterns=effective_cli_ignores,
            ):
                # Only prune if the directory and all its descendants are ignored
                if not _directory_has_unignored_files(dir_path_abs, root_dir_path, llmignore_spec, effective_cli_ignores):
                    dirs_to_prune_indices.append(i)
                continue  # Move to next directory in list `dirs`

            # Fallback: if no .llmignore, apply general default name-based exclusions for walk
            if not llmignore_spec:
                should_prune_by_fallback_dir = False
                for fallback_pattern in DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK:
                    # Check if dir_name itself or a pattern matches it from fallback
                    if dir_name == fallback_pattern or Path(dir_name).match(fallback_pattern):
                        should_prune_by_fallback_dir = True
                        break
                if should_prune_by_fallback_dir:
                    dirs_to_prune_indices.append(i)

        # Prune directories by iterating from the end to keep indices valid
        for i in sorted(dirs_to_prune_indices, reverse=True):
            del dirs[i]

        for file_name in sorted(files):
            file_path = current_subdir_path / file_name

            # 1. Check if the file is ignored by .llmignore, CLI excludes, or core system rules
            if ignore_handler.is_path_ignored(
                path_to_check=file_path,
                root_dir=root_dir_path,
                ignore_spec=llmignore_spec,
                cli_ignore_patterns=effective_cli_ignores,
            ):
                continue

            # 2. Fallback exclusion for files if no .llmignore was active
            if not llmignore_spec:
                should_skip_by_fallback_file = False
                for fallback_pattern in DEFAULT_EXCLUDED_ITEMS_GENERAL_FOR_WALK_FALLBACK:
                    if file_name == fallback_pattern or Path(file_name).match(fallback_pattern):
                        should_skip_by_fallback_file = True
                        break
                if should_skip_by_fallback_file:
                    continue

            # 3. If not ignored by any exclusion rule, check if it meets include criteria
            if not _file_matches_include_criteria(file_path, include_patterns):
                continue

            # --- File Processing Logic (binary check, read, append) ---
            try:
                relative_path_str = str(file_path.relative_to(root_dir_path).as_posix())
            except ValueError:
                relative_path_str = str(file_path.as_posix())

            try:
                with file_path.open(mode="rb") as binfile:
                    start_bytes = binfile.read(1024)
                if b"\x00" in start_bytes:
                    warning_msg = f"Skipped binary or non-UTF-8 file: {relative_path_str}"
                    # Only print console warning if outputting to file, to avoid cluttering console output mode
                    if output_file_path:
                        console.print(f"[yellow]Warning: Skipping binary or non-UTF-8 file: {file_path.as_posix()}[/yellow]")
                    flattened_content_parts.append(f"\n\n# --- {warning_msg} ---")
                    files_skipped_binary_count += 1
                    continue

                with file_path.open(mode="r", encoding="utf-8", errors="ignore") as infile:
                    content = infile.read()
                flattened_content_parts.append(f"\n\n# --- File: {relative_path_str} ---")
                flattened_content_parts.append(content)
                files_processed_count += 1
            except Exception as e:
                error_msg = f"Error reading file {file_path.as_posix()}: {e}"
                if output_file_path:  # Only print console error if outputting to file
                    console.print(f"[red]{error_msg}[/red]")
                flattened_content_parts.append(f"# --- {error_msg} ---")  # Always record error in output

    final_output_str = "\n".join(flattened_content_parts).strip()

    if output_file_path:
        try:
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            with output_file_path.open(mode="w", encoding="utf-8") as outfile:
                outfile.write(final_output_str)
            console.print(f"[green]Successfully flattened {files_processed_count} file(s) " f"to '{output_file_path.resolve()}'[/green]")
            if files_skipped_binary_count > 0:
                console.print(f"[yellow]Skipped {files_skipped_binary_count} binary/non-UTF-8 file(s).[/yellow]")
        except OSError as e:
            console.print(f"[bold red]Error writing to output file '{output_file_path}': {e}[/bold red]")
            raise typer.Exit(code=1) from e
    else:  # Printing to console
        console.print(final_output_str)
        # For console output, a summary might be too verbose if the content itself is printed.
        # Consider a verbosity flag for this summary later.
        # For now, let's make it less prominent or conditional.
        if files_processed_count > 0 or files_skipped_binary_count > 0:  # Only print summary if something happened
            summary_message = (
                f"\n--- Flattened {files_processed_count} file(s). " f"Skipped {files_skipped_binary_count} binary/non-UTF-8 file(s). ---"
            )
            console.print(f"[blue]{summary_message}[/blue]")
