# tests/tools/test_tree_generator.py
from pathlib import Path
from typing import Optional
from unittest import mock

import pytest

from src.contextcraft.tools import tree_generator
from src.contextcraft.utils import ignore_handler  # For .llmignore


# You can reuse or adapt the create_project_structure fixture
@pytest.fixture()
def create_project_structure_for_tree(tmp_path: Path):
    # Same as the one in test_flattener, or slightly adapted if needed
    def _create_files(structure: dict[str, Optional[str]]):
        for rel_path_str, content in structure.items():
            full_path = tmp_path / rel_path_str
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if content is not None:
                full_path.write_text(content, encoding="utf-8")
            else:
                full_path.mkdir(exist_ok=True)
        return tmp_path

    return _create_files


def test_tree_output_to_file_basic(create_project_structure_for_tree, snapshot):
    """Test basic tree generation to a file and compare with snapshot."""
    project_root = create_project_structure_for_tree(
        {
            "file1.txt": "content1",
            "dir1/file2.txt": "content2",
            "dir1/subdir/file3.txt": "content3",
            "empty_dir": None,
        }
    )
    output_file = project_root / "tree_output.txt"

    tree_generator.generate_and_output_tree(
        root_dir=project_root, output_file_path=output_file
    )

    assert output_file.exists()
    generated_tree_content = output_file.read_text()

    # Configure snapshot path if needed (usually pytest-snapshot handles it)
    # snapshot.snapshot_dir = Path("tests/tools/snapshots/tree_generator")
    snapshot.assert_match(generated_tree_content, "basic_tree.txt")


def test_tree_with_llmignore(create_project_structure_for_tree, snapshot):
    """Test tree generation with .llmignore file."""
    project_root = create_project_structure_for_tree(
        {
            ignore_handler.LLMIGNORE_FILENAME: "*.log\nbuild/\n!build/important.md",
            "app.py": "",
            "run.log": "",
            "build/artifact.bin": "",
            "build/important.md": "",
            "src/main.py": "",
        }
    )
    output_file = project_root / "tree_output_ignored.txt"

    tree_generator.generate_and_output_tree(
        root_dir=project_root, output_file_path=output_file
    )

    assert output_file.exists()
    generated_tree_content = output_file.read_text()
    snapshot.assert_match(generated_tree_content, "ignored_tree.txt")


def test_tree_console_output_basic(create_project_structure_for_tree, capsys):
    """Test basic tree generation to console."""
    project_root = create_project_structure_for_tree(
        {
            "file1.txt": "content1",
            "dir1/file2.txt": "content2",
        }
    )

    tree_generator.generate_and_output_tree(
        root_dir=project_root,
        output_file_path=None,  # Output to console
    )
    captured = capsys.readouterr()
    stdout = captured.out

    # For Rich output, assertions will be less precise than snapshots.
    # Check for key elements. The exact formatting characters can vary.
    assert project_root.name in stdout  # Root directory name
    assert "file1.txt" in stdout
    assert "dir1" in stdout
    assert "file2.txt" in stdout
    # Check for tree structure elements
    assert "📁" in stdout  # Directory icon
    assert "📄" in stdout  # File icon
    assert "┣━━" in stdout or "┗━━" in stdout  # Tree connectors


def test_tree_console_with_llmignore_negation(
    create_project_structure_for_tree, capsys
):
    """Test console tree with .llmignore including negation."""
    project_root = create_project_structure_for_tree(
        {
            ignore_handler.LLMIGNORE_FILENAME: "build/\n!build/important.md",
            "app.py": "",
            "build/artifact.bin": "",  # Should be ignored by 'build/'
            "build/important.md": "",  # Should be shown due to negation (if simpler Rich logic used, build/ might not show)
        }
    )

    tree_generator.generate_and_output_tree(
        root_dir=project_root,
        output_file_path=None,  # Console output
    )
    captured = capsys.readouterr()
    stdout = captured.out

    print("\nDEBUG CONSOLE OUTPUT (llmignore_negation):\n", stdout)

    assert "app.py" in stdout
    assert (
        "build" not in stdout
    )  # build/ itself is ignored by .llmignore and simpler Rich logic won't show it
    assert "important.md" not in stdout  # Consequently, important.md isn't shown either
    assert "artifact.bin" not in stdout
    assert ".llmignore" in stdout  # Assuming .llmignore is not ignored by itself


@mock.patch("pathlib.Path.iterdir", autospec=True)
def test_tree_permission_error_file_output(
    mock_iterdir, create_project_structure_for_tree, snapshot
):
    """Test tree generation handles PermissionError when writing to file."""
    project_root = create_project_structure_for_tree(
        {"allowed_dir/file.txt": "", "denied_dir/secret.txt": ""}
    )

    # Make iterdir on 'denied_dir' raise PermissionError
    def iterdir_side_effect(self, *args, **kwargs):
        if self.name == "denied_dir":
            raise PermissionError("Test permission denied")
        # For other paths, return an empty list or actual content if needed for other parts of test
        elif self.name == "allowed_dir":
            return iter([self / "file.txt"])
        return iter([])  # Default for other iterdir calls (like on project_root)

    mock_iterdir.side_effect = iterdir_side_effect

    output_file = project_root / "tree_permission_error.txt"
    tree_generator.generate_and_output_tree(
        root_dir=project_root, output_file_path=output_file
    )
    snapshot.assert_match(output_file.read_text(), "tree_permission_error.txt")


