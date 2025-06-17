# tests/tools/test_dependency_lister.py
"""Unit tests for the dependency_lister module.

Tests cover parsing functionality for various package manager files,
error handling, and output formatting.
"""

import json

import pytest

from src.codebrief.tools.dependency_lister import (
    DependencyInfo,
    PackageJsonParser,
    PyProjectTomlParser,
    RequirementsTxtParser,
    create_parser,
    discover_dependency_files,
    format_dependencies_as_markdown,
    list_dependencies,
)


class TestDependencyInfo:
    """Test cases for DependencyInfo class."""

    def test_basic_dependency(self):
        """Test basic dependency creation."""
        dep = DependencyInfo(name="requests", version="^2.31.0", group="main")
        assert dep.name == "requests"
        assert dep.version == "^2.31.0"
        assert dep.group == "main"
        assert dep.extras == []

    def test_dependency_with_extras(self):
        """Test dependency with extras."""
        dep = DependencyInfo(
            name="django", version=">=4.0", extras=["redis", "postgres"], group="main"
        )
        assert dep.name == "django"
        assert dep.version == ">=4.0"
        assert dep.extras == ["redis", "postgres"]
        assert dep.group == "main"

    def test_dependency_string_representation(self):
        """Test string representation of dependencies."""
        # Basic dependency
        dep1 = DependencyInfo(name="requests", version="^2.31.0")
        assert str(dep1) == "requests ^2.31.0"

        # Dependency with extras
        dep2 = DependencyInfo(
            name="django", version=">=4.0", extras=["redis", "postgres"]
        )
        assert str(dep2) == "django[redis,postgres] >=4.0"

        # Dependency without version
        dep3 = DependencyInfo(name="pytest")
        assert str(dep3) == "pytest"

    def test_dependency_repr(self):
        """Test repr of dependency."""
        dep = DependencyInfo(
            name="requests", version="^2.31.0", extras=["security"], group="dev"
        )
        expected = "DependencyInfo(name='requests', version='^2.31.0', extras=['security'], group='dev')"
        assert repr(dep) == expected


class TestPyProjectTomlParser:
    """Test cases for PyProjectTomlParser."""

    def test_poetry_basic_dependencies(self, tmp_path):
        """Test parsing basic Poetry dependencies."""
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"
click = "^8.0.0"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        parser = PyProjectTomlParser(pyproject_file)
        assert parser.can_parse()

        deps = parser.parse()

        # Should have 2 dependencies (python is skipped)
        assert len(deps) == 2

        requests_dep = next(d for d in deps if d.name == "requests")
        assert requests_dep.version == "^2.31.0"
        assert requests_dep.group == "main"

        click_dep = next(d for d in deps if d.name == "click")
        assert click_dep.version == "^8.0.0"
        assert click_dep.group == "main"

    def test_poetry_group_dependencies(self, tmp_path):
        """Test parsing Poetry group dependencies."""
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"

[tool.poetry.group.test.dependencies]
coverage = "^7.0.0"
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        parser = PyProjectTomlParser(pyproject_file)
        deps = parser.parse()

        # Check main dependencies
        main_deps = [d for d in deps if d.group == "main"]
        assert len(main_deps) == 1
        assert main_deps[0].name == "requests"

        # Check dev dependencies
        dev_deps = [d for d in deps if d.group == "dev"]
        assert len(dev_deps) == 2
        dev_names = {d.name for d in dev_deps}
        assert dev_names == {"pytest", "black"}

        # Check test dependencies
        test_deps = [d for d in deps if d.group == "test"]
        assert len(test_deps) == 1
        assert test_deps[0].name == "coverage"

    def test_poetry_complex_dependencies(self, tmp_path):
        """Test parsing complex Poetry dependencies with extras and options."""
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
django = {version = "^4.0", extras = ["redis", "postgres"]}
optional-pkg = {version = "^1.0", optional = true}
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        parser = PyProjectTomlParser(pyproject_file)
        deps = parser.parse()

        django_dep = next(d for d in deps if d.name == "django")
        assert django_dep.version == "^4.0"
        assert django_dep.extras == ["redis", "postgres"]
        assert django_dep.group == "main"

        optional_dep = next(d for d in deps if d.name == "optional-pkg")
        assert optional_dep.version == "^1.0"
        assert optional_dep.group == "optional"

    def test_pep621_dependencies(self, tmp_path):
        """Test parsing PEP 621 dependencies."""
        pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
