# src/contextcraft/tools/bundler.py
"""
Bundle Generator for ContextCraft.

This module provides functions to create comprehensive context bundles by
orchestrating calls to multiple ContextCraft tools. It aggregates outputs
from tree generation, Git context, dependency listing, and file flattening
into a single, well-structured Markdown document suitable for LLM consumption.

Core functionalities:
- Orchestrate multiple tool outputs into a single bundle
- Support configurable inclusion/exclusion of different context sections
- Handle multiple flatten specifications for different parts of the project
- Generate structured Markdown with clear sectioning and navigation
- Graceful error handling when individual tools encounter issues
- Support for both file output and console display
"""

import warnings
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from ..utils import config_manager
from . import dependency_lister, flattener, git_provider, tree_generator

console = Console()


def generate_tree_content(
    project_root: Path,
    config_global_excludes: List[str],
) -> str:
    """
    Generate directory tree content for the bundle.

    Args:
        project_root: The root directory of the project
        config_global_excludes: Global exclude patterns from config

    Returns:
        Formatted tree content as string, or error message if generation fails
    """
    try:
        # We need to capture the tree output as a string rather than printing it
        # The tree_generator currently outputs to file or console, we need string output
        # Let's use a temporary approach by redirecting to a temporary file-like object
        import sys
        from io import StringIO

        # Temporarily redirect stdout to capture tree output
        old_stdout = sys.stdout
        string_buffer = StringIO()
        sys.stdout = string_buffer

        try:
            tree_generator.generate_and_output_tree(
                root_dir=project_root,
                output_file_path=None,  # This will print to stdout (our captured buffer)
                ignore_list=[],
                config_global_excludes=config_global_excludes,
            )
        finally:
            sys.stdout = old_stdout

        tree_content = string_buffer.getvalue()
        return tree_content.strip() if tree_content else "No tree content generated"

    except Exception as e:
        return f"Error generating directory tree: {e}"


def generate_git_content(
    project_root: Path,
    log_count: int = 5,
    full_diff: bool = False,
    diff_options: Optional[str] = None,
) -> str:
    """
    Generate Git context content for the bundle.

    Args:
        project_root: The root directory of the project
        log_count: Number of recent commits to include
        full_diff: Whether to include full diff output
        diff_options: Optional diff options string

    Returns:
        Formatted Git context as string
    """
    try:
        return git_provider.get_git_context(
            project_root=project_root,
            diff_options=diff_options,
            log_count=log_count,
            full_diff=full_diff,
        )
    except Exception as e:
        return f"# Git Context\n\nError generating Git context: {e}\n"


def generate_deps_content(project_root: Path) -> str:
    """
    Generate dependency listing content for the bundle.

    Args:
        project_root: The root directory of the project

    Returns:
        Formatted dependency content as string
    """
    try:
        # Similar to tree generation, we need to capture the deps output
        import sys
        from io import StringIO

        # Temporarily redirect stdout to capture deps output
        old_stdout = sys.stdout
        string_buffer = StringIO()
        sys.stdout = string_buffer

        try:
            dependency_lister.list_dependencies_logic(
                project_path=project_root,
                actual_output_path=None,  # This will print to stdout (our captured buffer)
            )
        finally:
            sys.stdout = old_stdout

        deps_content = string_buffer.getvalue()
        return (
            deps_content.strip()
            if deps_content
            else "# Project Dependencies\n\nNo dependencies found.\n"
        )

    except Exception as e:
        return f"# Project Dependencies\n\nError generating dependency list: {e}\n"


