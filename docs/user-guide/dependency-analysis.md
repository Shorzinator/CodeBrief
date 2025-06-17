# Dependency Analysis

The `deps` command provides comprehensive dependency analysis across multiple programming languages and package managers. It's designed to give you a clear overview of your project's dependencies for documentation, LLM context, or dependency auditing.

## Overview

codebrief's dependency analysis tool:

- **Multi-language Support**: Python, Node.js, with extensible architecture for more languages
- **Multiple Package Managers**: Poetry, pip, npm, yarn
- **Clean Output**: Organized Markdown format perfect for documentation and LLM consumption
- **Dependency Separation**: Clearly distinguishes between main and development dependencies

## Supported Languages & Formats

### Python

| File Type | Package Manager | Dependencies | Dev Dependencies |
|-----------|----------------|--------------|------------------|
| `pyproject.toml` | Poetry | ✅ | ✅ |
| `pyproject.toml` | PEP 621 | ✅ | ✅ |
| `requirements.txt` | pip | ✅ | ❌ |
| `requirements-dev.txt` | pip | ❌ | ✅ |
| `dev-requirements.txt` | pip | ❌ | ✅ |

### Node.js

| File Type | Package Manager | Dependencies | Dev Dependencies |
|-----------|----------------|--------------|------------------|
| `package.json` | npm/yarn | ✅ | ✅ |

## Basic Usage

### Simple Dependency Analysis

```bash
# Analyze dependencies in current directory
codebrief deps

# Analyze specific project directory
codebrief deps /path/to/project

# Save to file
codebrief deps --output dependencies.md
```

### Example Output

```markdown
--- Project Dependencies ---

## Python

### Poetry

### Dev Dependencies
• ruff ^0.1.0
• pytest ^7.0.0
• pytest-cov ^4.0.0
• pre-commit ^4.2.0

### Main Dependencies
• typer ^0.9.0
• rich ^13.0.0
• pathspec ^0.12.1
```

## Configuration

### Default Output Files

Configure default output files in `pyproject.toml`:

```toml
[tool.codebrief]
default_output_filename_deps = "project-dependencies.md"
```

### Global Excludes

Exclude certain dependency files from analysis:

```toml
[tool.codebrief]
global_exclude_patterns = [
    "test-requirements.txt",
    "*/experimental-deps.toml"
]
```

## Advanced Usage

### Multiple Environments

For projects with multiple dependency environments:

```bash
# Analyze all dependency files in project
codebrief deps --output all-deps.md

# This will automatically detect:
# - pyproject.toml (main + dev dependencies)
# - requirements.txt (production)
# - requirements-dev.txt (development)
# - package.json (Node.js if present)
```

### CI/CD Integration

Perfect for automated dependency tracking:

```yaml
# GitHub Actions example
- name: Generate Dependency Report
  run: |
    poetry run codebrief deps --output deps-report.md
    cat deps-report.md >> $GITHUB_STEP_SUMMARY
```

## Understanding the Output

### Dependency Grouping

Dependencies are organized by:

1. **Language** (Python, Node.js)
2. **Package Manager** (Poetry, pip, npm)
3. **Dependency Type** (Main, Dev Dependencies)

### Direct Dependencies Only

The tool shows **direct dependencies** only (what you explicitly declared), not transitive dependencies. This keeps the output clean and focused on your project's intentional dependencies.

!!! info "Why Direct Dependencies Only?"

    Direct dependencies answer "What does this project intentionally depend on?" rather than "What gets installed?". This provides cleaner context for documentation and LLM consumption without overwhelming detail.

### Version Constraints

Version information is preserved as specified in your dependency files:

- `^1.0.0` - Caret constraints (Poetry/npm)
- `>=1.0.0,<2.0.0` - Range constraints
- `*` - Any version
- `1.0.0` - Exact version pins

## Use Cases

### Documentation Generation

Create dependency documentation for your project:

```bash
codebrief deps --output docs/dependencies.md
```

### LLM Context

Generate clean dependency context for AI assistance:

```bash
# Include in bundle for comprehensive project context
codebrief bundle --output project-context.md

# Or standalone for dependency-focused questions
codebrief deps --output deps-context.md
```

### Dependency Auditing

Regular dependency analysis for project maintenance:

```bash
# Weekly dependency check
codebrief deps --output weekly-deps-$(date +%Y-%m-%d).md
```

### Code Reviews

Include dependency changes in code reviews:

```bash
# Generate dependency snapshot for PR
codebrief deps --output pr-dependencies.md
git add pr-dependencies.md
```

## Extensibility

The dependency analysis system is designed for easy extension. The architecture supports:

- **New Languages**: Add support for Go, Rust, Java, etc.
- **New Package Managers**: Extend existing language support
- **Custom Formats**: Support organization-specific dependency formats

### Adding New Languages

The system uses a plugin-like architecture where new language analyzers can be added to the `dependency_lister.py` module.

## Troubleshooting

### No Dependencies Found

If no dependencies are detected:

1. **Check File Names**: Ensure dependency files are named correctly
2. **File Location**: Run from project root or specify correct path
3. **File Format**: Verify file syntax is valid

### Parsing Errors

For parsing errors:

```bash
# Check if files are valid
poetry check  # For pyproject.toml
npm install --dry-run  # For package.json
```

### Missing Languages

If your language isn't supported:

1. Check our [roadmap](https://github.com/Shorzinator/codebrief/issues) for planned support
2. [Open a feature request](https://github.com/Shorzinator/codebrief/issues/new) for new language support
3. Consider [contributing](../development/contributing.md) an implementation

## Performance

The dependency analysis is optimized for speed:

- **File Detection**: Fast filesystem scanning
- **Parallel Processing**: Multiple files processed concurrently when possible
- **Memory Efficient**: Streaming parsing for large dependency files
- **Cache Friendly**: Results can be cached for repeated analysis

## Integration with Other Tools

### With Tree Command

```bash
# Show structure and dependencies
codebrief tree --output structure.txt
codebrief deps --output deps.md
```

### With Bundle Command

```bash
# Comprehensive project context including dependencies
codebrief bundle \
  --output complete-context.md \
  --include-deps
```

### With Git Info

```bash
# Dependencies with Git context for version tracking
codebrief git-info --output git-context.md
codebrief deps --output deps-context.md
```

## Best Practices

1. **Regular Updates**: Run dependency analysis regularly to track changes
2. **Version Control**: Include dependency reports in version control for tracking
3. **Documentation**: Use in project documentation for clear dependency overview
4. **Security**: Regular analysis helps identify when dependencies change
5. **Team Communication**: Share dependency reports in code reviews and planning

## Command Reference

```bash
codebrief deps --help
```

For complete command options and flags, see the [CLI Commands Reference](cli-commands.md#deps-command).