dependencies = [
    "requests>=2.31.0",
    "click[dev]>=8.0.0",
]

[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "coverage>=7.0.0",
]
dev = [
    "black>=23.0.0",
    "mypy>=1.0.0",
]
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        parser = PyProjectTomlParser(pyproject_file)
        deps = parser.parse()

        # Check main dependencies
        main_deps = [d for d in deps if d.group == "main"]
        assert len(main_deps) == 2

        requests_dep = next(d for d in main_deps if d.name == "requests")
        assert requests_dep.version == ">=2.31.0"
        assert requests_dep.extras == []

        click_dep = next(d for d in main_deps if d.name == "click")
        assert click_dep.version == ">=8.0.0"
        assert click_dep.extras == ["dev"]

        # Check optional dependencies
        test_deps = [d for d in deps if d.group == "test"]
        assert len(test_deps) == 2
        test_names = {d.name for d in test_deps}
        assert test_names == {"pytest", "coverage"}

        dev_deps = [d for d in deps if d.group == "dev"]
        assert len(dev_deps) == 2
        dev_names = {d.name for d in dev_deps}
        assert dev_names == {"black", "mypy"}

    def test_mixed_poetry_pep621(self, tmp_path):
        """Test parsing file with both Poetry and PEP 621 sections."""
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"

[project]
dependencies = [
    "click>=8.0.0",
]
"""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(pyproject_content)

        parser = PyProjectTomlParser(pyproject_file)
        deps = parser.parse()

        # Should have both Poetry and PEP 621 dependencies
        assert len(deps) == 2
        dep_names = {d.name for d in deps}
        assert dep_names == {"requests", "click"}

        # Package manager should indicate mixed format
        assert "Poetry + PEP 621" in parser.package_manager

    def test_nonexistent_file(self, tmp_path):
        """Test behavior with non-existent file."""
        nonexistent_file = tmp_path / "nonexistent.toml"
        parser = PyProjectTomlParser(nonexistent_file)

        assert not parser.can_parse()
        assert parser.parse() == []

    def test_malformed_toml(self, tmp_path):
        """Test behavior with malformed TOML."""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text("invalid toml content [[[")

        parser = PyProjectTomlParser(pyproject_file)
        assert parser.can_parse()  # File exists

        deps = parser.parse()
        assert deps == []  # Should return empty list on parse error


class TestRequirementsTxtParser:
    """Test cases for RequirementsTxtParser."""

    def test_basic_requirements(self, tmp_path):
        """Test parsing basic requirements.txt file."""
        requirements_content = """
# Basic requirements
requests==2.31.0
click>=8.0.0
django~=4.0.0
"""
        requirements_file = tmp_path / "requirements.txt"
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        assert parser.can_parse()

        deps = parser.parse()
        assert len(deps) == 3

        requests_dep = next(d for d in deps if d.name == "requests")
        assert requests_dep.version == "==2.31.0"
        assert requests_dep.group == "main"

        click_dep = next(d for d in deps if d.name == "click")
        assert click_dep.version == ">=8.0.0"

        django_dep = next(d for d in deps if d.name == "django")
        assert django_dep.version == "~=4.0.0"

    def test_requirements_with_extras(self, tmp_path):
        """Test parsing requirements with extras."""
        requirements_content = """