def generate_flatten_content(
    project_root: Path,
    flatten_path: Path,
    config_global_excludes: List[str],
) -> str:
    """
    Generate flattened file content for a specific path.

    Args:
        project_root: The root directory of the project
        flatten_path: The specific path to flatten
        config_global_excludes: Global exclude patterns from config

    Returns:
        Formatted flattened content as string
    """
    try:
        # We need to capture the flattener output
        import sys
        from io import StringIO

        # Temporarily redirect stdout to capture flattener output
        old_stdout = sys.stdout
        string_buffer = StringIO()
        sys.stdout = string_buffer

        try:
            # If flatten_path is different from project_root, we need to call flattener on that specific path
            if flatten_path != project_root:
                flattener.flatten_code_logic(
                    root_dir=flatten_path,
                    output_file_path=None,  # This will print to stdout (our captured buffer)
                    include_patterns=None,  # Use defaults
                    exclude_patterns=None,  # Use defaults + config
                    config_global_excludes=config_global_excludes,
                )
            else:
                flattener.flatten_code_logic(
                    root_dir=project_root,
                    output_file_path=None,  # This will print to stdout (our captured buffer)
                    include_patterns=None,  # Use defaults
                    exclude_patterns=None,  # Use defaults + config
                    config_global_excludes=config_global_excludes,
                )
        finally:
            sys.stdout = old_stdout

        flatten_content = string_buffer.getvalue()
        if not flatten_content.strip():
            return f"# Files: {flatten_path.relative_to(project_root) if flatten_path != project_root else 'Project Root'}\n\nNo files found to flatten in this path.\n"

        # Add a header for this flatten section
        relative_path = (
            flatten_path.relative_to(project_root)
            if flatten_path != project_root
            else "Project Root"
        )
        header = f"# Files: {relative_path}\n\n"
        return header + flatten_content.strip()

    except Exception as e:
        relative_path = (
            flatten_path.relative_to(project_root)
            if flatten_path != project_root
            else "Project Root"
        )
        return f"# Files: {relative_path}\n\nError flattening files: {e}\n"


