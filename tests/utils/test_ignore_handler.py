# tests/utils/test_ignore_handler.py
"""Unit tests for the src.codebrief.utils.ignore_handler module.

This module tests the functionality for parsing .llmignore files and matching
paths against ignore patterns using pathspec.
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest

from src.codebrief.utils import ignore_handler


# Helper function to create a temporary .llmignore file
def create_temp_llmignore(temp_dir_path: Path, content: str) -> Path:
    """Create a temporary .llmignore file in the specified directory with the given content."""
    llmignore_file = temp_dir_path / ignore_handler.LLMIGNORE_FILENAME
    llmignore_file.write_text(content, encoding="utf-8")
    return llmignore_file


# --- Tests for load_ignore_patterns ---


def test_load_ignore_patterns_file_not_found():
    """Test that load_ignore_patterns returns None if .llmignore doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is None


def test_load_ignore_patterns_empty_file():
    """Test that load_ignore_patterns returns None for an empty .llmignore file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        create_temp_llmignore(root_dir, "")
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is None


def test_load_ignore_patterns_comments_and_blank_lines_only():
    """Test that load_ignore_patterns returns None if .llmignore only contains comments and blank lines."""
    content = """
    # This is a comment
    \n
    # Another comment
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        create_temp_llmignore(root_dir, content)
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert (
            spec is None
        )  # pathspec itself might return an empty spec, lets checksits behavior


def test_load_ignore_patterns_valid_patterns():
    """Test loading valid patterns from .llmignore."""
    content = "*.log\nbuild/"
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        create_temp_llmignore(root_dir, content)
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is not None
        # Pathspec doesn't directly expose the number of patterns easily in a public API after parsing lines.
        # We can test its behavior by matching known files.
        assert spec.match_file("some.log")
        assert spec.match_file("build/somefile.txt")
        assert not spec.match_file("src/app.py")


# --- Tests for is_path_ignored ---


@pytest.fixture()
def setup_test_directory():
    """Sets up a temporary directory with a predefined structure and .llmignore file.
    Returns the root Path object of this temporary directory.
    """
    with tempfile.TemporaryDirectory(prefix="codebrief_test_") as tmpdir_name:
        root_dir = Path(tmpdir_name)

        # Create .llmignore
        llmignore_content = """
        # Comments
        *.log
        temp_file.txt
        build/
        **/__pycache__/
        secrets/*.key

        # Specific file in a generally ignored directory
        !build/important_file.txt

        # Test negation for a file that would otherwise be included
        docs/
        !docs/README.md
        """
        create_temp_llmignore(root_dir, llmignore_content)

        # Create some files and directories for testing
        (root_dir / "file.py").touch()
        (root_dir / "another.log").touch()
        (root_dir / "temp_file.txt").touch()  # Should be ignored by name

        (root_dir / "build").mkdir()
        (root_dir / "build" / "output.bin").touch()  # Should be ignored (in build/)
        (
            root_dir / "build" / "important_file.txt"
        ).touch()  # Should be included by negation

        (root_dir / "src").mkdir()
        (root_dir / "src" / "app.py").touch()
        (root_dir / "src" / "__pycache__").mkdir()  # Should be ignored by **/
        (root_dir / "src" / "__pycache__" / "cachefile.pyc").touch()

        (root_dir / ".git").mkdir()  # Core system exclusion
        (root_dir / ".git" / "config").touch()

        (root_dir / "secrets").mkdir()
        (root_dir / "secrets" / "api.key").touch()  # Should be ignored
        (root_dir / "secrets" / "other.txt").touch()  # Should NOT be ignored by *.key

        (root_dir / "docs").mkdir()
        (root_dir / "docs" / "index.md").touch()  # Should be ignored by docs/
        (
            root_dir / "docs" / "README.md"
        ).touch()  # Should be included by !docs/README.md

        yield root_dir  # Provide the root_dir to the test


def test_is_path_ignored_core_system_exclusions(setup_test_directory):
    """Test that core system exclusions like .git are always ignored."""
    root_dir = setup_test_directory
    ignore_spec = ignore_handler.load_ignore_patterns(
        root_dir
    )  # Load spec for other tests

    git_dir = root_dir / ".git"
    git_config_file = root_dir / ".git" / "config"

    assert ignore_handler.is_path_ignored(git_dir, root_dir, ignore_spec)
    assert ignore_handler.is_path_ignored(git_config_file, root_dir, ignore_spec)


