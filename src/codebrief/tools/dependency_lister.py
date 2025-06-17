# src/codebrief/tools/dependency_lister.py
"""Dependency Listing Utilities.

This module provides functions to identify and list project dependencies from various
common package manager files. It supports multiple programming languages and package
managers, outputting structured Markdown suitable for inclusion in context bundles.

Core functionalities:
- Parsing Python dependencies from pyproject.toml (Poetry and PEP 621)
- Parsing Python dependencies from requirements.txt files
- Parsing Node.js dependencies from package.json
- Extensible design for future language/package manager support
- Structured Markdown output with grouping by language/file
- Graceful handling of missing or malformed files
"""

import json
import re
from pathlib import Path
from typing import Any, Optional

import typer
from rich.console import Console

# Import for TOML parsing
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib

console = Console()


class DependencyInfo:
    """Represents information about a single dependency.

    Attributes
    ----------
        name: The name of the dependency
        version: The version constraint/specification (optional)
        extras: List of optional extras/features (optional)
        group: Dependency group (e.g., 'dev', 'test', 'main')

    """

    def __init__(
        self,
        name: str,
        version: Optional[str] = None,
        extras: Optional[list[str]] = None,
        group: str = "main",
    ):
        """Initialize a DependencyInfo object."""
        self.name = name
        self.version = version
        self.extras = extras or []
        self.group = group

    def __str__(self) -> str:
        """Return the string representation of the dependency."""
        result = self.name
        if self.extras:
            result += f"[{','.join(self.extras)}]"
        if self.version:
            result += f" {self.version}"
        return result

    def __repr__(self) -> str:
        """Return the detailed string representation of the object."""
        return (
            f"DependencyInfo(name='{self.name}', version='{self.version}', "
            f"extras={self.extras}, group='{self.group}')"
        )


class PackageManagerParser:
    """Base class for package manager parsers."""

    def __init__(self, file_path: Path):
        """Initialize the parser with a file path."""
        self.file_path = file_path
        self.language = "Unknown"
        self.package_manager = "Unknown"

    def can_parse(self) -> bool:
        """Check if this parser can handle the given file."""
        return self.file_path.exists()

    def parse(self) -> list[DependencyInfo]:
        """Parse the file and extract dependency information."""
        raise NotImplementedError("Subclasses must implement parse()")


