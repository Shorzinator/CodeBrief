# src/contextcraft/utils/config_manager.py
"""Manages loading and accessing configuration for ContextCraft."""
import warnings
from contextlib import suppress
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    with suppress(ImportError):
        import toml  # type: ignore

from rich.console import Console

console = Console()

CONFIG_SECTION_NAME = "contextcraft"
TOOL_CONFIG_KEY = f"tool.{CONFIG_SECTION_NAME}"

DEFAULT_CONFIG_VALUES: dict[str, Any] = {
    "default_output_filename_tree": None,
    "default_output_filename_flatten": None,
    "default_output_filename_bundle": None,
    "default_output_filename_deps": None,
    "global_include_patterns": [],
    "global_exclude_patterns": [],
}


def _get_toml_loader():
    """Return the appropriate TOML loading function."""
    if "tomllib" in globals():
        return tomllib.load  # type: ignore
    if "toml" in globals():
        return toml.load  # type: ignore
    raise RuntimeError(
        "TOML parser (tomllib or toml) not found. "
        "Install 'toml' if using Python < 3.11."
    )


def load_config(project_root: Path) -> dict[str, Any]:
    """Load config from [tool.contextcraft] in pyproject.toml."""
    pyproject_path = project_root / "pyproject.toml"
    config = DEFAULT_CONFIG_VALUES.copy()
    toml_load = _get_toml_loader()

    if not pyproject_path.is_file():
        return config

    try:
        with pyproject_path.open("rb") as f:
            data = toml_load(f)
        tool_config = data.get("tool", {}).get(CONFIG_SECTION_NAME, {})
        if not tool_config:
            return config

        for key, default_value in DEFAULT_CONFIG_VALUES.items():
            if key in tool_config:
                loaded_value = tool_config[key]
                expected_type = type(default_value)

                is_valid = True
                if default_value is not None:
                    is_valid = isinstance(loaded_value, expected_type)
                elif loaded_value is not None:
                    # If default is None, we assume str or list are acceptable
                    is_valid = isinstance(loaded_value, (str, list))

                if is_valid:
                    config[key] = loaded_value
                else:
                    default_type_name = (
                        "list" if isinstance(default_value, list) else "string or None"
                    )
                    warnings.warn(
                        f"Config Warning: Expected {default_type_name} for '{key}', "
                        f"got {type(loaded_value).__name__}. Using default.",
                        UserWarning,
                        stacklevel=2,
                    )
                    config[key] = default_value

    except Exception as e:
        warnings.warn(
            f"Could not parse config from {pyproject_path}: {e}. " "Using defaults.",
            UserWarning,
            stacklevel=2,
        )
        return DEFAULT_CONFIG_VALUES.copy()

    return config