django[redis,postgres]>=4.0.0
requests[security,socks]>=2.31.0
"""
        requirements_file = tmp_path / "requirements.txt"
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        deps = parser.parse()

        django_dep = next(d for d in deps if d.name == "django")
        assert django_dep.extras == ["redis", "postgres"]
        assert django_dep.version == ">=4.0.0"

        requests_dep = next(d for d in deps if d.name == "requests")
        assert requests_dep.extras == ["security", "socks"]
        assert requests_dep.version == ">=2.31.0"

    def test_requirements_with_comments(self, tmp_path):
        """Test parsing requirements with comments and empty lines."""
        requirements_content = """
# This is a comment
requests==2.31.0  # Inline comment

# Another comment

click>=8.0.0
"""
        requirements_file = tmp_path / "requirements.txt"
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        deps = parser.parse()

        assert len(deps) == 2
        dep_names = {d.name for d in deps}
        assert dep_names == {"requests", "click"}

    def test_dev_requirements_file(self, tmp_path):
        """Test parsing dev requirements file."""
        requirements_content = """
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
"""
        requirements_file = tmp_path / "requirements-dev.txt"
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        deps = parser.parse()

        # All dependencies should be in 'dev' group based on filename
        assert all(d.group == "dev" for d in deps)
        assert len(deps) == 3

    @pytest.mark.parametrize(
        ("filename", "expected_group"),
        [
            ("requirements.txt", "main"),
            ("requirements-dev.txt", "dev"),
            ("requirements-test.txt", "test"),
            ("requirements-prod.txt", "production"),
            ("requirements-production.txt", "production"),
        ],
    )
    def test_group_determination_from_filename(
        self, tmp_path, filename, expected_group
    ):
        """Test group determination from various filenames."""
        requirements_content = "requests>=2.31.0\n"
        requirements_file = tmp_path / filename
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        deps = parser.parse()

        assert len(deps) == 1
        assert deps[0].group == expected_group

    def test_skip_requirement_options(self, tmp_path):
        """Test skipping requirement file options like -r, -f, etc."""
        requirements_content = """