def test_is_path_ignored_llmignore_patterns(setup_test_directory):
    """Test various patterns from the .llmignore file."""
    root_dir = setup_test_directory
    ignore_spec = ignore_handler.load_ignore_patterns(root_dir)

    # Ignored by *.log
    assert ignore_handler.is_path_ignored(
        root_dir / "another.log", root_dir, ignore_spec
    )
    # Ignored by temp_file.txt
    assert ignore_handler.is_path_ignored(
        root_dir / "temp_file.txt", root_dir, ignore_spec
    )
    # Ignored by build/
    assert ignore_handler.is_path_ignored(
        root_dir / "build" / "output.bin", root_dir, ignore_spec
    )
    assert ignore_handler.is_path_ignored(
        root_dir / "build", root_dir, ignore_spec
    )  # The directory itself
    # Ignored by **/__pycache__/
    assert ignore_handler.is_path_ignored(
        root_dir / "src" / "__pycache__" / "cachefile.pyc", root_dir, ignore_spec
    )
    assert ignore_handler.is_path_ignored(
        root_dir / "src" / "__pycache__", root_dir, ignore_spec
    )
    # Ignored by secrets/*.key
    assert ignore_handler.is_path_ignored(
        root_dir / "secrets" / "api.key", root_dir, ignore_spec
    )
    # Ignored by docs/
    assert ignore_handler.is_path_ignored(
        root_dir / "docs" / "index.md", root_dir, ignore_spec
    )

    # Not ignored (included or not matching ignore patterns)
    assert not ignore_handler.is_path_ignored(
        root_dir / "file.py", root_dir, ignore_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "src" / "app.py", root_dir, ignore_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "secrets" / "other.txt", root_dir, ignore_spec
    )

    # Test negations
    assert not ignore_handler.is_path_ignored(
        root_dir / "build" / "important_file.txt", root_dir, ignore_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "docs" / "README.md", root_dir, ignore_spec
    )


def test_is_path_ignored_cli_overrides(setup_test_directory):
    """Test interaction with CLI ignore patterns."""
    root_dir = setup_test_directory
    ignore_spec = ignore_handler.load_ignore_patterns(root_dir)

    # File normally included, but ignored by CLI
    cli_ignores_1 = ["file.py"]
    assert ignore_handler.is_path_ignored(
        root_dir / "file.py", root_dir, ignore_spec, cli_ignore_patterns=cli_ignores_1
    )

    # File normally included, but ignored by CLI glob
    cli_ignores_2 = ["src/*"]  # This should match app.py in src
    assert ignore_handler.is_path_ignored(
        root_dir / "src" / "app.py",
        root_dir,
        ignore_spec,
        cli_ignore_patterns=cli_ignores_2,
    )

    # File normally ignored by .llmignore, CLI ignore is redundant but path remains ignored
    cli_ignores_3 = ["another.log"]
    assert ignore_handler.is_path_ignored(
        root_dir / "another.log",
        root_dir,
        ignore_spec,
        cli_ignore_patterns=cli_ignores_3,
    )

    # Directory normally ignored by .llmignore (build/), CLI pattern for something else
    cli_ignores_4 = ["*.tmp"]
    assert ignore_handler.is_path_ignored(
        root_dir / "build" / "output.bin",
        root_dir,
        ignore_spec,
        cli_ignore_patterns=cli_ignores_4,
    )


def test_is_path_ignored_no_llmignore_file(setup_test_directory):
    """Test behavior when no .llmignore file exists, only CLI ignores."""
    root_dir = setup_test_directory
    # Simulate no .llmignore by passing None as ignore_spec

    cli_ignores = ["file.py"]
    assert ignore_handler.is_path_ignored(
        root_dir / "file.py", root_dir, None, cli_ignore_patterns=cli_ignores
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "another.log", root_dir, None, cli_ignore_patterns=cli_ignores
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "src" / "app.py", root_dir, None, cli_ignore_patterns=cli_ignores
    )


