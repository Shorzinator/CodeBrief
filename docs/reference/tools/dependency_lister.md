# Dependency Lister API Reference

::: codebrief.tools.dependency_lister
    handler: python
    options:
        show_root_heading: true
        show_root_full_path: false
        show_category_heading: true
        members_order: source
        heading_level: 2
        group_by_category: true
        show_symbol_type_heading: true
        show_symbol_type_toc: true

## Overview

The dependency lister tool analyzes project dependency files across multiple programming languages and package managers, generating comprehensive dependency reports in Markdown format.

## Supported Languages & Package Managers

### Python
- **pyproject.toml** - Poetry and PEP 621 format
- **requirements.txt** files and variants
- **setup.py** (partial support)

### Node.js
- **package.json** - Dependencies and devDependencies
- **package-lock.json** (metadata only)
- **yarn.lock** (planned)

### Future Support
- **Java**: Maven (pom.xml), Gradle (build.gradle)
- **Ruby**: Gemfile, Gemfile.lock
- **Go**: go.mod, go.sum
- **Rust**: Cargo.toml, Cargo.lock
- **PHP**: composer.json, composer.lock
- **C#**: .csproj, packages.config

## Key Features

### Multi-Language Analysis
- Automatic detection of dependency files
- Language-specific parsing logic
- Unified output format across languages

### Dependency Grouping
- Main/production dependencies
- Development dependencies
- Optional dependencies
- Peer dependencies (Node.js)
- Build dependencies

### Metadata Extraction
- Version constraints and ranges
- Dependency descriptions
- License information (when available)
- Repository URLs

### Output Formatting
- Clean Markdown tables
- Hierarchical organization by language
- Version information preservation
- Group-based categorization

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from contextcraft.tools.dependency_lister import list_dependencies_logic

# Analyze current directory
list_dependencies_logic(
    project_path=Path("."),
    actual_output_path=None  # Print to console
)

# Save to file
list_dependencies_logic(
    project_path=Path("/path/to/project"),
    actual_output_path=Path("dependencies.md")
)
```

### Programmatic Access

```python
from contextcraft.tools.dependency_lister import (
    find_dependency_files,
    parse_python_dependencies,
    parse_nodejs_dependencies
)

# Find all dependency files
project_path = Path(".")
dependency_files = find_dependency_files(project_path)

# Parse specific files
for file_path in dependency_files:
    if file_path.name == "pyproject.toml":
        deps = parse_python_dependencies(file_path)
    elif file_path.name == "package.json":
        deps = parse_nodejs_dependencies(file_path)
```

## Architecture

### Extensible Design
The dependency lister uses a plugin-like architecture that makes it easy to add support for new languages:

```python
# Each language has dedicated parser functions
def parse_python_dependencies(file_path: Path) -> DependencyInfo:
    """Parse Python dependency files."""
    # Language-specific parsing logic

def parse_nodejs_dependencies(file_path: Path) -> DependencyInfo:
    """Parse Node.js dependency files."""
    # Language-specific parsing logic
```

### Data Structures
The module uses well-defined data structures for consistency:

- **DependencyInfo**: Container for all dependency data
- **DependencyGroup**: Categorized dependencies (main, dev, etc.)
- **Dependency**: Individual dependency with version info

### Error Handling
Robust error handling ensures graceful operation:

- Invalid file formats are skipped with warnings
- Missing files don't halt processing
- Malformed version specs are preserved as-is
- Network-dependent operations are avoided

## Output Format

The dependency lister generates structured Markdown output:

```markdown
# Project Dependencies

## Python Dependencies

### Main Dependencies (pyproject.toml)
- typer: ^0.9.0
- rich: ^13.0.0
- pathspec: ^0.12.1

### Development Dependencies (pyproject.toml)
- pytest: ^7.0.0
- mypy: ^1.0.0
- ruff: ^0.1.0

## Node.js Dependencies

### Dependencies (package.json)
- express: ^4.18.0
- lodash: ^4.17.21

### Development Dependencies (package.json)
- typescript: ^4.9.0
- jest: ^29.0.0
```

## Configuration Integration

The dependency lister integrates with ContextCraft's configuration system:

```toml
[tool.contextcraft]
default_output_filename_deps = "docs/dependencies.md"
```

## Performance Considerations

- **Fast File Discovery**: Uses efficient file system traversal
- **Lazy Parsing**: Only parses files when needed
- **Memory Efficient**: Streams output for large dependency lists
- **Caching**: Future versions will cache parsed results

## Testing

The module includes comprehensive tests covering:

- All supported file formats
- Edge cases and error conditions
- Multi-language projects
- Various dependency configurations
- Output formatting validation

## Future Enhancements

### Version 1.1
- License detection and reporting
- Security vulnerability scanning
- Dependency graph visualization
- Outdated dependency detection

### Version 1.2
- Dependency analysis and recommendations
- Conflict detection
- Size analysis for JavaScript packages
- Performance impact assessment

## Error Handling Patterns

The dependency lister uses consistent error handling:

```python
try:
    # Parse dependency file
    dependencies = parse_file(file_path)
except FileNotFoundError:
    console.print(f"[yellow]Warning: File not found: {file_path}[/yellow]")
    continue
except ParseError as e:
    console.print(f"[yellow]Warning: Could not parse {file_path}: {e}[/yellow]")
    continue
```

## Integration Examples

### CI/CD Integration

```yaml
# GitHub Actions
- name: Generate dependency report
  run: poetry run contextcraft deps --output artifacts/dependencies.md

- name: Check for security issues
  run: |
    poetry run contextcraft deps --output deps.md
    # Use output for security scanning
```

### Development Workflow

```bash
# Regular dependency analysis
contextcraft deps --output docs/dependencies.md

# Include in project documentation
cat docs/dependencies.md >> docs/project-overview.md

# Compare dependencies between branches
git checkout main
contextcraft deps --output main-deps.md
git checkout feature-branch
contextcraft deps --output feature-deps.md
diff main-deps.md feature-deps.md
```

---

*For more examples and advanced usage, see the [Tutorials](../../tutorials/basic-usage.md) and [User Guide](../../user-guide/dependency-analysis.md).*