class PyProjectTomlParser(PackageManagerParser):
    """Parser for Python pyproject.toml files (Poetry and PEP 621)."""

    def __init__(self, file_path: Path):
        """Initialize the pyproject.toml parser."""
        super().__init__(file_path)
        self.language = "Python"
        self.package_manager = "pyproject.toml"

    def can_parse(self) -> bool:
        """Check if this is a valid pyproject.toml file."""
        if not self.file_path.exists():
            return False

        # Check if we have a TOML parser available
        if not tomllib:
            console.print(
                "[yellow]Warning: No TOML parser available for "
                "pyproject.toml parsing[/yellow]"
            )
            return False

        return True

    def _load_toml(self) -> dict[str, Any]:
        """Load TOML data from file."""
        try:
            with self.file_path.open("rb") as f:
                return tomllib.load(f)  # type: ignore[no-any-return]
        except Exception as e:
            console.print(
                f"[yellow]Warning: Failed to load TOML file {self.file_path}: {e}[/yellow]"
            )
            return {}

    def _parse_poetry_dependencies(self, data: dict[str, Any]) -> list[DependencyInfo]:
        """Parse Poetry-style dependencies."""
        deps = []

        # Main dependencies
        poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        for name, spec in poetry_deps.items():
            if name == "python":  # Skip Python version constraint
                continue

            if isinstance(spec, str):
                deps.append(DependencyInfo(name=name, version=spec, group="main"))
            elif isinstance(spec, dict):
                version = spec.get("version")
                extras = spec.get("extras", [])
                optional = spec.get("optional", False)
                group = "optional" if optional else "main"
                deps.append(
                    DependencyInfo(
                        name=name, version=version, extras=extras, group=group
                    )
                )

        # Group dependencies (e.g., dev, test)
        groups = data.get("tool", {}).get("poetry", {}).get("group", {})
        for group_name, group_data in groups.items():
            group_deps = group_data.get("dependencies", {})
            for name, spec in group_deps.items():
                if isinstance(spec, str):
                    deps.append(
                        DependencyInfo(name=name, version=spec, group=group_name)
                    )
                elif isinstance(spec, dict):
                    version = spec.get("version")
                    extras = spec.get("extras", [])
                    deps.append(
                        DependencyInfo(
                            name=name, version=version, extras=extras, group=group_name
                        )
                    )

        return deps

    def _parse_pep621_dependencies(self, data: dict[str, Any]) -> list[DependencyInfo]:
        """Parse PEP 621 style dependencies."""
        deps = []

        # Main dependencies
        project_deps = data.get("project", {}).get("dependencies", [])
        for dep_spec in project_deps:
            if isinstance(dep_spec, str):
                name, version, extras = self._parse_requirement_string(dep_spec)
                deps.append(
                    DependencyInfo(
                        name=name, version=version, extras=extras, group="main"
                    )
                )

        # Optional dependencies
        optional_deps = data.get("project", {}).get("optional-dependencies", {})
        for group_name, group_deps in optional_deps.items():
            for dep_spec in group_deps:
                if isinstance(dep_spec, str):
                    name, version, extras = self._parse_requirement_string(dep_spec)
                    deps.append(
                        DependencyInfo(
                            name=name, version=version, extras=extras, group=group_name
                        )
                    )

        return deps

    def _parse_requirement_string(
        self, req_string: str
    ) -> tuple[str, Optional[str], list[str]]:
        """Parse a requirement string like 'package[extra1,extra2]>=1.0'."""
        # This is a simplified parser - a full implementation would use packaging.requirements
        req_string = req_string.strip()

        # Extract extras
        extras = []
        extras_match = re.search(r"\[([^\]]+)\]", req_string)
        if extras_match:
            extras = [e.strip() for e in extras_match.group(1).split(",")]
            req_string = req_string.replace(extras_match.group(0), "")

        # Extract version constraint
        version_match = re.search(r"([<>=!~]+.+)", req_string)
        version = version_match.group(1) if version_match else None

        # Extract package name
        name = re.sub(r"[<>=!~].*", "", req_string).strip()

        return name, version, extras

    def parse(self) -> list[DependencyInfo]:
        """Parse pyproject.toml file."""
        if not self.can_parse():
            return []

        data = self._load_toml()
        if not data:
            return []

        deps = []

        # Try Poetry format first
        if "tool" in data and "poetry" in data["tool"]:
            self.package_manager = "Poetry (pyproject.toml)"
            deps.extend(self._parse_poetry_dependencies(data))

        # Try PEP 621 format
        if "project" in data:
            if deps:  # If we already found Poetry deps, this might be a mixed file
                self.package_manager = "Poetry + PEP 621 (pyproject.toml)"
            else:
                self.package_manager = "PEP 621 (pyproject.toml)"
            deps.extend(self._parse_pep621_dependencies(data))

        return deps


class RequirementsTxtParser(PackageManagerParser):
    """Parser for Python requirements.txt files."""

    def __init__(self, file_path: Path):
        """Initialize the requirements.txt parser."""
        super().__init__(file_path)
        self.language = "Python"
        self.package_manager = f"requirements.txt ({file_path.name})"

    def parse(self) -> list[DependencyInfo]:
        """Parse requirements.txt file."""
        if not self.can_parse():
            return []

        deps = []
        group = self._determine_group_from_filename()
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("-"):
                        continue
                    name, version, extras = self._parse_requirement_string(line)
                    deps.append(
                        DependencyInfo(
                            name=name, version=version, extras=extras, group=group
                        )
                    )
        except Exception as e:
            console.print(
                f"[yellow]Warning: Failed to parse {self.file_path}: {e}[/yellow]"
            )

        return deps

    def _determine_group_from_filename(self) -> str:
        """Determine dependency group based on filename conventions."""
        name = self.file_path.name.lower()
        if "dev" in name:
            return "dev"
        if "test" in name:
            return "test"
        if "prod" in name or "production" in name:
            return "production"
        return "main"

    def _parse_requirement_string(
        self, req_string: str
    ) -> tuple[str, Optional[str], list[str]]:
        """Parse a requirement string like 'package[extra]>=1.0'."""
        req_string = req_string.strip().split("#")[0].strip()
        extras = []
        extras_match = re.search(r"\[([^\]]+)\]", req_string)
        if extras_match:
            extras = [e.strip() for e in extras_match.group(1).split(",")]
            req_string = req_string.replace(extras_match.group(0), "")

        version_match = re.search(r"([<>=!~]=.+)", req_string)
        version = version_match.group(1) if version_match else None
        name = re.sub(r"[<>=!~]=.*", "", req_string).strip()

        return name, version, extras