-r other-requirements.txt
-f https://example.com/packages
--find-links https://example.com
requests>=2.31.0
-e git+https://github.com/example/repo.git#egg=example
click>=8.0.0
"""
        requirements_file = tmp_path / "requirements.txt"
        requirements_file.write_text(requirements_content)

        parser = RequirementsTxtParser(requirements_file)
        deps = parser.parse()

        # Should only parse actual package requirements
        assert len(deps) == 2
        dep_names = {d.name for d in deps}
        assert dep_names == {"requests", "click"}


class TestPackageJsonParser:
    """Test cases for PackageJsonParser."""

    def test_basic_package_json(self, tmp_path):
        """Test parsing basic package.json file."""
        package_data = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {"express": "^4.18.0", "lodash": "^4.17.21"},
            "devDependencies": {"jest": "^29.0.0", "eslint": "^8.0.0"},
        }

        package_file = tmp_path / "package.json"
        package_file.write_text(json.dumps(package_data, indent=2))

        parser = PackageJsonParser(package_file)
        assert parser.can_parse()

        deps = parser.parse()
        assert len(deps) == 4

        # Check main dependencies
        main_deps = [d for d in deps if d.group == "main"]
        assert len(main_deps) == 2
        main_names = {d.name for d in main_deps}
        assert main_names == {"express", "lodash"}

        # Check dev dependencies
        dev_deps = [d for d in deps if d.group == "dev"]
        assert len(dev_deps) == 2
        dev_names = {d.name for d in dev_deps}
        assert dev_names == {"jest", "eslint"}

    def test_all_dependency_types(self, tmp_path):
        """Test parsing all types of dependencies."""
        package_data = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {"express": "^4.18.0"},
            "devDependencies": {"jest": "^29.0.0"},
            "peerDependencies": {"react": "^18.0.0"},
            "optionalDependencies": {"fsevents": "^2.3.0"},
        }

        package_file = tmp_path / "package.json"
        package_file.write_text(json.dumps(package_data, indent=2))

        parser = PackageJsonParser(package_file)
        deps = parser.parse()

        assert len(deps) == 4

        # Check each dependency group
        groups = {d.group: d.name for d in deps}
        assert groups["main"] == "express"
        assert groups["dev"] == "jest"
        assert groups["peer"] == "react"
        assert groups["optional"] == "fsevents"

    def test_malformed_json(self, tmp_path):
        """Test behavior with malformed JSON."""
        package_file = tmp_path / "package.json"
        package_file.write_text('{"invalid": json}')

        parser = PackageJsonParser(package_file)
        assert parser.can_parse()  # File exists

        deps = parser.parse()
        assert deps == []  # Should return empty list on parse error

    def test_empty_dependencies(self, tmp_path):
        """Test parsing package.json with no dependencies."""
        package_data = {"name": "test-project", "version": "1.0.0"}

        package_file = tmp_path / "package.json"
        package_file.write_text(json.dumps(package_data, indent=2))

        parser = PackageJsonParser(package_file)
        deps = parser.parse()

        assert deps == []


class TestDiscoveryFunctions:
    """Test cases for dependency file discovery functions."""

    def test_discover_dependency_files(self, tmp_path):
        """Test discovering various dependency files."""
        # Create various dependency files
        (tmp_path / "pyproject.toml").write_text("[tool.poetry]\nname = 'test'")
        (tmp_path / "requirements.txt").write_text("requests>=2.0.0")
        (tmp_path / "requirements-dev.txt").write_text("pytest>=7.0.0")
        (tmp_path / "package.json").write_text('{"name": "test"}')

        discovered_files = discover_dependency_files(tmp_path)

        # Should find the 4 supported files we created
        assert len(discovered_files) == 4

        filenames = {f.name for f in discovered_files}
        expected_files = {
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            "package.json",
        }
        assert expected_files == filenames

    def test_discover_no_files(self, tmp_path):
        """Test discovery when no dependency files exist."""
        # Create some non-dependency files
        (tmp_path / "README.md").write_text("# Test Project")
        (tmp_path / "main.py").write_text("print('hello')")

        discovered_files = discover_dependency_files(tmp_path)
        assert discovered_files == []

    @pytest.mark.parametrize(
        ("filename", "parser_class"),
        [
            ("pyproject.toml", PyProjectTomlParser),
            ("requirements.txt", RequirementsTxtParser),
            ("requirements-dev.txt", RequirementsTxtParser),
            ("package.json", PackageJsonParser),
        ],
    )
    def test_create_parser(self, tmp_path, filename, parser_class):
        """Test creating appropriate parser for different files."""
        file_path = tmp_path / filename
        file_path.write_text("dummy content")

        parser = create_parser(file_path)
        assert isinstance(parser, parser_class)

    def test_create_parser_unsupported_file(self, tmp_path):
        """Test creating parser for unsupported file type."""
        file_path = tmp_path / "Gemfile"  # Ruby file - not supported
        file_path.write_text("source 'https://rubygems.org'")

        parser = create_parser(file_path)
        assert parser is None


class TestMarkdownFormatting:
    """Test cases for Markdown formatting functionality."""

    def test_format_empty_dependencies(self):
        """Test formatting empty dependency data."""
        result = format_dependencies_as_markdown({})
        assert "# Project Dependencies" in result
        # Empty data should just show the header

    def test_format_single_language_dependencies(self):
        """Test formatting dependencies for a single language."""
        deps_main = [DependencyInfo("requests", "^2.31.0", group="main")]
        deps_dev = [DependencyInfo("pytest", "^7.0.0", group="dev")]

        dependency_data = {
            "Python": {
                "Poetry": {
                    "main": deps_main,
                    "dev": deps_dev,
                }
            }
        }

        result = format_dependencies_as_markdown(dependency_data)

        assert "# Project Dependencies" in result
        assert "## Python" in result
        assert "### Poetry" in result
        assert "#### Main Dependencies" in result
        assert "#### Dev Dependencies" in result
        assert "requests" in result
        assert "^2.31.0" in result
        assert "pytest" in result
        assert "^7.0.0" in result

    def test_format_multiple_languages(self):
        """Test formatting dependencies for multiple languages."""
        python_deps = [DependencyInfo("requests", "^2.31.0", group="main")]
        nodejs_deps = [DependencyInfo("express", "^4.18.0", group="main")]

        dependency_data = {
            "Python": {"Poetry": {"main": python_deps}},
            "Node.js": {"npm/yarn": {"main": nodejs_deps}},
        }

        result = format_dependencies_as_markdown(dependency_data)

        assert "## Python" in result
        assert "## Node.js" in result
        assert "requests" in result
        assert "express" in result

    def test_format_dependencies_with_extras(self):
        """Test formatting dependencies with extras."""
        deps = [
            DependencyInfo(
                "django", "^4.0.0", extras=["redis", "postgres"], group="main"
            )
        ]

        dependency_data = {"Python": {"Poetry": {"main": deps}}}

        result = format_dependencies_as_markdown(dependency_data)

        assert "django" in result
        assert "^4.0.0" in result

    def test_format_single_group_no_header(self):
        """Test that single dependency groups don't show group headers."""
        deps = [
            DependencyInfo("requests", "^2.31.0", group="main"),
            DependencyInfo("click", "^8.0.0", group="main"),
        ]

        dependency_data = {"Python": {"Poetry": {"main": deps}}}

        result = format_dependencies_as_markdown(dependency_data)

        # Should have group headers even for single groups
        assert "#### Main Dependencies" in result
        assert "requests" in result
        assert "click" in result