def test_is_path_ignored_patterns_with_leading_trailing_spaces(setup_test_directory):
    """Test that patterns with leading/trailing spaces in .llmignore are handled (pathspec usually trims)."""
    root_dir = setup_test_directory
    # Create a new .llmignore with spacey patterns
    llmignore_content_spaces = """
      *.spacedlog
    spaced_dir/
      !  spaced_dir/important.txt
    """
    create_temp_llmignore(
        root_dir, llmignore_content_spaces
    )  # Overwrites fixture's .llmignore

    ignore_spec_spaces = ignore_handler.load_ignore_patterns(root_dir)
    assert ignore_spec_spaces is not None

    (root_dir / "test.spacedlog").touch()
    (root_dir / "spaced_dir").mkdir()
    (root_dir / "spaced_dir" / "somefile.txt").touch()

    print("\nDEBUG FOR SPACED TEST:")
    print(
        f"Patterns in spec: {[p.pattern for p in ignore_spec_spaces.patterns]}"
    )  # See the actual patterns
    path_str_to_test = (
        (root_dir / "spaced_dir" / "important.txt").relative_to(root_dir).as_posix()
    )
    print(f"Path string for match_file: '{path_str_to_test}'")
    print(
        f"ignore_spec_spaces.match_file result: {ignore_spec_spaces.match_file(path_str_to_test)}"
    )

    assert ignore_handler.is_path_ignored(
        root_dir / "test.spacedlog", root_dir, ignore_spec_spaces
    ), "Should ignore file matching pattern with leading/trailing spaces."
    assert ignore_handler.is_path_ignored(
        root_dir / "spaced_dir" / "somefile.txt", root_dir, ignore_spec_spaces
    ), "Should ignore file in directory matching pattern with trailing space and slash."
    assert not ignore_handler.is_path_ignored(
        root_dir / "spaced_dir" / "important.txt", root_dir, ignore_spec_spaces
    ), "Negated pattern with spaces should correctly un-ignore."


# tests/utils/test_ignore_handler.py


