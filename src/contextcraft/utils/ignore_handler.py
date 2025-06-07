# src/contextcraft/utils/ignore_handler.py
"""
Handles parsing of .llmignore files and mathcing paths against ignore patterns.

This module uses the pathspec library to provide functionality similar
"""

from contextlib import suppress
from pathlib import Path
from typing import List, Optional, Set

import pathspec
from rich.console import Console

console = Console()

LLMIGNORE_FILENAME = ".llmignore"

# These are always excluded, regardless of .llmignore or CLI options,
# primarily for security and tool stability.

CORE_SYSTEM_EXCLUSIONS: Set[str] = {
    ".git",
    # ".env",
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
                    pattern_part = parts[0].strip()  # Pattern is before the first #, then strip

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
            spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, processed_lines)

            if not spec.patterns:
                # console.print(f"[dim].llmignore file at {llmignore_file} resulted in no patterns in spec.[/dim]")
                return None
            return spec

        except Exception as e:
            console.print(f"[yellow]Warning: Could not read or parse {llmignore_file}: {e}[/yellow]")
            return None
    return None


def is_path_ignored(
    path_to_check: Path,
    root_dir: Path,
    ignore_spec: Optional[pathspec.PathSpec],
    cli_ignore_patterns: Optional[List[str]] = None,
) -> bool:
    path_to_check_abs = path_to_check.resolve()
    root_dir_abs = root_dir.resolve()

    # 1. Check against core system exclusions
    for i, part_name in enumerate(path_to_check_abs.parts):
        if part_name in CORE_SYSTEM_EXCLUSIONS:
            excluded_base = Path(*path_to_check_abs.parts[: i + 1])
            if path_to_check_abs == excluded_base or path_to_check_abs.is_relative_to(excluded_base):
                return True

    relative_path_for_spec: Optional[Path] = None
    with suppress(ValueError):
        relative_path_for_spec = path_to_check_abs.relative_to(root_dir_abs)

    # 2. Check against .llmignore patterns
    if ignore_spec and relative_path_for_spec is not None:
        # Path string without trailing slash for patterns like "name" (matching file or dir)
        path_str_name_only = relative_path_for_spec.as_posix()

        # Path string with trailing slash for patterns like "name/" (matching dir explicitly)
        path_str_as_dir = path_str_name_only
        if path_to_check_abs.is_dir():
            if str(relative_path_for_spec) == ".":  # Root directory itself
                path_str_as_dir = "./"  # Note: pathspec matches "./" against "/" pattern.
            elif not path_str_as_dir.endswith("/"):
                path_str_as_dir += "/"

        # Debug print for clarity before matching attempts
        print(f"    SpecCheck Input: Path='{path_to_check_abs.name}', IsDir={path_to_check_abs.is_dir()}, RelPathForSpec='{relative_path_for_spec}'")
        print(f"    SpecCheck Attempt1 (as_dir if applicable): PathStr='{path_str_as_dir}', Match={ignore_spec.match_file(path_str_as_dir)}")
        print(f"    SpecCheck Attempt2 (name_only if different): PathStr='{path_str_name_only}', Match={ignore_spec.match_file(path_str_name_only)}")

        # A. Check if a directory-specific pattern (e.g., "build/") matches the directory.
        #    For this, we use the path_str_as_dir (e.g., "build/").
        if path_to_check_abs.is_dir() and ignore_spec.match_file(path_str_as_dir):
            print(f"    [MATCHED DIR AS DIR_PATTERN] SpecCheck: Path='{path_str_as_dir}', IsDir={path_to_check_abs.is_dir()}, Match=True")
            return True

        # B. Check if a name pattern (e.g., "some_name" which can be file or dir)
        #    matches the path (file or directory name).
        #    For this, we use path_str_name_only (e.g., "build" or "file.txt").
        #    This also handles files correctly.
        if ignore_spec.match_file(path_str_name_only):
            print(f"    [MATCHED AS NAME_PATTERN] SpecCheck: Path='{path_str_name_only}', IsDir={path_to_check_abs.is_dir()}, Match=True")
            return True

    # 3. Check against CLI-provided ignore patterns
    if cli_ignore_patterns:
        filename = path_to_check_abs.name
        for pattern in cli_ignore_patterns:
            if filename == pattern:
                return True
            if Path(filename).match(pattern):
                return True  # Simple glob on name
            if relative_path_for_spec:
                # More complex CLI patterns might need pathspec-like handling too
                # For now, keep it simpler.
                rel_path_str_cli = relative_path_for_spec.as_posix()
                current_path_for_cli_match = Path(rel_path_str_cli)  # Path object for .match()

                if pattern.endswith("/") and path_to_check_abs.is_dir():
                    # Ensure rel_path_str_cli for dir also ends with / for comparison
                    path_to_match_cli_dir = rel_path_str_cli
                    if not path_to_match_cli_dir.endswith("/"):
                        path_to_match_cli_dir += "/"
                    if path_to_match_cli_dir == pattern:
                        return True
                    # Match "build/" pattern against directory name "build"
                    if current_path_for_cli_match.name + "/" == pattern:
                        return True

                if current_path_for_cli_match.match(pattern):
                    return True
    return False
