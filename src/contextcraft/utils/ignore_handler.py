# src/contextcraft/utils/ignore_handler.py
"""Handles parsing of .llmignore files and mathcing paths against ignore patterns.

This module uses the pathspec library to provide functionality similar
"""

from contextlib import suppress
from pathlib import Path
from typing import Optional

import pathspec
from rich.console import Console

console = Console()

LLMIGNORE_FILENAME = ".llmignore"

# These are always excluded, regardless of .llmignore or CLI options,
# primarily for security and tool stability.

CORE_SYSTEM_EXCLUSIONS: set[str] = {
    ".git",
    # ".env",
}


def load_ignore_patterns(root_dir: Path) -> Optional[pathspec.PathSpec]:
    """Loads ignore patterns from an .llmignore file in the given root directory

    Args:
    ----
        root_dir: The root directory to search for the .llmignore file

    Returns:
    -------
        A pathspec.PathSpec object if .llmignore is found and parsed,
        otherwise None. Returns None if .llmignore is not found or is empty.

    """
    llmignore_file = root_dir / LLMIGNORE_FILENAME

    if llmignore_file.is_file():
        try:
            with llmignore_file.open("r", encoding="utf-8") as f:
                lines = f.read().splitlines()

            processed_lines = []
            for line_content in lines:  # Iterate with line number for potential debug
                # 1. Remove potential BOM and leading/trailing whitespace from the whole line first
                current_line = line_content.strip()

                # 2. Ignore empty lines or lines that are purely comments
                if not current_line or current_line.startswith("#"):
                    continue

                # 3. Separate pattern from trailing comments
                pattern_part = current_line
                if "#" in current_line:
                    # Ensure '#' is not part of a valid filename/pattern (e.g. escaped \#)
                    # For simplicity, we assume '#' always starts a comment if not at the beginning.
                    # A more robust parser would handle escaped '#'.
                    # Find the first '#' that is likely a comment starter
                    # comment_start_index = -1
                    # Gitignore: A hash HASH `"#"` marks the beginning of a comment.
                    # Put a backslash `"\#"` in front of the first hash if it is part of a pattern.
                    # For now, we'll assume unescaped # is a comment.

                    # Simplistic approach: split by "#" and take the first part
                    # This might fail if "#" is a valid character in a filename and not escaped.
                    # Git's behavior is nuanced here. For now, let's be pragmatic.
                    parts = current_line.split("#", 1)
                    pattern_part = parts[
                        0
                    ].strip()  # Pattern is before the first #, then strip

                    # If pattern_part becomes empty after removing comment, skip
                    if not pattern_part:
                        continue

                # 4. Handle negation '!' specifically for stripping
                if pattern_part.startswith("!"):
                    # Preserve '!', strip the actual pattern content after '!'
                    actual_pattern = pattern_part[1:].strip()
                    if actual_pattern:  # Ensure pattern after '!' is not empty
                        processed_lines.append("!" + actual_pattern)
                elif pattern_part:  # Ensure non-negated pattern is not empty
                    processed_lines.append(pattern_part)

            if not processed_lines:
                # console.print(f"[dim].llmignore file at {llmignore_file} contains no active patterns after processing.[/dim]")
                return None

            # console.print(f"[dim]PATTERNS TO PATHSPEC: {processed_lines}[/dim]") # DEBUG
            spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, processed_lines
            )

            if not spec.patterns:
                # console.print(f"[dim].llmignore file at {llmignore_file} resulted in no patterns in spec.[/dim]")
                return None
            return spec

        except Exception as e:
            console.print(
                f"[yellow]Warning: Could not read or parse {llmignore_file}: {e}[/yellow]"
            )
            return None
    return None