def test_is_path_ignored_directory_vs_file_patterns(setup_test_directory):
    """Test differentiation between patterns matching directories (ending with /)
    and patterns that can match either files or directories (no trailing /).
    """
    root_dir = setup_test_directory
    llmignore_content = """
    is_a_dir/  # Pattern specifically for a directory
    is_a_file  # Pattern for a file OR a directory named 'is_a_file'
    """
    # This test creates its own .llmignore, effectively overriding any from setup_test_directory fixture
    # if the fixture also created one (which it does). This is fine for focused testing.
    create_temp_llmignore(root_dir, llmignore_content)
    current_spec = ignore_handler.load_ignore_patterns(root_dir)
    assert current_spec is not None, "Spec should be loaded"

    # --- Setup specific to this test ---
    # For 'is_a_dir/' pattern
    (root_dir / "is_a_dir").mkdir()
    (root_dir / "is_a_dir" / "child_in_is_a_dir.txt").touch()
    (
        root_dir / "is_a_dir_file_variant"
    ).touch()  # A file that starts with "is_a_dir" but isn't the dir

    # For 'is_a_file' pattern (testing against a file)
    (root_dir / "is_a_file").touch()

    # For 'is_a_file' pattern (testing against a directory with the exact same name)
    (root_dir / "is_a_file_as_dir").mkdir()  # Directory named 'is_a_file_as_dir'
    (root_dir / "is_a_file_as_dir" / "child_in_is_a_file_as_dir.txt").touch()

    # Control file/dir (should not be ignored by these patterns)
    (root_dir / "not_ignored.txt").touch()
    (root_dir / "not_ignored_dir").mkdir()

    print("\nDEBUG FOR test_is_path_ignored_directory_vs_file_patterns:")
    print(
        f"Patterns in spec: {[p.pattern for p in current_spec.patterns if p]}"
    )  # Filter out None if any

    # --- Test 'is_a_dir/' pattern (directory-specific pattern) ---
    path_is_a_dir_dir = root_dir / "is_a_dir"
    print(
        f"Testing dir specific pattern ('is_a_dir/') against dir: {path_is_a_dir_dir}, IsDir: {path_is_a_dir_dir.is_dir()}"
    )
    assert ignore_handler.is_path_ignored(
        path_is_a_dir_dir, root_dir, current_spec
    ), "Directory 'is_a_dir' should be ignored by pattern 'is_a_dir/'."
    assert ignore_handler.is_path_ignored(
        root_dir / "is_a_dir" / "child_in_is_a_dir.txt", root_dir, current_spec
    ), "File inside 'is_a_dir' should be ignored due to pattern 'is_a_dir/'."
    assert not ignore_handler.is_path_ignored(
        root_dir / "is_a_dir_file_variant", root_dir, current_spec
    ), "File 'is_a_dir_file_variant' should NOT be ignored by directory pattern 'is_a_dir/'."

    # --- Test 'is_a_file' pattern (file OR directory pattern) ---
    # Test against a file named 'is_a_file'
    path_is_a_file_file = root_dir / "is_a_file"
    print(
        f"Testing file/dir pattern ('is_a_file') against file: {path_is_a_file_file}, IsDir: {path_is_a_file_file.is_dir()}"
    )
    assert ignore_handler.is_path_ignored(
        path_is_a_file_file, root_dir, current_spec
    ), "File 'is_a_file' should be ignored by pattern 'is_a_file'."

    # Test against a directory named 'is_a_file_as_dir' (note: name mismatch with pattern 'is_a_file')
    # This directory should NOT be ignored by the pattern "is_a_file" because the names differ.
    path_is_a_file_as_dir_dir = root_dir / "is_a_file_as_dir"
    print(
        f"Testing file/dir pattern ('is_a_file') against dir: {path_is_a_file_as_dir_dir}, IsDir: {path_is_a_file_as_dir_dir.is_dir()}"
    )
    assert not ignore_handler.is_path_ignored(
        path_is_a_file_as_dir_dir, root_dir, current_spec
    ), "Directory 'is_a_file_as_dir' should NOT be ignored by pattern 'is_a_file' (name mismatch)."
    assert not ignore_handler.is_path_ignored(
        root_dir / "is_a_file_as_dir" / "child_in_is_a_file_as_dir.txt",
        root_dir,
        current_spec,
    ), "File in 'is_a_file_as_dir' should NOT be ignored by pattern 'is_a_file' (name mismatch)."

    # --- Test control paths (should not be ignored) ---
    assert not ignore_handler.is_path_ignored(
        root_dir / "not_ignored.txt", root_dir, current_spec
    ), "Control file 'not_ignored.txt' should not be ignored."
    assert not ignore_handler.is_path_ignored(
        root_dir / "not_ignored_dir", root_dir, current_spec
    ), "Control directory 'not_ignored_dir' should not be ignored."


def test_is_path_ignored_complex_glob_patterns(setup_test_directory):
    """Test more complex glob patterns like '?', '[]', and nested '**'."""
    root_dir = setup_test_directory
    llmignore_content = """
    # Matches 'fileA.txt', 'fileB.txt', etc.
    file?.txt

    # Matches 'image1.png', 'image2.png', ... 'image9.png'
    image[0-9].png

    # Matches any 'config.json' in any subdirectory of 'settings'
    settings/**/config.json

    # Matches 'data.csv' anywhere in the project
    **/data.csv
    """
    create_temp_llmignore(root_dir, llmignore_content)
    current_spec = ignore_handler.load_ignore_patterns(root_dir)
    assert current_spec is not None

    (root_dir / "fileA.txt").touch()
    (root_dir / "fileLong.txt").touch()  # Should not match file?.txt
    (root_dir / "image1.png").touch()
    (root_dir / "image10.png").touch()  # Should not match image[0-9].png

    (root_dir / "settings").mkdir()
    (root_dir / "settings" / "user").mkdir()
    (root_dir / "settings" / "user" / "config.json").touch()
    (root_dir / "settings" / "another_config.json").touch()  # Should not match

    (root_dir / "project_data").mkdir()
    (root_dir / "project_data" / "data.csv").touch()
    (root_dir / "src" / "data.csv").touch()  # Should also be matched by **/data.csv

    # Test 'file?.txt'
    assert ignore_handler.is_path_ignored(
        root_dir / "fileA.txt", root_dir, current_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "fileLong.txt", root_dir, current_spec
    )

    # Test 'image[0-9].png'
    assert ignore_handler.is_path_ignored(
        root_dir / "image1.png", root_dir, current_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "image10.png", root_dir, current_spec
    )

    # Test 'settings/**/config.json'
    assert ignore_handler.is_path_ignored(
        root_dir / "settings" / "user" / "config.json", root_dir, current_spec
    )
    assert not ignore_handler.is_path_ignored(
        root_dir / "settings" / "another_config.json", root_dir, current_spec
    )

    # Test '**/data.csv'
    assert ignore_handler.is_path_ignored(
        root_dir / "project_data" / "data.csv", root_dir, current_spec
    )
    assert ignore_handler.is_path_ignored(
        root_dir / "src" / "data.csv", root_dir, current_spec
    )


