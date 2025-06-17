# tests/utils/test_config_manager.py

"""Unit tests for the src.codebrief.config_manager module.

This module tests configuration loading and validation functionality.
"""

import tempfile
import unittest.mock as mock
import warnings
from pathlib import Path
from typing import Any
from unittest.mock import mock_open, patch

import pytest
import toml

from src.codebrief.utils import config_manager

# Default values expected from config_manager if nothing is loaded or section missing

EXPECTED_DEFAULTS = {
    "default_output_filename_tree": None,
    "default_output_filename_flatten": None,
    "default_output_filename_bundle": None,
    "default_output_filename_deps": None,
    "default_output_filename_git_info": None,
    "global_include_patterns": [],
    "global_exclude_patterns": [],
}


def create_pyproject_toml(tmp_path: Path, content: dict[str, Any]) -> Path:
    """Helper to create a pyproject.toml file with specified content using the 'toml' package."""
    pyproject_file = tmp_path / "pyproject.toml"

    # Always use the 'toml' package for writing in tests, as it supports dumps.
    # This assumes 'toml' is a development dependency.
    try:
        pyproject_file.write_text(toml.dumps(content), encoding="utf-8")
    except (
        NameError
    ) as err:  # Should not happen if toml is imported correctly at module level
        raise RuntimeError(
            "The 'toml' package is required for writing TOML in tests but not found."
        ) from err
    except Exception as err:
        raise RuntimeError(
            f"Failed to write TOML content using 'toml' package: {err}"
        ) from err

    return pyproject_file


def test_load_config_pyproject_not_found():
    """Test loading config when pyproject.toml does not exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        config = config_manager.load_config(project_root)
        assert config == EXPECTED_DEFAULTS


def test_load_config_section_not_found():
    """Test loading config when [tool.codebrief] section is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # Create pyproject.toml without the relevant section
        create_pyproject_toml(project_root, {"tool": {"other_tool": {}}})
        config = config_manager.load_config(project_root)
        assert config == EXPECTED_DEFAULTS


def test_load_config_empty_section():
    """Test loading config when [tool.codebrief] section is empty."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: {}}}
        )
        config = config_manager.load_config(project_root)
        assert config == EXPECTED_DEFAULTS


def test_load_config_all_values_present_and_correct_type():
    """Test loading a valid config with all options correctly typed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        config_data = {
            "default_output_filename_tree": "tree.txt",
            "default_output_filename_flatten": "flat.md",
            "default_output_filename_bundle": "bundle.md",
            "global_include_patterns": ["*.py", ".md"],
            "global_exclude_patterns": ["*.log", "build/"],
        }
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: config_data}}
        )

        config = config_manager.load_config(project_root)

        # Expected config should include defaults for unspecified keys
        expected_config = EXPECTED_DEFAULTS.copy()
        expected_config.update(config_data)
        assert config == expected_config


def test_load_config_some_values_missing():
    """Test loading config with some options present, others using defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        config_data = {
            "default_output_filename_flatten": "custom_flat.txt",
            "global_include_patterns": ["*.js"],
        }
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: config_data}}
        )

        config = config_manager.load_config(project_root)

        expected_partial_config = EXPECTED_DEFAULTS.copy()
        expected_partial_config.update(config_data)
        assert config == expected_partial_config


def test_load_config_incorrect_type_for_list_option_issues_warning():
    """Test warning and default usage for incorrectly typed list option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # global_include_patterns should be a list, but providing a string
        config_data = {"global_include_patterns": "*.py"}
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: config_data}}
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter(
                "always"
            )  # Cause all warnings to always be triggered.
            config = config_manager.load_config(project_root)

            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Expected list for 'global_include_patterns'" in str(w[-1].message)

        # Should use default for the mistyped key
        assert (
            config["global_include_patterns"]
            == EXPECTED_DEFAULTS["global_include_patterns"]
        )  # which is []


def test_load_config_incorrect_type_for_string_option_issues_warning():
    """Test warning and default usage for incorrectly typed string option."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # default_output_filename_tree should be string or None, providing int
        config_data = {"default_output_filename_tree": 123}
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: config_data}}
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            config = config_manager.load_config(project_root)

            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Expected string or None for 'default_output_filename_tree'" in str(
                w[-1].message
            ) or "Expected str for 'default_output_filename_tree'" in str(
                w[-1].message
            )  # Older logic output

        # Should use default for the mistyped key
        assert (
            config["default_output_filename_tree"]
            == EXPECTED_DEFAULTS["default_output_filename_tree"]
        )  # which is None


def test_load_config_unknown_option_is_ignored():
    """Test that unknown options in the config section are ignored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        config_data = {
            "default_output_filename_tree": "tree.txt",
            "unknown_option": "some_value",  # This should be ignored
        }
        create_pyproject_toml(
            project_root, {"tool": {config_manager.CONFIG_SECTION_NAME: config_data}}
        )

        config = config_manager.load_config(project_root)

        expected_known_config = EXPECTED_DEFAULTS.copy()
        expected_known_config["default_output_filename_tree"] = "tree.txt"

        assert config == expected_known_config
        assert "unknown_option" not in config


@mock.patch("pathlib.Path.open")  # Use a more specific mock target from unittest.mock
def test_load_config_parsing_error_issues_warning(mock_open_method):
    """Test warning and default usage when pyproject.toml parsing fails."""
    # Mock Path.open to simulate a read error or malformed content scenario indirectly
    # A more direct way is to write malformed TOML if the parser raises specific errors
    mock_open_method.side_effect = Exception("Simulated TOML parsing error")

    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # Create a dummy pyproject.toml so Path.is_file() passes, but open() fails
        (project_root / "pyproject.toml").touch()

        with pytest.warns(UserWarning, match="Could not parse config"):
            config = config_manager.load_config(project_root)

        # Should return all defaults
        assert config == EXPECTED_DEFAULTS


def test_load_config_no_codebrief_section():
    """Test loading config when [tool.codebrief] section is missing."""
    project_root = Path("test_project")
    mock_data = {"tool": {"other_tool": {"setting": "value"}}}

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.open", mock_open()),
        patch(
            "src.codebrief.utils.config_manager._get_toml_loader",
            return_value=lambda f: mock_data,
        ),
    ):
        config = config_manager.load_config(project_root)
        assert config == config_manager.EXPECTED_DEFAULTS


def test_load_config_empty_codebrief_section():
    """Test loading config when [tool.codebrief] section is empty."""
    project_root = Path("test_project")
    mock_data = {
        "tool": {config_manager.CONFIG_SECTION_NAME: {}}
    }  # Empty codebrief section

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.open", mock_open()),
        patch(
            "src.codebrief.utils.config_manager._get_toml_loader",
            return_value=lambda f: mock_data,
        ),
    ):
        config = config_manager.load_config(project_root)
        assert config == config_manager.EXPECTED_DEFAULTS