def create_bundle(
    project_root: Path,
    output_file_path: Optional[Path] = None,
    include_tree: bool = True,
    include_git: bool = True,
    include_deps: bool = True,
    flatten_paths: Optional[List[Path]] = None,
    git_log_count: int = 5,
    git_full_diff: bool = False,
    git_diff_options: Optional[str] = None,
) -> None:
    """
    Create a comprehensive context bundle by aggregating multiple tool outputs.

    This function orchestrates calls to various ContextCraft tools and combines
    their outputs into a single, well-structured Markdown document. The bundle
    includes a table of contents and clear sectioning for easy navigation.

    Args:
        project_root: The root directory of the project to bundle
        output_file_path: Optional path to save the bundle. If None, prints to console
        include_tree: Whether to include directory tree (default: True)
        include_git: Whether to include Git context (default: True)
        include_deps: Whether to include dependency information (default: True)
        flatten_paths: Optional list of paths to flatten and include
        git_log_count: Number of recent commits to include in Git context
        git_full_diff: Whether to include full diff in Git context
        git_diff_options: Optional Git diff options string

    Raises:
        typer.Exit: If project_root is invalid or critical errors occur
    """
    if not project_root.exists():
        console.print(
            f"[bold red]Error: Project path '{project_root}' does not exist.[/bold red]"
        )
        raise typer.Exit(code=1)

    if not project_root.is_dir():
        console.print(
            f"[bold red]Error: Project path '{project_root}' is not a directory.[/bold red]"
        )
        raise typer.Exit(code=1)

    # Load configuration
    config = config_manager.load_config(project_root)
    config_global_excludes = config.get("global_exclude_patterns", [])
    if not isinstance(config_global_excludes, list):
        warnings.warn(
            "Config Warning: 'global_exclude_patterns' should be a list. Using empty list.",
            UserWarning,
            stacklevel=2,
        )
        config_global_excludes = []

    if output_file_path:
        console.print(
            f"[dim]Generating context bundle for '{project_root.resolve()}'...[/dim]"
        )

    # Start building the bundle
    bundle_sections = []

    # Header and project info
    project_name = project_root.name if project_root.name else "Unknown Project"
    bundle_sections.append(f"# ContextCraft Bundle: {project_name}")
    bundle_sections.append("")
    bundle_sections.append(f"**Project Root:** `{project_root.resolve()}`")
    bundle_sections.append("")

    # Table of Contents
    toc_items = []
    if include_tree:
        toc_items.append("- [Directory Tree](#directory-tree)")
    if include_git:
        toc_items.append("- [Git Context](#git-context)")
    if include_deps:
        toc_items.append("- [Project Dependencies](#project-dependencies)")
    if flatten_paths:
        for flatten_path in flatten_paths:
            relative_path = (
                flatten_path.relative_to(project_root)
                if flatten_path != project_root
                else "project-root"
            )
            relative_path_str = str(relative_path)
            toc_items.append(
                f"- [Files: {relative_path}](#files-{relative_path_str.replace('/', '-').replace('_', '-').lower()})"
            )

    if toc_items:
        bundle_sections.append("## Table of Contents")
        bundle_sections.append("")
        bundle_sections.extend(toc_items)
        bundle_sections.append("")
        bundle_sections.append("---")
        bundle_sections.append("")

    # Generate and add each section
    section_count = 0

    # 1. Directory Tree
    if include_tree:
        if output_file_path:
            console.print("[dim]  - Generating directory tree...[/dim]")

        tree_content = generate_tree_content(project_root, config_global_excludes)

        bundle_sections.append("## Directory Tree")
        bundle_sections.append("")
        bundle_sections.append("```")
        bundle_sections.append(tree_content)
        bundle_sections.append("```")
        bundle_sections.append("")
        section_count += 1

    # 2. Git Context
    if include_git:
        if output_file_path:
            console.print("[dim]  - Generating Git context...[/dim]")

        git_content = generate_git_content(
            project_root,
            log_count=git_log_count,
            full_diff=git_full_diff,
            diff_options=git_diff_options,
        )

        # Remove the main header from git content since we'll add our own
        git_lines = git_content.split("\n")
        if git_lines and git_lines[0].startswith("# Git Context"):
            git_lines = git_lines[1:]  # Remove the first line
            if git_lines and git_lines[0] == "":
                git_lines = git_lines[1:]  # Remove empty line after header

        bundle_sections.append("## Git Context")
        bundle_sections.append("")
        bundle_sections.extend(git_lines)
        bundle_sections.append("")
        section_count += 1

    # 3. Dependencies
    if include_deps:
        if output_file_path:
            console.print("[dim]  - Generating dependency information...[/dim]")

        deps_content = generate_deps_content(project_root)

        # Remove the main header from deps content since we'll add our own
        deps_lines = deps_content.split("\n")
        if deps_lines and deps_lines[0].startswith("# Project Dependencies"):
            deps_lines = deps_lines[1:]  # Remove the first line
            if deps_lines and deps_lines[0] == "":
                deps_lines = deps_lines[1:]  # Remove empty line after header

        bundle_sections.append("## Project Dependencies")
        bundle_sections.append("")
        bundle_sections.extend(deps_lines)
        bundle_sections.append("")
        section_count += 1

    # 4. Flattened Files
    if flatten_paths:
        for flatten_path in flatten_paths:
            if not flatten_path.exists():
                console.print(
                    f"[yellow]Warning: Flatten path '{flatten_path}' does not exist. Skipping.[/yellow]"
                )
                continue

            if output_file_path:
                relative_path = (
                    flatten_path.relative_to(project_root)
                    if flatten_path != project_root
                    else "project root"
                )
                console.print(
                    f"[dim]  - Flattening files in '{relative_path}'...[/dim]"
                )

            flatten_content = generate_flatten_content(
                project_root, flatten_path, config_global_excludes
            )

            # Remove the main header from flatten content since we'll add our own
            flatten_lines = flatten_content.split("\n")
            if flatten_lines and flatten_lines[0].startswith("# Files:"):
                section_title = flatten_lines[0][2:]  # Remove "# " prefix
                flatten_lines = flatten_lines[1:]  # Remove the first line
                if flatten_lines and flatten_lines[0] == "":
                    flatten_lines = flatten_lines[1:]  # Remove empty line after header
            else:
                relative_path = (
                    flatten_path.relative_to(project_root)
                    if flatten_path != project_root
                    else "Project Root"
                )
                section_title = f"Files: {relative_path}"

            bundle_sections.append(f"## {section_title}")
            bundle_sections.append("")
            bundle_sections.extend(flatten_lines)
            bundle_sections.append("")
            section_count += 1

    # Footer
    bundle_sections.append("---")
    bundle_sections.append("")
    bundle_sections.append(
        f"*Bundle generated by ContextCraft - {section_count} sections included*"
    )

    # Combine all sections
    bundle_content = "\n".join(bundle_sections)

    # Output the bundle
    if output_file_path:
        try:
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            with output_file_path.open("w", encoding="utf-8") as f:
                f.write(bundle_content)
            console.print(
                f"[green]Successfully created context bundle: '{output_file_path.resolve()}'[/green]"
            )
            console.print(f"[dim]Bundle contains {section_count} sections[/dim]")
        except OSError as e:
            console.print(
                f"[bold red]Error writing bundle to '{output_file_path}': {e}[/bold red]"
            )
            raise typer.Exit(code=1) from e
    else:
        # Print to console using Rich for better formatting
        from rich.markdown import Markdown

        markdown_obj = Markdown(bundle_content)
        console.print(markdown_obj)
