# src/contextcraft/__init__.py
"""
ContextCraft: A CLI toolkit for generating comprehensive project context for LLMs.
"""
import importlib.metadata

try:
    # This will try to get the version from the installed package metadata
    __version__ = importlib.metadata.version("contextcraft")
except importlib.metadata.PackageNotFoundError:
    # Fallback for when the package is not installed (e.g., during development directly from source)
    # You might need to adjust this if you have a single source of truth for the version
    # For now, let's assume it can be found or default to a dev version.
    # A more robust way if not installed is to parse pyproject.toml, but that's more complex.
    # For development, often `poetry version` is the source of truth.
    # Let's keep it simple: if not installed, it might error or we can set a placeholder.
    # This path is less critical for --version display via Typer if Typer handles it.
    __version__ = "0.0.0-dev"  # Placeholder if not installed