class TestMainLogic:
    """Test cases for the main dependency listing logic."""

    def test_list_dependencies_nonexistent_path(self, tmp_path):
        """Test behavior with non-existent project path."""
        nonexistent_path = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError):
            list_dependencies(nonexistent_path, None)

    def test_list_dependencies_file_instead_of_directory(self, tmp_path):
        """Test behavior when project path is a file, not a directory."""
        file_path = tmp_path / "not_a_directory.txt"
        file_path.write_text("I'm a file, not a directory")

        with pytest.raises(FileNotFoundError):
            list_dependencies(file_path, None)

    def test_list_dependencies_no_files(self, tmp_path):
        """Test behavior when no dependency files are found."""
        # Create empty directory
        with pytest.raises(FileNotFoundError):
            list_dependencies(tmp_path, None)

    def test_list_dependencies_to_file(self, tmp_path):
        """Test listing dependencies to an output file."""
        # Create a simple pyproject.toml
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)

        output_file = tmp_path / "dependencies.md"

        list_dependencies(tmp_path, output_file)

        # Check that output file was created
        assert output_file.exists()

        content = output_file.read_text()
        assert "# Project Dependencies" in content
        assert "requests" in content
        assert "^2.31.0" in content

    def test_list_dependencies_to_console(self, tmp_path, capsys):
        """Test listing dependencies to console."""
        # Create a simple package.json
        package_data = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {"express": "^4.18.0"},
        }

        (tmp_path / "package.json").write_text(json.dumps(package_data, indent=2))

        result = list_dependencies(tmp_path, None)

        captured = capsys.readouterr()
        # Function should return markdown string when no output file specified
        assert result is not None
        assert "express" in result
        assert "# Project Dependencies" in result
        # Should still print diagnostic messages to console
        assert "Scanning for dependency files" in captured.out

    def test_list_dependencies_mixed_files(self, tmp_path):
        """Test listing dependencies from multiple file types."""
        # Create pyproject.toml
        pyproject_content = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.31.0"
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)

        # Create package.json
        package_data = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {"express": "^4.18.0"},
        }
        (tmp_path / "package.json").write_text(json.dumps(package_data, indent=2))

        # Create requirements.txt
        (tmp_path / "requirements.txt").write_text("click>=8.0.0\n")

        output_file = tmp_path / "dependencies.md"
        list_dependencies(tmp_path, output_file)

        content = output_file.read_text()

        # Should contain dependencies from all files
        assert "requests" in content
        assert "express" in content
        assert "click" in content

        # Should have both Python and Node.js sections
        assert "## Python" in content
        assert "## Node.js" in content
