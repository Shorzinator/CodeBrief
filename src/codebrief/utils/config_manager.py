# src/codebrief/utils/config_manager.py
"""Configuration management utilities."""

import warnings
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib

# Constants for backward compatibility with tests
CONFIG_SECTION_NAME = "codebrief"

# Default configuration values
EXPECTED_DEFAULTS: Dict[str, Any] = {
    "default_output_filename_tree": None,
    "default_output_filename_flatten": None,
    "default_output_filename_bundle": None,
    "default_output_filename_deps": None,
    "default_output_filename_git_info": None,
    "global_include_patterns": [],
    "global_exclude_patterns": [],
}

console_instance = None
try:
    from rich.console import Console

    console_instance = Console(stderr=True)
except ImportError:
    pass


def _warn_config_load_error(config_path: Path, e: Exception) -> None:
    """Warn about config loading errors."""
    warning_message = f"Could not parse config from {config_path}: {e}"
    warnings.warn(warning_message, UserWarning, stacklevel=3)


def _get_toml_loader() -> Any:
    """Get the appropriate TOML loader function."""
    return tomllib.load


def _validate_and_merge_config(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate configuration values and merge with defaults."""
    result = EXPECTED_DEFAULTS.copy()

    for key, value in raw_config.items():
        if key not in EXPECTED_DEFAULTS:
            # Ignore unknown keys
            continue

        # Validate list types
        if key in ["global_include_patterns", "global_exclude_patterns"]:
            if not isinstance(value, list):
                warnings.warn(
                    f"Expected list for '{key}', got {type(value).__name__}. Using default.",
                    UserWarning,
                    stacklevel=3,
                )
                continue

        # Validate string types (that can be None)
        elif key.startswith("default_output_filename_"):
            if value is not None and not isinstance(value, str):
                warnings.warn(
                    f"Expected string or None for '{key}', got {type(value).__name__}. Using default.",
                    UserWarning,
                    stacklevel=3,
                )
                continue

        result[key] = value

    return result


def load_config(project_root: Path) -> Dict[str, Any]:
    """Load configuration from codebrief.toml or pyproject.toml."""
    config_paths = [
        project_root / "codebrief.toml",
        project_root / "pyproject.toml",
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with config_path.open("rb") as f:
                    data = _get_toml_loader()(f)

                raw_config = {}
                if config_path.name == "pyproject.toml":
                    # Extract codebrief section from pyproject.toml
                    raw_config = data.get("tool", {}).get(CONFIG_SECTION_NAME, {})
                else:
                    # For codebrief.toml, return the whole thing
                    raw_config = data

                return _validate_and_merge_config(raw_config)

            except Exception as e:
                _warn_config_load_error(config_path, e)
                continue

    # No config found or all failed to load - return defaults
    return EXPECTED_DEFAULTS.copy()
