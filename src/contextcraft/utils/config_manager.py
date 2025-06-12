# src/contextcraft/utils/config_manager.py
"""
Manages loading and accessing configuration for ContextCraft from pyproject.toml.
"""
import warnings  # For warning about invalid config values
from contextlib import suppress
from pathlib import Path
from typing import Any, Dict

# Try to import tomllib (Python 3.11+) and fall back to toml package
try:
    import tomllib
except ImportError:
    # If tomllib is not available (Python < 3.11), try to import the toml package.
    # This assumes 'toml' has been added as a dependency via Poetry.
    with suppress(ImportError):
        import toml  # type: ignore

from rich.console import Console

console = Console()

CONFIG_SECTION_NAME = "contextcraft"
TOOL_CONFIG_KEY = f"tool.{CONFIG_SECTION_NAME}"

# Define default values for all known configuration keys
DEFAULT_CONFIG_VALUES: Dict[str, Any] = {
    "default_output_filename_tree": None,
    "default_output_filename_flatten": None,
    "default_output_filename_bundle": None,
    "default_output_filename_deps": None,
    "global_include_patterns": [],  # Default to empty list
    "global_exclude_patterns": [],  # Default to empty list
}


def _get_toml_loader():
    """Returns the appropriate TOML loading function."""
    if "tomllib" in globals():
        return tomllib.load  # type: ignore
    elif "toml" in globals():
        return toml.load  # type: ignore
    else:
        # This should ideally not be reached if Poetry dependencies are set up.
        # Or, if supporting only Py 3.11+, then `toml` isn't needed.
        raise RuntimeError("TOML parser (tomllib or toml package) not found. Please install 'toml' package if using Python < 3.11.")


def load_config(project_root: Path) -> Dict[str, Any]:
    """
    Loads ContextCraft configuration from the [tool.contextcraft] section
    of a pyproject.toml file located in the project_root.

    Args:
        project_root: The root directory of the project where pyproject.toml is expected.

    Returns:
        A dictionary containing the configuration values. If pyproject.toml
        is not found, or the [tool.contextcraft] section is missing, or options
        are missing, appropriate defaults are returned.
    """
    pyproject_path = project_root / "pyproject.toml"
    config_values = DEFAULT_CONFIG_VALUES.copy()  # Start with defaults

    toml_load_func = _get_toml_loader()

    if pyproject_path.is_file():
        try:
            with pyproject_path.open("rb") as f:  # Open in binary mode for tomllib/toml
                data = toml_load_func(f)

            tool_config = data.get("tool", {}).get(CONFIG_SECTION_NAME, {})

            if tool_config:  # If [tool.contextcraft] section exists
                for key, default_value in DEFAULT_CONFIG_VALUES.items():
                    if key in tool_config:
                        loaded_value = tool_config[key]
                        expected_type = type(default_value)

                        # Basic type validation (can be expanded)
                        if default_value is not None and not isinstance(loaded_value, expected_type):
                            if isinstance(default_value, list) and not isinstance(loaded_value, list):
                                warnings.warn(
                                    f"Config Warning: Expected list for '{key}' in [tool.contextcraft], "
                                    f"got {type(loaded_value).__name__}. Using default.",
                                    UserWarning,
                                    stacklevel=2,
                                )
                                config_values[key] = default_value  # Fallback to default
                            elif not isinstance(default_value, list) and expected_type != type(None):  # for Optional[str] etc.
                                warnings.warn(
                                    f"Config Warning: Expected {expected_type.__name__} for '{key}' in [tool.contextcraft], "
                                    f"got {type(loaded_value).__name__}. Using default.",
                                    UserWarning,
                                    stacklevel=2,
                                )
                                config_values[key] = default_value  # Fallback to default
                            else:  # Type matches or default was None (so any type is okay for loaded_value if key exists)
                                config_values[key] = loaded_value
                        elif default_value is None and loaded_value is not None:  # e.g. default_output_filename_tree can be None or str
                            if not isinstance(loaded_value, str):  # Assuming these should be strings if not None
                                warnings.warn(
                                    f"Config Warning: Expected string or None for '{key}' in [tool.contextcraft], "
                                    f"got {type(loaded_value).__name__}. Using default (None).",
                                    UserWarning,
                                    stacklevel=2,
                                )
                                config_values[key] = None  # Fallback to None
                            else:
                                config_values[key] = loaded_value
                        else:  # Type matches or default_value is None and loaded_value is None
                            config_values[key] = loaded_value
                    # If key not in tool_config, it keeps the default value from DEFAULT_CONFIG_VALUES
            # else:
            # console.print(f"[dim]No [tool.contextcraft] section found in {pyproject_path}. Using default configuration.[/dim]")
        except Exception as e:  # Catch errors during parsing or file reading
            console.print(f"[yellow]Warning: Could not load or parse configuration from {pyproject_path}: {e}. Using default configuration.[/yellow]")
            # Ensure config_values remains as defaults
            config_values = DEFAULT_CONFIG_VALUES.copy()
    # else:
    # console.print(f"[dim]No pyproject.toml found in {project_root}. Using default configuration.[/dim]")

    return config_values
