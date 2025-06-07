# tests/tools/test_tree_generator.py
from pathlib import Path
from typing import Dict, Optional

import pytest

from src.contextcraft.tools import tree_generator
from src.contextcraft.utils import ignore_handler  # For .llmignore


# You can reuse or adapt the create_project_structure fixture
@pytest.fixture()
def create_project_structure_for_tree(tmp_path: Path):
    # Same as the one in test_flattener, or slightly adapted if needed
    def _create_files(structure: Dict[str, Optional[str]]):
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
        {"file1.txt": "content1", "dir1/file2.txt": "content2", "dir1/subdir/file3.txt": "content3", "empty_dir": None}
    )
    output_file = project_root / "tree_output.txt"

    tree_generator.generate_and_output_tree(root_dir=project_root, output_file_path=output_file)

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

    tree_generator.generate_and_output_tree(root_dir=project_root, output_file_path=output_file)

    assert output_file.exists()
    generated_tree_content = output_file.read_text()
    snapshot.assert_match(generated_tree_content, "ignored_tree.txt")


# TODO:
# - Test console output (capsys, check for key elements)
# - Test CLI --ignore flags
# - Test interaction of .llmignore and CLI --ignore
# - Test DEFAULT_EXCLUDED_ITEMS fallback when no .llmignore
# - Test output file self-exclusion
# - Test permission error handling (mocking Path.iterdir)