def is_path_ignored(
    path_to_check: Path,
    root_dir: Path,
    ignore_spec: Optional[pathspec.PathSpec],
    cli_ignore_patterns: Optional[list[str]] = None,
    config_exclude_patterns: Optional[list[str]] = None,
) -> bool:
    path_to_check_abs = path_to_check.resolve()
    root_dir_abs = root_dir.resolve()

    # 1. Check against core system exclusions (HIGHEST PRECEDENCE)
    for i, part_name in enumerate(path_to_check_abs.parts):
        if part_name in CORE_SYSTEM_EXCLUSIONS:
            excluded_base = Path(*path_to_check_abs.parts[: i + 1])
            if path_to_check_abs == excluded_base or path_to_check_abs.is_relative_to(
                excluded_base
            ):
                # console.print(f"[dim]Ignoring '{path_to_check_abs}' due to CORE system exclusion '{part_name}'[/dim]")
                return True

    relative_path_for_spec: Optional[Path] = None
    with suppress(ValueError):  # path_to_check_abs might not be under root_dir_abs
        relative_path_for_spec = path_to_check_abs.relative_to(root_dir_abs)

    # 2. Check against .llmignore patterns (SECOND PRECEDENCE)
    if ignore_spec and relative_path_for_spec is not None:
        path_str_name_only = relative_path_for_spec.as_posix()
        path_str_as_dir = path_str_name_only
        if path_to_check_abs.is_dir():
            if str(relative_path_for_spec) == ".":
                path_str_as_dir = "./"
            elif not path_str_as_dir.endswith("/"):
                path_str_as_dir += "/"

        if path_to_check_abs.is_dir() and ignore_spec.match_file(path_str_as_dir):
            # console.print(f"[dim]Ignoring '{path_to_check_abs}' (as dir) due to .llmignore matching '{path_str_as_dir}'[/dim]")
            return True
        if ignore_spec.match_file(path_str_name_only):
            # console.print(f"[dim]Ignoring '{path_to_check_abs}' (as path) due to .llmignore matching '{path_str_name_only}'[/dim]")
            return True

    # 3. Check against config_exclude_patterns (THIRD PRECEDENCE)
    if config_exclude_patterns:
        filename = path_to_check_abs.name
        for pattern in config_exclude_patterns:
            if filename == pattern:
                return True
            if Path(filename).match(pattern):
                return True
            if relative_path_for_spec:
                rel_path_str = relative_path_for_spec.as_posix()
                current_path_obj_for_match = Path(rel_path_str)

                # For directory patterns ending with "/", check if this is a directory
                if pattern.endswith("/") and path_to_check_abs.is_dir():
                    path_to_match_as_dir = rel_path_str
                    if not path_to_match_as_dir.endswith("/"):
                        path_to_match_as_dir += "/"
                    if path_to_match_as_dir == pattern:
                        return True
                    if current_path_obj_for_match.name + "/" == pattern:
                        return True

                # For directory patterns ending with "/", also check if any parent directory matches
                if pattern.endswith("/"):
                    # Check if any parent directory of the file matches the pattern
                    for parent in current_path_obj_for_match.parents:
                        parent_str = parent.as_posix()
                        if parent_str + "/" == pattern:
                            return True
                        if parent.name + "/" == pattern:
                            return True

                if current_path_obj_for_match.match(pattern):
                    return True

    # 4. Check against CLI-provided ignore patterns (FOURTH PRECEDENCE)
    # This block is your existing CLI ignore logic, now at a lower precedence.
    if cli_ignore_patterns:
        filename = path_to_check_abs.name
        for pattern in cli_ignore_patterns:
            if filename == pattern:
                return True
            if Path(filename).match(pattern):
                return True
            if relative_path_for_spec:
                rel_path_str_cli = relative_path_for_spec.as_posix()
                current_path_for_cli_match = Path(rel_path_str_cli)

                # For directory patterns ending with "/", check if this is a directory
                if pattern.endswith("/") and path_to_check_abs.is_dir():
                    path_to_match_cli_dir = rel_path_str_cli
                    if not path_to_match_cli_dir.endswith("/"):
                        path_to_match_cli_dir += "/"
                    if path_to_match_cli_dir == pattern:
                        return True
                    if current_path_for_cli_match.name + "/" == pattern:
                        return True

                # For directory patterns ending with "/", also check if any parent directory matches
                if pattern.endswith("/"):
                    # Check if any parent directory of the file matches the pattern
                    for parent in current_path_for_cli_match.parents:
                        parent_str = parent.as_posix()
                        if parent_str + "/" == pattern:
                            return True
                        if parent.name + "/" == pattern:
                            return True

                if current_path_for_cli_match.match(pattern):
                    return True

    return False
