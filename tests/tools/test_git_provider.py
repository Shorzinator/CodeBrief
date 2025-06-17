"""Tests for the git provider module."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from codebrief.tools import git_provider


class TestGetGitContext:
    """Test cases for the get_git_context function."""

    def test_non_existent_path(self):
        """Test error handling for non-existent project path."""
        non_existent_path = Path("/this/path/does/not/exist")
        result = git_provider.get_git_context(non_existent_path)

        assert "# Git Context" in result
        assert "Error: Project path" in result
        assert "does not exist" in result

    def test_path_is_not_directory(self, tmp_path):
        """Test error handling when path is not a directory."""
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("test content")

        result = git_provider.get_git_context(test_file)

        assert "# Git Context" in result
        assert "Error: Project path" in result
        assert "is not a directory" in result

    @patch("subprocess.run")
    def test_git_not_installed(self, mock_run, tmp_path):
        """Test error handling when Git is not installed."""
        mock_run.side_effect = FileNotFoundError("git command not found")

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "Error: Git executable not found" in result
        assert "Please ensure Git is installed" in result

    @patch("subprocess.run")
    def test_git_timeout(self, mock_run, tmp_path):
        """Test error handling when Git command times out."""
        mock_run.side_effect = subprocess.TimeoutExpired("git", 10)

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "Error: Git command timed out" in result

    @patch("subprocess.run")
    def test_git_executable_error(self, mock_run, tmp_path):
        """Test error handling when Git executable returns error."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git --version")

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "Error: Git executable found but returned an error" in result

    @patch("subprocess.run")
    def test_not_git_repository(self, mock_run, tmp_path):
        """Test error handling when directory is not a Git repository."""
        # First call (git --version) succeeds
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version succeeds
            subprocess.CalledProcessError(
                128, "git rev-parse --is-inside-work-tree"
            ),  # not a git repo
        ]

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "Not a Git repository or no Git history" in result

    @patch("subprocess.run")
    def test_successful_git_context_clean_repo(self, mock_run, tmp_path):
        """Test successful Git context extraction from a clean repository."""
        # Mock all subprocess calls for a successful scenario
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            MagicMock(stdout="main\n", returncode=0),  # current branch
            MagicMock(stdout="", returncode=0),  # git status --short (clean)
            MagicMock(
                stdout="", returncode=0
            ),  # git diff HEAD --name-status (no changes)
            MagicMock(
                stdout="* abcd123 (HEAD -> main) Initial commit\n", returncode=0
            ),  # git log
        ]

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "## Current Branch" in result
        assert "main" in result
        assert "## Git Status" in result
        assert "Working tree clean" in result
        assert "## Uncommitted Changes (Tracked Files)" in result
        assert "No uncommitted changes to tracked files" in result
        assert "## Recent Commits" in result
        assert "Initial commit" in result

    @patch("subprocess.run")
    def test_successful_git_context_with_changes(self, mock_run, tmp_path):
        """Test successful Git context extraction from a repository with changes."""
        # Mock all subprocess calls for a repository with changes
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            MagicMock(stdout="feature/test\n", returncode=0),  # current branch
            MagicMock(
                stdout=" M src/test.py\n?? new_file.txt\n", returncode=0
            ),  # git status
            MagicMock(
                stdout="M\tsrc/test.py\n", returncode=0
            ),  # git diff HEAD --name-status
            MagicMock(
                stdout="* abcd123 (HEAD -> feature/test) Add new feature\n* efgh456 Initial commit\n",
                returncode=0,
            ),  # git log
        ]

        result = git_provider.get_git_context(tmp_path, log_count=2)

        assert "# Git Context" in result
        assert "## Current Branch" in result
        assert "feature/test" in result
        assert "## Git Status" in result
        assert "M src/test.py" in result
        assert "?? new_file.txt" in result
        assert "## Uncommitted Changes (Tracked Files)" in result
        assert "M\tsrc/test.py" in result
        assert "## Recent Commits" in result
        assert "Add new feature" in result
        assert "Initial commit" in result

    @patch("subprocess.run")
    def test_git_context_with_full_diff(self, mock_run, tmp_path):
        """Test Git context extraction with full diff enabled."""
        # Mock subprocess calls including full diff
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            MagicMock(stdout="main\n", returncode=0),  # current branch
            MagicMock(stdout=" M src/test.py\n", returncode=0),  # git status
            MagicMock(
                stdout="M\tsrc/test.py\n", returncode=0
            ),  # git diff HEAD --name-status
            MagicMock(
                stdout="* abcd123 (HEAD -> main) Test commit\n", returncode=0
            ),  # git log
            MagicMock(
                stdout="diff --git a/src/test.py b/src/test.py\n+added line\n",
                returncode=0,
            ),  # full diff
        ]

        result = git_provider.get_git_context(tmp_path, full_diff=True)

        assert "# Git Context" in result
        assert "## Full Diff" in result
        assert "diff --git" in result
        assert "+added line" in result

    @patch("subprocess.run")
    def test_git_context_with_diff_options(self, mock_run, tmp_path):
        """Test Git context extraction with custom diff options."""
        # Mock subprocess calls including custom diff options
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            MagicMock(stdout="main\n", returncode=0),  # current branch
            MagicMock(stdout=" M src/test.py\n", returncode=0),  # git status
            MagicMock(
                stdout="M\tsrc/test.py\n", returncode=0
            ),  # git diff HEAD --name-status
            MagicMock(
                stdout="* abcd123 (HEAD -> main) Test commit\n", returncode=0
            ),  # git log
            MagicMock(
                stdout="src/test.py | 1 +\n 1 file changed, 1 insertion(+)\n",
                returncode=0,
            ),  # diff with --stat
        ]

        result = git_provider.get_git_context(tmp_path, diff_options="--stat")

        assert "# Git Context" in result
        assert "## Diff (--stat)" in result
        assert "1 file changed" in result
        assert "1 insertion" in result

    @patch("subprocess.run")
    def test_git_command_error_handling(self, mock_run, tmp_path):
        """Test error handling for individual Git command failures."""
        # Mock scenario where git repo check succeeds but branch command fails
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            subprocess.CalledProcessError(
                128,
                "git rev-parse --abbrev-ref HEAD",
                stderr="fatal: not a git repository",
            ),  # branch command fails
            MagicMock(stdout="", returncode=0),  # git status still works
            MagicMock(stdout="", returncode=0),  # git diff still works
            MagicMock(stdout="", returncode=0),  # git log still works
        ]

        result = git_provider.get_git_context(tmp_path)

        assert "# Git Context" in result
        assert "## Current Branch" in result
        assert "Error getting current branch" in result
        assert "fatal: not a git repository" in result

    @patch("subprocess.run")
    def test_parameter_validation(self, mock_run, tmp_path):
        """Test parameter validation and different log counts."""
        # Mock successful calls
        mock_run.side_effect = [
            MagicMock(returncode=0),  # git --version
            MagicMock(stdout="true\n", returncode=0),  # is git repo check
            MagicMock(stdout="main\n", returncode=0),  # current branch
            MagicMock(stdout="", returncode=0),  # git status
            MagicMock(stdout="", returncode=0),  # git diff
            MagicMock(
                stdout="* commit1\n* commit2\n* commit3\n", returncode=0
            ),  # git log with 3 commits
        ]

        git_provider.get_git_context(tmp_path, log_count=3)

        # Verify git log was called with correct parameters
        git_log_call = None
        for call in mock_run.call_args_list:
            if call[0][0] and "log" in call[0][0]:
                git_log_call = call
                break

        assert git_log_call is not None
        assert "-n" in git_log_call[0][0]
        assert "3" in git_log_call[0][0]

    def test_integration_with_real_git_repo(self, tmp_path):
        """Integration test with a real Git repository."""
        # This test requires Git to be installed and available
        try:
            # Initialize a real git repo
            subprocess.run(
                ["git", "init"], cwd=tmp_path, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=tmp_path,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True
            )

            # Create and commit a file
            test_file = tmp_path / "test.txt"
            test_file.write_text("Hello World")
            subprocess.run(["git", "add", "test.txt"], cwd=tmp_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"], cwd=tmp_path, check=True
            )

            # Test the git_provider function
            result = git_provider.get_git_context(tmp_path)

            assert "# Git Context" in result
            assert "## Current Branch" in result
            assert "## Git Status" in result
            assert "## Uncommitted Changes (Tracked Files)" in result
            assert "## Recent Commits" in result
            assert "Initial commit" in result

        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip("Git not available for integration test")
