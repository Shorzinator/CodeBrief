# src/contextcraft/tools/dependency_lister.py
"""
Dependency Listing Utilities.

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
from typing import Any, Dict, List, Optional, Tuple, cast

import typer
from rich.console import Console
from rich.markdown import Markdown

# Import for TOML parsing
try:
    import tomllib
except ImportError:
    # Fallback for Python < 3.11
    try:
        import toml  # type: ignore
    except ImportError:
        toml = None  # type: ignore

console = Console()


class DependencyInfo:
    """
    Represents information about a single dependency.

    Attributes:
        name: The name of the dependency
        version: The version constraint/specification (optional)
        extras: List of optional extras/features (optional)
        group: Dependency group (e.g., 'dev', 'test', 'main')
    """

    def __init__(self, name: str, version: Optional[str] = None, extras: Optional[List[str]] = None, group: str = "main"):
        self.name = name
        self.version = version
        self.extras = extras or []
        self.group = group

    def __str__(self) -> str:
        """String representation of the dependency."""
        result = self.name
        if self.extras:
            result += f"[{','.join(self.extras)}]"
        if self.version:
            result += f" {self.version}"
        return result

    def __repr__(self) -> str:
        return f"DependencyInfo(name='{self.name}', version='{self.version}', extras={self.extras}, group='{self.group}')"


class PackageManagerParser:
    """Base class for package manager parsers."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.language = "Unknown"
        self.package_manager = "Unknown"

    def can_parse(self) -> bool:
        """Check if this parser can handle the given file."""
        return self.file_path.exists()

    def parse(self) -> List[DependencyInfo]:
        """Parse the file and extract dependency information."""
        raise NotImplementedError("Subclasses must implement parse()")


class PyProjectTomlParser(PackageManagerParser):
    """Parser for Python pyproject.toml files (Poetry and PEP 621)."""

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.language = "Python"
        self.package_manager = "pyproject.toml"

    def can_parse(self) -> bool:
        """Check if this is a valid pyproject.toml file."""
        if not self.file_path.exists():
            return False

        # Check if we have a TOML parser available
        if not tomllib and not toml:
            console.print("[yellow]Warning: No TOML parser available for pyproject.toml parsing[/yellow]")
            return False

        return True

    def _load_toml(self) -> Dict[str, Any]:
        """Load TOML data from file."""
        try:
            if tomllib:
                with self.file_path.open("rb") as f:
                    # Type cast needed for mypy since tomllib.load return type might be Any
                    return cast(Dict[str, Any], tomllib.load(f))
            elif toml:
                with self.file_path.open("r", encoding="utf-8") as f:
                    # Type cast needed for mypy since toml.load return type is Any
                    return cast(Dict[str, Any], toml.load(f))
            else:
                raise RuntimeError("No TOML parser available")
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to parse {self.file_path}: {e}[/yellow]")
            return {}

    def _parse_poetry_dependencies(self, data: Dict[str, Any]) -> List[DependencyInfo]:
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
                deps.append(DependencyInfo(name=name, version=version, extras=extras, group=group))

        # Group dependencies (e.g., dev, test)
        groups = data.get("tool", {}).get("poetry", {}).get("group", {})
        for group_name, group_data in groups.items():
            group_deps = group_data.get("dependencies", {})
            for name, spec in group_deps.items():
                if isinstance(spec, str):
                    deps.append(DependencyInfo(name=name, version=spec, group=group_name))
                elif isinstance(spec, dict):
                    version = spec.get("version")
                    extras = spec.get("extras", [])
                    deps.append(DependencyInfo(name=name, version=version, extras=extras, group=group_name))

        return deps

    def _parse_pep621_dependencies(self, data: Dict[str, Any]) -> List[DependencyInfo]:
        """Parse PEP 621 style dependencies."""
        deps = []

        # Main dependencies
        project_deps = data.get("project", {}).get("dependencies", [])
        for dep_spec in project_deps:
            if isinstance(dep_spec, str):
                name, version, extras = self._parse_requirement_string(dep_spec)
                deps.append(DependencyInfo(name=name, version=version, extras=extras, group="main"))

        # Optional dependencies
        optional_deps = data.get("project", {}).get("optional-dependencies", {})
        for group_name, group_deps in optional_deps.items():
            for dep_spec in group_deps:
                if isinstance(dep_spec, str):
                    name, version, extras = self._parse_requirement_string(dep_spec)
                    deps.append(DependencyInfo(name=name, version=version, extras=extras, group=group_name))

        return deps

    def _parse_requirement_string(self, req_string: str) -> Tuple[str, Optional[str], List[str]]:
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

    def parse(self) -> List[DependencyInfo]:
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
        super().__init__(file_path)
        self.language = "Python"
        self.package_manager = f"requirements.txt ({file_path.name})"

    def parse(self) -> List[DependencyInfo]:
        """Parse requirements.txt file."""
        if not self.can_parse():
            return []

        deps = []

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Skip -r, -f, --find-links, etc. (requirement file options)
                    if line.startswith("-"):
                        continue

                    # Remove inline comments
                    if "#" in line:
                        line = line.split("#")[0].strip()

                    if line:
                        try:
                            name, version, extras = self._parse_requirement_string(line)
                            # Determine group based on filename
                            group = self._determine_group_from_filename()
                            deps.append(DependencyInfo(name=name, version=version, extras=extras, group=group))
                        except Exception as e:
                            console.print(f"[yellow]Warning: Failed to parse line {line_num} in {self.file_path}: {e}[/yellow]")
                            continue

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to read {self.file_path}: {e}[/yellow]")
            return []

        return deps

    def _determine_group_from_filename(self) -> str:
        """Determine dependency group from filename."""
        filename = self.file_path.name.lower()

        if "dev" in filename:
            return "dev"
        elif "test" in filename:
            return "test"
        elif "prod" in filename or "production" in filename:
            return "production"
        else:
            return "main"

    def _parse_requirement_string(self, req_string: str) -> Tuple[str, Optional[str], List[str]]:
        """Parse a requirement string like 'package[extra1,extra2]>=1.0'."""
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