def test_is_path_ignored_anchored_patterns(setup_test_directory):
    """Test patterns anchored to the root (e.g., /file.txt in .gitignore syntax)."""
    # Pathspec's GitWildMatchPattern handles this:
    # A pattern with no leading slash can match anywhere.
    # A pattern with a leading slash is anchored to the root of the ignore file's directory.
    root_dir = setup_test_directory
    llmignore_content = """
    /root_file.txt    # Only matches root_file.txt in the root directory
    sub/root_file.txt # Matches root_file.txt inside 'sub' relative to root.
    anywhere.txt      # Matches 'anywhere.txt' in root or any subdirectory
    """
    create_temp_llmignore(root_dir, llmignore_content)
    current_spec = ignore_handler.load_ignore_patterns(root_dir)
    assert current_spec is not None

    (root_dir / "root_file.txt").touch()
    (root_dir / "sub").mkdir()
    (
        root_dir / "sub" / "root_file.txt"
    ).touch()  # This is the one matched by 'sub/root_file.txt'
    (
        root_dir / "sub" / "another_root_file.txt"
    ).touch()  # Not matched by '/root_file.txt'

    (root_dir / "anywhere.txt").touch()
    (root_dir / "sub" / "anywhere.txt").touch()

    print(f"Patterns in spec: {[p.pattern for p in current_spec.patterns]}")
    print(
        f"Direct pathspec match for 'root_file.txt': {current_spec.match_file('root_file.txt')}"
    )
    assert ignore_handler.is_path_ignored(
        root_dir / "root_file.txt", root_dir, current_spec
    ), "Root-anchored pattern should match file in root."

    # Test '/root_file.txt'
    assert ignore_handler.is_path_ignored(
        root_dir / "root_file.txt", root_dir, current_spec
    ), "Root-anchored pattern should match file in root."
    assert not ignore_handler.is_path_ignored(
        root_dir / "sub" / "another_root_file.txt", root_dir, current_spec
    ), "File in subdir should not match root-anchored pattern '/root_file.txt' (different name)."
    # The existing (root_dir / "sub" / "root_file.txt") *is* matched by the pattern "sub/root_file.txt"

    # Test 'sub/root_file.txt'
    assert ignore_handler.is_path_ignored(
        root_dir / "sub" / "root_file.txt", root_dir, current_spec
    ), "Pattern 'sub/root_file.txt' should match specific nested file."

    # Test 'anywhere.txt'
    assert ignore_handler.is_path_ignored(
        root_dir / "anywhere.txt", root_dir, current_spec
    ), "Unanchored pattern should match file in root."
    assert ignore_handler.is_path_ignored(
        root_dir / "sub" / "anywhere.txt", root_dir, current_spec
    ), "Unanchored pattern should match file in subdirectory."


# --- Tests for load_ignore_patterns ---


def test_load_ignore_patterns_whitespace_only_lines():
    """Test .llmignore with lines that are only whitespace after stripping comments."""
    content = "  \n\t\n# comment\n   # another comment"
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        create_temp_llmignore(root_dir, content)
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is None  # Should result in no processed lines


def test_load_ignore_patterns_patterns_become_empty_after_comment_strip():
    """Test patterns that become empty after stripping inline comments."""
    content = " # only comment here \npattern1 # comment \n ! # comment after bang"
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        create_temp_llmignore(root_dir, content)
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is not None
        # 'pattern1' should be loaded. '!' should likely be ignored or result in an empty pattern.
        # Pathspec might just ignore a lone '!' or an empty string after '!'.
        assert spec.match_file("pattern1")
        # Check how a lone "!" or "! " is handled by your parser and pathspec
        # For example, if "!" becomes an empty negation, it might negate everything or nothing.
        # This depends on pathspec's interpretation of `PathSpec.from_lines(['!'])`
        # Most likely, it results in no effective patterns.


