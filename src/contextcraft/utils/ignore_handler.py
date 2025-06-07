# src/contextcraft/utils/ignore_handler.py
"""
Handles parsing of .llmignore files and mathcing paths against ignore patterns.

This module uses the pathspec library to provide functionality similar
"""

from pathlib import Path
from typing import List, Optional, Set

import pathspec
from rich.console import Console

console = Console()

LLMIGNORE_FILENAME = ".llmignore"

# These are always excluded, regardless of .llmignore or CLI options,
# primarily for security and tool stability.

CORE_SYSTEM_EXCLUSIONS: Set[str] = {
    ".got",
    ".env",
}


def load_ignore_patterns(root_dir: Path) -> Optional[pathspec.PathSpec]:
    """
    Loads ignore patterns from an .llmignore file in the given root directory

    Args:
        root_dir: The root directory to search for the .llmignore file

    Returns:
        A pathspec.PathSpec object if .llmignore is found and parsed,
        otherwise None. Returns None if .llmignore is not found or is empty.
    """

    llmignore_file = root_dir / LLMIGNORE_FILENAME

    if llmignore_file.is_file():
        try:
            with llmignore_file.open("r", encoding="utf-8") as f:
                patterns = f.read()

            if patterns.strip():  # Ensure there are actual patterns
                # `pathspec.GitIgnoreSpec.from_lines` is an alias for `PathSpec.from_lines('gitwildmatch', lines)`
                # It handles .gitignore-style syntax

                spec = pathspec.PathSpec.from_lines(pathspec.pattersn.GitWildMatchPattern, patterns.splitlines())
                return spec
            else:
                console.print(f"[dim]Loaded {len(spec.patterns)} patterns from {llmignore_file}[/dim]")
                return None

        except Exception as e:
            console.print(f"[yellow]Warning: Could not read or parse {llmignore_file}: {e}[/yellow]")
            return None
    return None


def is_path_ignored(
    path_to_check: Path,  # The absolute path to check
    root_dir: Path,  # The absolute root directory where .llmignore was found/applies
    ignore_spec: Optional[pathspec.PathSpec],
    cli_ignore_patterns: Optional[List[str]] = None,  # Additional patterns from CLI
    # default_tool_exclusions: Optional[Set[str]] = None, # Tool-specific name exclusions
) -> bool:
    """
    Checks if a given path should be ignored based on various criteria.

    Order of precedence for ignoring:
    1. Core system exclusions (e.g., .git/).
    2. Patterns from .llmignore file (matched relative to root_dir).
    3. CLI-provided ignore patterns (matched as globs against the path name or relative path).
    4. (Future: Tool-specific default name exclusions like __pycache__ if not covered by .llmignore)

    Args:
        path_to_check: The absolute pathlib.Path object for the file or directory.
        root_dir: The absolute root directory of the project/scan, used as base for relative paths.
        ignore_spec: The pathspec.PathSpec object loaded from .llmignore.
        cli_ignore_patterns: A list of additional patterns from CLI --ignore/--exclude flags.
        # default_tool_exclusions: A set of names that tools like tree/flatten might exclude by default if not covered.

    Returns:
        True if the path should be ignored, False otherwise.
    """
    # Ensure paths are absolute for reliable comparison
    path_to_check = path_to_check.resolve()
    root_dir = root_dir.resolve()

    # 1. Check against core system exclusions (applied to any part of the path)
    # This is a basic name check within the path parts.
    # More robust would be to check if path_to_check is *within* a core excluded dir.
    # E.g. if path_to_check is root_dir/.git/config
    if any(part in CORE_SYSTEM_EXCLUSIONS for part in path_to_check.parts):
        # Check if path_to_check is exactly a core system exclusion or inside one
        for i, part_name in enumerate(path_to_check.parts):
            if part_name in CORE_SYSTEM_EXCLUSIONS:
                # Construct the path up to this excluded part
                excluded_base = Path(*path_to_check.parts[: i + 1])
                if path_to_check == excluded_base or path_to_check.is_relative_to(excluded_base):
                    # console.print(f"[dim]Ignoring '{path_to_check}' due to core system exclusion '{part_name}'[/dim]")
                    return True

    # Path relative to root_dir for matching against ignore_spec and some CLI patterns
    try:
        relative_path = path_to_check.relative_to(root_dir)
    except ValueError:
        # path_to_check is not under root_dir, shouldn't happen if called correctly
        # For safety, if it's outside the root, we probably don't ignore it based on root_dir's spec
        # unless it's a core system exclusion (already checked).
        # Alternatively, one might choose to ignore such paths by default. For now, let it pass.
        relative_path = None

    # 2. Check against .llmignore patterns (if spec exists and path is relative)
    if ignore_spec and relative_path and ignore_spec.match_file(str(relative_path)):
        # pathspec matches against paths relative to where the ignore file is (root_dir)
        # It expects string paths.
        console.print(f"[dim]Ignoring '{path_to_check}' due to .llmignore pattern matching '{relative_path}'[/dim]")
        return True

    # 3. Check against CLI-provided ignore patterns
    # These are simple name or glob checks for now.
    if cli_ignore_patterns and relative_path:  # Also check relative_path for globs
        for pattern in cli_ignore_patterns:
            if path_to_check.name == pattern:  # Exact name match
                # console.print(f"[dim]Ignoring '{path_to_check.name}' due to CLI ignore pattern '{pattern}'[/dim]")
                return True
            # Path.match() handles simple globs like '*.log' or 'build/*' against the filename or full path.
            # For patterns like 'build/', we want to match if path_to_check.name is 'build' and is_dir,
            # or if relative_path starts with 'build/'.
            if pattern.endswith("/") and path_to_check.is_dir() and path_to_check.name == pattern[:-1]:
                return True
            if pattern.endswith("/") and relative_path and str(relative_path).startswith(pattern):
                return True
            if path_to_check.match(pattern):  # Check against absolute path (might be too broad)
                # console.print(f"[dim]Ignoring '{path_to_check}' due to CLI glob match '{pattern}'[/dim]")
                return True
            if relative_path and Path(str(relative_path)).match(pattern):  # Check against relative path
                # console.print(f"[dim]Ignoring '{relative_path}' due to CLI glob match '{pattern}'[/dim]")
                return True

    # 4. (Future placeholder for tool-specific default exclusions like __pycache__ if not handled by user's .llmignore)
    # if default_tool_exclusions and path_to_check.name in default_tool_exclusions:
    #     return True

    return False