class PackageJsonParser(PackageManagerParser):
    """Parser for Node.js package.json files."""

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.language = "Node.js"
        self.package_manager = "npm/yarn (package.json)"

    def parse(self) -> List[DependencyInfo]:
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
                deps.append(DependencyInfo(name=name, version=version, group="optional"))

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to parse {self.file_path}: {e}[/yellow]")
            return []

        return deps


def discover_dependency_files(project_path: Path) -> List[Path]:
    """
    Discover supported dependency files in the project.

    Args:
        project_path: The root path of the project to scan

    Returns:
        List of discovered dependency files
    """
    dependency_files = []

    # Python files
    pyproject_toml = project_path / "pyproject.toml"
    if pyproject_toml.exists():
        dependency_files.append(pyproject_toml)

    # Requirements files (look for common patterns)
    requirements_patterns = [
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "requirements-prod.txt",
        "requirements/*.txt",
        "requirements/*.in",
    ]

    for pattern in requirements_patterns:
        if "*" in pattern:
            # Handle glob patterns
            for path in project_path.glob(pattern):
                if path.is_file():
                    dependency_files.append(path)
        else:
            req_file = project_path / pattern
            if req_file.exists():
                dependency_files.append(req_file)

    # Node.js files
    package_json = project_path / "package.json"
    if package_json.exists():
        dependency_files.append(package_json)

    return dependency_files


def create_parser(file_path: Path) -> Optional[PackageManagerParser]:
    """
    Create appropriate parser for the given file.

    Args:
        file_path: Path to the dependency file

    Returns:
        Parser instance or None if no suitable parser found
    """
    filename = file_path.name.lower()

    if filename == "pyproject.toml":
        return PyProjectTomlParser(file_path)
    elif filename.endswith((".txt", ".in")) and "requirements" in filename:
        return RequirementsTxtParser(file_path)
    elif filename == "package.json":
        return PackageJsonParser(file_path)

    return None