class PackageJsonParser(PackageManagerParser):
    """Parser for Node.js package.json files."""

    def __init__(self, file_path: Path):
        """Initialize the package.json parser."""
        super().__init__(file_path)
        self.language = "Node.js"
        self.package_manager = "npm/yarn (package.json)"

    def parse(self) -> list[DependencyInfo]:
        """Parse package.json file."""
        if not self.can_parse():
            return []

        deps = []
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            # Parse main dependencies
            dependencies = data.get("dependencies", {})
            for name, version in dependencies.items():
                deps.append(DependencyInfo(name=name, version=version, group="main"))

            # Parse dev dependencies
            dev_dependencies = data.get("devDependencies", {})
            for name, version in dev_dependencies.items():
                deps.append(DependencyInfo(name=name, version=version, group="dev"))

            # Parse peer dependencies
            peer_dependencies = data.get("peerDependencies", {})
            for name, version in peer_dependencies.items():
                deps.append(DependencyInfo(name=name, version=version, group="peer"))

            # Parse optional dependencies
            optional_dependencies = data.get("optionalDependencies", {})
            for name, version in optional_dependencies.items():
                deps.append(
                    DependencyInfo(name=name, version=version, group="optional")
                )

        except Exception as e:
            console.print(
                f"[yellow]Warning: Failed to parse {self.file_path}: {e}[/yellow]"
            )
            return []

        return deps


def discover_dependency_files(project_path: Path) -> list[Path]:
    """Discover all supported dependency files in the project."""
    supported_files = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "dev-requirements.txt",
        "requirements_dev.txt",
        "test-requirements.txt",
        "requirements-test.txt",
        "requirements_test.txt",
        "package.json",
    ]
    found_files = []
    for p in project_path.rglob("*"):
        if p.name in supported_files:
            # Exclude files in common virtual environment folders
            if ".venv" not in p.parts and "venv" not in p.parts:
                found_files.append(p)
    return found_files


def create_parser(file_path: Path) -> Optional[PackageManagerParser]:
    """Create a parser instance for a given file path."""
    name = file_path.name
    if name == "pyproject.toml":
        return PyProjectTomlParser(file_path)
    if name.endswith(".txt") and "requirements" in name:
        return RequirementsTxtParser(file_path)
    if name == "package.json":
        return PackageJsonParser(file_path)
    return None


def format_dependencies_as_markdown(
    dependency_data: dict[str, dict[str, dict[str, list[DependencyInfo]]]],
) -> str:
    """Format the collected dependency data into a Markdown string."""
    md_content = ["# Project Dependencies"]
    for lang, managers in sorted(dependency_data.items()):
        md_content.append(f"\n## {lang}\n")
        for manager, groups in sorted(managers.items()):
            md_content.append(f"### {manager}\n")
            for group, deps in sorted(groups.items()):
                if deps:
                    md_content.append(f"#### {group.capitalize()} Dependencies\n")
                    for dep in sorted(deps, key=lambda d: d.name):
                        md_content.append(f"- `{dep}`")
                    md_content.append("")
    return "\n".join(md_content)


def list_dependencies(project_path: Path, output_file: Optional[Path]) -> Optional[str]:
    """Main logic function for listing project dependencies.

    Args:
        project_path: Root directory to scan for dependency files.
        output_file: Optional path to save the output. If None, returns string.

    Returns:
        Markdown string if no output file specified, None otherwise.
    """
    console.print(f"Scanning for dependency files in: {project_path}")
    files_to_parse = discover_dependency_files(project_path)

    if not files_to_parse:
        raise FileNotFoundError("No supported dependency files found in the project.")

    all_deps: dict[str, dict[str, dict[str, list[DependencyInfo]]]] = {}

    for file_path in files_to_parse:
        parser = create_parser(file_path)
        if parser and parser.can_parse():
            console.print(
                f"  -> Parsing [green]{file_path.relative_to(project_path)}[/green]..."
            )
            deps = parser.parse()
            if not deps:
                continue

            lang = parser.language
            manager = parser.package_manager
            if lang not in all_deps:
                all_deps[lang] = {}
            if manager not in all_deps[lang]:
                all_deps[lang][manager] = {}

            for dep in deps:
                if dep.group not in all_deps[lang][manager]:
                    all_deps[lang][manager][dep.group] = []
                all_deps[lang][manager][dep.group].append(dep)

    # Reformat the dictionary for the markdown formatter
    # The all_deps structure is: lang -> manager -> group -> list[DependencyInfo]
    # We need to pass this directly to format_dependencies_as_markdown
    markdown_output = format_dependencies_as_markdown(all_deps)

    if output_file:
        try:
            output_file.write_text(markdown_output, encoding="utf-8")
            console.print(
                f"\n[bold green]✓ Dependencies saved to {output_file}[/bold green]"
            )
        except Exception as e:
            console.print(f"[bold red]Error saving to {output_file}: {e}[/bold red]")
            raise typer.Exit(code=1)
        return None
    else:
        # Return the markdown output for the main command to handle
        return markdown_output