@mock.patch(
    "pathlib.Path.open", new_callable=mock.mock_open
)  # Use mock_open for context manager
@mock.patch("pathlib.Path.is_file", return_value=True)  # Ensure is_file returns True
def test_load_ignore_patterns_read_error(mock_is_file, mock_open_method):
    """Test load_ignore_patterns when file reading raises an OSError."""
    mock_open_method.side_effect = OSError("Test read error")  # Make the open call fail
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir)
        # No need to actually create the file if open is mocked to fail
        spec = ignore_handler.load_ignore_patterns(root_dir)
        assert spec is None
        # mock_is_file.assert_called_once() # Optional: check if is_file was called
        # mock_open_method.assert_called_once() # Optional: check if open was called


# --- Additional Tests for is_path_ignored ---


def test_is_path_ignored_path_not_under_root(setup_test_directory):
    """Test is_path_ignored when path_to_check is not under root_dir."""
    # setup_test_directory creates root_dir and an .llmignore inside it
    root_dir_with_spec = setup_test_directory
    ignore_spec = ignore_handler.load_ignore_patterns(root_dir_with_spec)

    # Create a path completely outside the root_dir structure
    with tempfile.TemporaryDirectory() as another_tmpdir:
        outside_path = Path(another_tmpdir) / "some_other_file.txt"
        outside_path.touch()

        # This path should not be ignored by the spec tied to root_dir_with_spec
        assert not ignore_handler.is_path_ignored(
            outside_path, root_dir_with_spec, ignore_spec
        )

        # Test with a core system exclusion name, even if outside root for spec
        git_imposter_dir = Path(another_tmpdir) / ".git"
        git_imposter_dir.mkdir()
        git_imposter_file = git_imposter_dir / "config"
        git_imposter_file.touch()
        assert ignore_handler.is_path_ignored(
            git_imposter_file, root_dir_with_spec, ignore_spec
        ), "Core system exclusion should apply even if path is outside spec root"
        assert ignore_handler.is_path_ignored(
            git_imposter_dir, root_dir_with_spec, ignore_spec
        )


def test_is_path_ignored_various_llmignore_matches(setup_test_directory):
    """Test more specific .llmignore matching scenarios."""
    root_dir = setup_test_directory  # Uses the .llmignore from the fixture
    spec = ignore_handler.load_ignore_patterns(root_dir)
    assert spec is not None

    # Scenario: file that does NOT match any .llmignore pattern
    assert not ignore_handler.is_path_ignored(
        root_dir / "src" / "app.py", root_dir, spec
    )

    # Scenario: Directory ignored, file within it also ignored
    assert ignore_handler.is_path_ignored(
        root_dir / "build" / "output.bin", root_dir, spec
    )

    # Scenario: Directory pattern in .llmignore (`build/`)
    # Test matching the directory itself
    assert ignore_handler.is_path_ignored(root_dir / "build", root_dir, spec)

    # Scenario: File pattern in .llmignore (`*.log`)
    assert ignore_handler.is_path_ignored(root_dir / "another.log", root_dir, spec)


# tests/utils/test_ignore_handler.py