def format_dependencies_as_markdown(dependency_data: Dict[str, Dict[str, List[DependencyInfo]]]) -> str:
    """
    Format dependency data as structured Markdown.

    Args:
        dependency_data: Nested dict with structure:
            {language: {file_type: [DependencyInfo, ...]}}

    Returns:
        Formatted Markdown string
    """
    if not dependency_data:
        return "# Project Dependencies\n\nNo dependencies found.\n"

    markdown_lines = ["# Project Dependencies\n"]

    for language, files_data in dependency_data.items():
        markdown_lines.append(f"## {language}\n")

        for file_type, dependencies in files_data.items():
            if not dependencies:
                continue

            markdown_lines.append(f"### {file_type}\n")

            # Group dependencies by their group (main, dev, test, etc.)
            grouped_deps: Dict[str, List[DependencyInfo]] = {}
            for dep in dependencies:
                if dep.group not in grouped_deps:
                    grouped_deps[dep.group] = []
                grouped_deps[dep.group].append(dep)

            for group, group_deps in grouped_deps.items():
                if len(grouped_deps) > 1:  # Only show group header if there are multiple groups
                    group_title = group.replace("_", " ").title()
                    markdown_lines.append(f"#### {group_title} Dependencies\n")

                # Sort dependencies alphabetically
                group_deps.sort(key=lambda x: x.name.lower())

                for dep in group_deps:
                    line = f"- **{dep.name}**"
                    if dep.version:
                        line += f" `{dep.version}`"
                    if dep.extras:
                        line += f" (extras: {', '.join(dep.extras)})"
                    markdown_lines.append(line)

                markdown_lines.append("")  # Empty line after each group

    return "\n".join(markdown_lines)


def list_dependencies_logic(project_path: Path, actual_output_path: Optional[Path]) -> None:
    """
    Main logic function for listing project dependencies.

    Args:
        project_path: The root directory of the project to analyze
        actual_output_path: Optional path to save the output. If None, prints to console.

    Raises:
        typer.Exit: If project path is invalid or other critical errors occur
    """
    if not project_path.exists():
        console.print(f"[bold red]Error: Project path '{project_path}' does not exist.[/bold red]")
        raise typer.Exit(code=1)

    if not project_path.is_dir():
        console.print(f"[bold red]Error: Project path '{project_path}' is not a directory.[/bold red]")
        raise typer.Exit(code=1)

    # Discover dependency files
    dependency_files = discover_dependency_files(project_path)

    if not dependency_files:
        message = f"No supported dependency files found in '{project_path}'"
        if actual_output_path:
            console.print(f"[yellow]{message}[/yellow]")
        else:
            console.print(message)
        return

    if actual_output_path:
        console.print(f"[dim]Analyzing dependencies in '{project_path.resolve()}'...[/dim]")
        console.print(f"[dim]Found {len(dependency_files)} dependency file(s)[/dim]")

    # Parse dependencies from all files
    dependency_data: Dict[str, Dict[str, List[DependencyInfo]]] = {}
    total_dependencies = 0

    for file_path in dependency_files:
        parser = create_parser(file_path)
        if not parser:
            console.print(f"[yellow]Warning: No parser available for {file_path}[/yellow]")
            continue

        try:
            dependencies = parser.parse()
            if dependencies:
                language = parser.language
                file_type = parser.package_manager

                if language not in dependency_data:
                    dependency_data[language] = {}

                if file_type not in dependency_data[language]:
                    dependency_data[language][file_type] = []

                dependency_data[language][file_type].extend(dependencies)
                total_dependencies += len(dependencies)

                if actual_output_path:
                    console.print(f"[dim]  - {file_path.name}: {len(dependencies)} dependencies[/dim]")

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to parse {file_path}: {e}[/yellow]")
            continue

    # Format output
    markdown_content = format_dependencies_as_markdown(dependency_data)

    if actual_output_path:
        try:
            actual_output_path.parent.mkdir(parents=True, exist_ok=True)
            with actual_output_path.open("w", encoding="utf-8") as f:
                f.write(markdown_content)
            console.print(f"[green]Successfully listed {total_dependencies} dependencies to '{actual_output_path.resolve()}'[/green]")
        except OSError as e:
            console.print(f"[bold red]Error writing to output file '{actual_output_path}': {e}[/bold red]")
            raise typer.Exit(code=1) from e
    else:
        # Print to console using Rich Markdown rendering
        markdown_obj = Markdown(markdown_content)
        console.print(markdown_obj)