@mock.patch("pathlib.Path.iterdir", autospec=True)
def test_tree_permission_error_console_output(
    mock_iterdir, create_project_structure_for_tree, capsys
):
    """Test tree generation handles PermissionError for console output."""
    project_root = create_project_structure_for_tree(
        {
            "allowed_dir/file.txt": "",  # Will create allowed_dir and this file
            "denied_dir/secret.txt": "",  # Will create denied_dir and this file
        }
    )

    # Create the actual files/dirs that the mock will refer to
    # (create_project_structure_for_tree already does this)
    allowed_dir_path = project_root / "allowed_dir"
    denied_dir_path = project_root / "denied_dir"
    allowed_file_path = allowed_dir_path / "file.txt"  # This file exists

    def iterdir_side_effect(self: Path, *args, **kwargs):
        # self is the Path instance on which iterdir is called
        # print(f"DEBUG: mock_iterdir called on: {self.as_posix()}") # Helpful for debugging mock calls

        if self == project_root:  # When iterdir is called on the root
            # Return the top-level directories we created
            return iter([allowed_dir_path, denied_dir_path])
        elif self == allowed_dir_path:
            # Return contents of allowed_dir
            return iter([allowed_file_path])
        elif self == denied_dir_path:
            # This is where we want the permission error
            raise PermissionError("Test permission denied on denied_dir")
        return iter([])  # Default for any other unexpected calls

    mock_iterdir.side_effect = iterdir_side_effect

    tree_generator.generate_and_output_tree(
        root_dir=project_root,
        output_file_path=None,  # Console output
    )
    captured = capsys.readouterr()
    stdout = captured.out

    print(
        f"\nDEBUG STDOUT for permission error console test:\n{stdout}"
    )  # Add this to see actual output

    # Assertions need to be robust to Rich's output.
    # The Rich output for a denied directory looks like:
    # ┣━━ 📁 denied_dir
    # ┃   └── [dim italic](Permission Denied)[/dim italic]
    # Or if denied_dir is last:
    # ┗━━ 📁 denied_dir
    #     └── [dim italic](Permission Denied)[/dim italic]

    assert "allowed_dir" in stdout
    assert "file.txt" in stdout  # Assuming allowed_dir is listed and its contents shown
    assert "denied_dir" in stdout  # The directory name itself should be listed
    # Check for the specific Permission Denied message associated with denied_dir
    # A more robust check might involve parsing the tree structure slightly or using regex
    # For now, let's check if "Permission Denied" appears after "denied_dir" in the output.
    # This is a bit fragile due to Rich's formatting characters.

    # A slightly better check:
    # We expect the denied_dir to be listed, and then the (Permission Denied) message
    # as its child in the Rich Tree representation.
    # Example of how the text might look (stripping Rich markup):
    # test_tree_permission_error_console_output0/
    # ├── allowed_dir/
    # │   └── file.txt
    # └── denied_dir/
    #     (Permission Denied)

    # Let's look for the sequence
    denied_dir_index = stdout.find("denied_dir")
    assert denied_dir_index != -1, "The 'denied_dir' should be listed in the output."

    permission_denied_message_index = stdout.find(
        "(Permission Denied)", denied_dir_index
    )
    assert (
        permission_denied_message_index > denied_dir_index
    ), "'(Permission Denied)' message should appear after 'denied_dir'."

    # Ensure the (Permission Denied) message is "under" denied_dir visually.
    # This often means more leading spaces or specific tree connectors.
    # This part is hard to assert precisely without parsing Rich's output.
    # For now, the above checks are a good start.
    # The most important thing is that the code path for PermissionError in
    # _add_nodes_to_rich_tree_recursive is hit.

    assert "secret.txt" not in stdout  # File inside denied_dir should not be listed


def test_tree_fallback_exclusions_no_llmignore(
    create_project_structure_for_tree, snapshot, monkeypatch
):
    """Test fallback exclusions when no .llmignore file is present."""
    # Temporarily modify DEFAULT_EXCLUDED_ITEMS_TOOL_SPECIFIC for a predictable test
    monkeypatch.setattr(
        tree_generator,
        "DEFAULT_EXCLUDED_ITEMS_TOOL_SPECIFIC",
        {
            "__pycache__",
            "*.log",
            "explicitly_ignored.txt",
        },  # These are names/simple globs
    )

    project_root = create_project_structure_for_tree(
        {
            "main.py": "",
            "app.log": "",  # Should be ignored by *.log in fallback
            "__pycache__/cache.pyc": "",  # Dir __pycache__ should be ignored by fallback
            "explicitly_ignored.txt": "",  # Should be ignored by name
            "keeper.py": "",
        }
    )
    # IMPORTANT: Do NOT create an .llmignore file for this test

    output_file = project_root / "tree_fallback.txt"
    tree_generator.generate_and_output_tree(
        root_dir=project_root,
        output_file_path=output_file,
        # No llmignore_spec is loaded, no CLI ignores are passed
    )

    content = output_file.read_text()
    snapshot.assert_match(content, "tree_fallback.txt")


# TODO:
# - Test console output (capsys, check for key elements)
# - Test CLI --ignore flags
# - Test interaction of .llmignore and CLI --ignore
# - Test DEFAULT_EXCLUDED_ITEMS fallback when no .llmignore
# - Test output file self-exclusion
# - Test permission error handling (mocking Path.iterdir)