@pytest.mark.parametrize(
    ("cli_pattern", "path_str_to_check", "is_dir_check", "should_ignore_val"),
    [
        # Path A: filename == pattern
        ("exact_file.txt", "exact_file.txt", False, True),
        ("exact_file.txt", "other_exact_file.txt", False, False),
        # Path B: Path(filename).match(pattern)
        ("*.log", "file.log", False, True),
        ("file.*", "file.log", False, True),
        ("*.txt", "file.log", False, False),
        # Path D, E, F: pattern.endswith("/") and path_to_check_abs.is_dir()
        ("dir1/", "dir1", True, True),  # Hits Path E (path_to_match_cli_dir == pattern)
        (
            "dir2/",
            "dir2",
            True,
            True,
        ),  # Hits Path F (current_path_for_cli_match.name + "/" == pattern)
        (
            "dir3/",
            "sub/dir3",
            True,
            True,
        ),  # Hits Path E (relative path 'sub/dir3/' matches 'dir3/' if pattern is simplified or
        # pathspec-like)
        # OR Path G (current_path_for_cli_match.match(pattern)) if pattern="*/dir3/"
        # Current custom logic might need specific pattern for this
        ("dir4/", "dir4_file", False, False),  # Pattern implies dir, path is file
        # Path G: current_path_for_cli_match.match(pattern)
        ("src/app.*", "src/app.py", False, True),
        ("src/app.*", "src/app.js", False, True),
        ("src/utils/*", "src/utils/helper.py", False, True),
        ("src/utils/*", "src/main.py", False, False),  # main.py not in utils
        # Ensure a non-match for Path G
        ("non_matching_glob/*", "src/app.py", False, False),
        # Test a case where relative_path_for_spec is None (path_to_check outside root_dir)
        # This is better handled by a separate test like test_is_path_ignored_cli_path_outside_root
    ],
)
def test_is_path_ignored_cli_pattern_branches(
    cli_pattern: str,
    path_str_to_check: str,
    is_dir_check: bool,
    should_ignore_val: bool,
    setup_test_directory,
):
    root_dir = setup_test_directory  # .llmignore in fixture won't affect these CLI-only tests if path doesn't match it

    full_path_to_check = root_dir / path_str_to_check
    full_path_to_check.parent.mkdir(parents=True, exist_ok=True)
    if is_dir_check:
        full_path_to_check.mkdir(exist_ok=True)
    else:
        if (
            not full_path_to_check.exists()
        ):  # Avoid error if dir was created by parent.mkdir
            full_path_to_check.touch()

    # Test with no .llmignore spec active to isolate CLI pattern effect
    result = ignore_handler.is_path_ignored(
        full_path_to_check, root_dir, None, cli_ignore_patterns=[cli_pattern]
    )
    assert result is should_ignore_val

    assert not ignore_handler.is_path_ignored(
        root_dir / "some_file_not_otherwise_ignored.txt",
        root_dir,
        None,
        cli_ignore_patterns=[],
    )


def test_is_path_ignored_cli_path_outside_root(tmp_path_factory, setup_test_directory):
    root_dir_for_spec = setup_test_directory  # Has an .llmignore
    spec = ignore_handler.load_ignore_patterns(root_dir_for_spec)

    # Path outside the spec's root_dir
    outside_project_root = tmp_path_factory.mktemp("outside_project")
    outside_file = outside_project_root / "external_file.log"
    outside_file.touch()

    # CLI pattern that would match if path was relative
    assert not ignore_handler.is_path_ignored(
        outside_file,
        root_dir_for_spec,
        spec,
        cli_ignore_patterns=["external_project/*.log"],
    )
    # CLI pattern matching only filename should work
    assert ignore_handler.is_path_ignored(
        outside_file, root_dir_for_spec, spec, cli_ignore_patterns=["external_file.log"]
    )
    assert ignore_handler.is_path_ignored(
        outside_file,
        root_dir_for_spec,
        spec,
        cli_ignore_patterns=["*.log"],  # Path(filename).match()
    )


def test_is_path_ignored_cli_empty_list(setup_test_directory):
    root_dir = setup_test_directory
    spec = ignore_handler.load_ignore_patterns(root_dir)  # Use existing spec
    # A file that is definitely NOT ignored by the fixture's .llmignore or core exclusions
    path_to_check = root_dir / "src" / "app.py"
    assert not ignore_handler.is_path_ignored(
        path_to_check, root_dir, spec, cli_ignore_patterns=[]
    )


# Note on Symlinks:
# `pathspec` itself doesn't inherently resolve symlinks before matching; it matches based on the
# path strings given to it. If `path_to_check` is a symlink, `path_to_check.is_dir()` or
# `path_to_check.is_file()` will operate on the target of the symlink.
# The `Path.resolve()` call at the beginning of `is_path_ignored` will resolve symlinks in
# `path_to_check` and `root_dir`. This means matching happens against the canonical path.
# Testing symlink behavior explicitly would require creating symlinks in the temp directory,
# which can be OS-dependent or require specific permissions.
# For now, relying on `Path.resolve()` is a reasonable approach.
