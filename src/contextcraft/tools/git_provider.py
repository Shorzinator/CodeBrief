# src/contextcraft/tools/git_provider.py
"""
Git Context Provider for ContextCraft.

This module provides functions to extract Git context information from a project
repository, including current branch, status, uncommitted changes, and recent commits.
It uses subprocess calls to interact with Git and formats the output as structured
Markdown suitable for inclusion in context bundles.

Core functionalities:
- Extract current branch name
- Get Git status summary
- List uncommitted changes with file status
- Retrieve recent commit history
- Support for optional diff output (controlled by parameters)
- Graceful handling of non-Git repositories
- Structured Markdown output with clear sectioning
"""

import subprocess  # nosec B404
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def get_git_context(
    project_root: Path,
    diff_options: Optional[str] = None,
    log_count: int = 5,
    full_diff: bool = False,
) -> str:
    """
    Extract Git context information from a project repository.

    This function executes various Git commands to gather comprehensive context
    about the repository state, including branch information, file changes,
    and commit history. All output is formatted as structured Markdown.

    Args:
        project_root: The root directory of the Git repository
        diff_options: Optional string for advanced git diff options (e.g., "--stat", "src/myfile.py")
        log_count: Number of recent commits to include (default: 5)
        full_diff: If True, include full diff output (default: False)

    Returns:
        Formatted Markdown string containing Git context information

    Note:
        No exceptions are raised; all errors are captured and included in the output
    """
    if not project_root.exists():
        return (
            f"# Git Context\n\nError: Project path '{project_root}' does not exist.\n"
        )

    if not project_root.is_dir():
        return f"# Git Context\n\nError: Project path '{project_root}' is not a directory.\n"

    # Check if git executable is available
    try:
        subprocess.run(  # nosec B603, B607
            ["git", "--version"],
            capture_output=True,
            check=True,
            timeout=10,
        )
    except FileNotFoundError:
        return "# Git Context\n\nError: Git executable not found. Please ensure Git is installed and available in PATH.\n"
    except subprocess.TimeoutExpired:
        return "# Git Context\n\nError: Git command timed out.\n"
    except subprocess.CalledProcessError:
        return "# Git Context\n\nError: Git executable found but returned an error.\n"

    # Check if this is a Git repository
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=10,
        )
        if result.stdout.strip() != "true":
            return "# Git Context\n\nNot a Git repository or no Git history.\n"
    except subprocess.CalledProcessError:
        return "# Git Context\n\nNot a Git repository or no Git history.\n"
    except subprocess.TimeoutExpired:
        return "# Git Context\n\nError: Git command timed out while checking repository status.\n"
    except Exception as e:
        return f"# Git Context\n\nError checking Git repository: {e}\n"

    # Now we know it's a valid Git repository, gather information
    markdown_sections = ["# Git Context\n"]

    # 1. Get current branch
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=10,
        )
        current_branch = result.stdout.strip()
        markdown_sections.append("## Current Branch\n")
        markdown_sections.append("```")
        markdown_sections.append(current_branch)
        markdown_sections.append("```\n")
    except subprocess.CalledProcessError as e:
        markdown_sections.append("## Current Branch\n")
        markdown_sections.append("```")
        markdown_sections.append(
            f"Error getting current branch: {e.stderr.strip() if e.stderr else 'Unknown error'}"
        )
        markdown_sections.append("```\n")
    except subprocess.TimeoutExpired:
        markdown_sections.append("## Current Branch\n")
        markdown_sections.append("```")
        markdown_sections.append("Error: Git command timed out")
        markdown_sections.append("```\n")
    except Exception as e:
        markdown_sections.append("## Current Branch\n")
        markdown_sections.append("```")
        markdown_sections.append(f"Error: {e}")
        markdown_sections.append("```\n")

    # 2. Get Git status
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "status", "--short"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=10,
        )
        git_status = result.stdout.strip()
        markdown_sections.append("## Git Status\n")
        markdown_sections.append("```")
        if git_status:
            markdown_sections.append(git_status)
        else:
            markdown_sections.append("Working tree clean")
        markdown_sections.append("```\n")
    except subprocess.CalledProcessError as e:
        markdown_sections.append("## Git Status\n")
        markdown_sections.append("```")
        markdown_sections.append(
            f"Error getting Git status: {e.stderr.strip() if e.stderr else 'Unknown error'}"
        )
        markdown_sections.append("```\n")
    except subprocess.TimeoutExpired:
        markdown_sections.append("## Git Status\n")
        markdown_sections.append("```")
        markdown_sections.append("Error: Git command timed out")
        markdown_sections.append("```\n")
    except Exception as e:
        markdown_sections.append("## Git Status\n")
        markdown_sections.append("```")
        markdown_sections.append(f"Error: {e}")
        markdown_sections.append("```\n")

    # 3. Get uncommitted changes (tracked files)
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "diff", "HEAD", "--name-status"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=15,
        )
        uncommitted_changes = result.stdout.strip()
        markdown_sections.append("## Uncommitted Changes (Tracked Files)\n")
        markdown_sections.append("```")
        if uncommitted_changes:
            markdown_sections.append(uncommitted_changes)
        else:
            markdown_sections.append("No uncommitted changes to tracked files")
        markdown_sections.append("```\n")
    except subprocess.CalledProcessError as e:
        markdown_sections.append("## Uncommitted Changes (Tracked Files)\n")
        markdown_sections.append("```")
        markdown_sections.append(
            f"Error getting uncommitted changes: {e.stderr.strip() if e.stderr else 'Unknown error'}"
        )
        markdown_sections.append("```\n")
    except subprocess.TimeoutExpired:
        markdown_sections.append("## Uncommitted Changes (Tracked Files)\n")
        markdown_sections.append("```")
        markdown_sections.append("Error: Git command timed out")
        markdown_sections.append("```\n")
    except Exception as e:
        markdown_sections.append("## Uncommitted Changes (Tracked Files)\n")
        markdown_sections.append("```")
        markdown_sections.append(f"Error: {e}")
        markdown_sections.append("```\n")

    # 4. Get recent commits
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "log", "-n", str(log_count), "--oneline", "--decorate", "--graph"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=15,
        )
        recent_commits = result.stdout.strip()
        markdown_sections.append(f"## Recent Commits (Last {log_count})\n")
        markdown_sections.append("```")
        if recent_commits:
            markdown_sections.append(recent_commits)
        else:
            markdown_sections.append("No commits found")
        markdown_sections.append("```\n")
    except subprocess.CalledProcessError as e:
        markdown_sections.append(f"## Recent Commits (Last {log_count})\n")
        markdown_sections.append("```")
        markdown_sections.append(
            f"Error getting recent commits: {e.stderr.strip() if e.stderr else 'Unknown error'}"
        )
        markdown_sections.append("```\n")
    except subprocess.TimeoutExpired:
        markdown_sections.append(f"## Recent Commits (Last {log_count})\n")
        markdown_sections.append("```")
        markdown_sections.append("Error: Git command timed out")
        markdown_sections.append("```\n")
    except Exception as e:
        markdown_sections.append(f"## Recent Commits (Last {log_count})\n")
        markdown_sections.append("```")
        markdown_sections.append(f"Error: {e}")
        markdown_sections.append("```\n")

    # 5. Optional full diff or custom diff options
    if full_diff or diff_options:
        try:
            diff_cmd = ["git", "diff", "HEAD"]
            if diff_options:
                # Split diff_options and add to command
                # This is a simple split - in production, you might want more sophisticated parsing
                diff_cmd.extend(diff_options.split())

            result = subprocess.run(  # nosec B603, B607
                diff_cmd,
                cwd=project_root,
                capture_output=True,
                check=True,
                text=True,
                timeout=30,  # Longer timeout for diff operations
            )
            diff_output = result.stdout.strip()

            diff_title = "## Full Diff" if full_diff else f"## Diff ({diff_options})"
            markdown_sections.append(f"{diff_title}\n")
            markdown_sections.append("```diff")
            if diff_output:
                markdown_sections.append(diff_output)
            else:
                markdown_sections.append("No differences found")
            markdown_sections.append("```\n")
        except subprocess.CalledProcessError as e:
            diff_title = "## Full Diff" if full_diff else f"## Diff ({diff_options})"
            markdown_sections.append(f"{diff_title}\n")
            markdown_sections.append("```")
            markdown_sections.append(
                f"Error getting diff: {e.stderr.strip() if e.stderr else 'Unknown error'}"
            )
            markdown_sections.append("```\n")
        except subprocess.TimeoutExpired:
            diff_title = "## Full Diff" if full_diff else f"## Diff ({diff_options})"
            markdown_sections.append(f"{diff_title}\n")
            markdown_sections.append("```")
            markdown_sections.append("Error: Git diff command timed out")
            markdown_sections.append("```\n")
        except Exception as e:
            diff_title = "## Full Diff" if full_diff else f"## Diff ({diff_options})"
            markdown_sections.append(f"{diff_title}\n")
            markdown_sections.append("```")
            markdown_sections.append(f"Error: {e}")
            markdown_sections.append("```\n")

    return "\n".join(markdown_sections)
