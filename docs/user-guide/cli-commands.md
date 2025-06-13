# CLI Commands

Complete reference for all ContextCraft commands, options, and usage patterns.

## 📋 Command Overview

ContextCraft provides four main commands for different types of context generation:

| Command | Purpose | Output Format |
|---------|---------|---------------|
| `tree` | Generate directory structure | Text tree or Rich console |
| `flatten` | Concatenate file contents | Markdown with file separators |
| `deps` | Analyze project dependencies | Markdown with dependency tables |
| `hello` | Example/test command | Console output |

## 🌳 tree - Directory Tree Generation

Generate visual representations of your project structure.

### Basic Usage

```bash
# Generate tree for current directory
contextcraft tree

# Generate tree for specific directory
contextcraft tree /path/to/project

# Save tree to file
contextcraft tree --output project-structure.txt
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--ignore` | `-i` | `List[str]` | Patterns to ignore (repeatable) |
| `--help` |  | | Show command help |

### Examples

=== "Basic Tree"

    ```bash
    contextcraft tree
    ```

    Output:
    ```
    📁 my-project/
    ├── 📄 README.md
    ├── 📄 pyproject.toml
    ├── 📁 src/
    │   ├── 📁 myapp/
    │   │   ├── 📄 __init__.py
    │   │   └── 📄 main.py
    │   └── 📄 __init__.py
    └── 📁 tests/
        └── 📄 test_main.py
    ```

=== "With Ignores"

    ```bash
    contextcraft tree --ignore "*.pyc" --ignore "__pycache__"
    ```

=== "Save to File"

    ```bash
    contextcraft tree --output docs/project-structure.txt
    ```

### Integration with .llmignore

The tree command automatically respects `.llmignore` patterns:

```gitignore
# .llmignore
__pycache__/
*.pyc
.venv/
```

```bash
# Automatically excludes patterns from .llmignore
contextcraft tree
```

### Configuration Integration

Use `pyproject.toml` for default settings:

```toml
[tool.contextcraft]
default_output_filename_tree = "docs/structure.txt"
global_exclude_patterns = ["*.log", "tmp/"]
```

```bash
# Uses configuration defaults
contextcraft tree  # Creates docs/structure.txt
```

## 📄 flatten - Code Flattening

Concatenate multiple files into a single, LLM-friendly document.

### Basic Usage

```bash
# Flatten all default file types
contextcraft flatten

# Flatten specific directory
contextcraft flatten src/

# Flatten with custom patterns
contextcraft flatten . --include "*.py" --include "*.md"
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--include` | `-inc` | `List[str]` | Include patterns (repeatable) |
| `--exclude` | `-exc` | `List[str]` | Exclude patterns (repeatable) |
| `--help` |  | | Show command help |

### Examples

=== "Python Project"

    ```bash
    contextcraft flatten . \
      --include "*.py" \
      --include "*.md" \
      --include "*.toml" \
      --output python-context.md
    ```

=== "Web Project"

    ```bash
    contextcraft flatten . \
      --include "*.js" \
      --include "*.ts" \
      --include "*.html" \
      --include "*.css" \
      --exclude "node_modules/" \
      --exclude "dist/" \
      --output web-context.md
    ```

=== "Selective Flattening"

    ```bash
    # Only source code
    contextcraft flatten src/ --output source-only.md

    # Only tests
    contextcraft flatten tests/ --include "*.py" --output tests-only.md
    ```

### Output Format

The flatten command produces well-structured output:

```markdown
# --- File: src/main.py ---
"""Main application module."""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()


# --- File: src/utils.py ---
"""Utility functions."""

def helper_function():
    return "I'm helping!"


# --- File: tests/test_main.py ---
"""Tests for main module."""

import pytest
from src.main import main

def test_main():
    # Test implementation
    assert True
```

### Binary File Handling

ContextCraft gracefully handles binary files:

```bash
contextcraft flatten . --include "*"
```

Output includes:
```markdown
# --- Skipped binary or non-UTF-8 file: image.png ---

# --- File: script.py ---
# Python content here...
```

## 📦 deps - Dependency Analysis

Analyze and document project dependencies across multiple languages.

### Basic Usage

```bash
# Analyze dependencies in current project
contextcraft deps

# Save dependency report
contextcraft deps --output dependencies.md
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--help` |  | | Show command help |

### Supported Dependency Files

| Language | Files Supported |
|----------|----------------|
| **Python** | `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, etc. |
| **Node.js** | `package.json` |
| **Future** | `pom.xml`, `build.gradle`, `Gemfile`, `Cargo.toml`, etc. |

### Examples

=== "Python Project"

    ```bash
    contextcraft deps --output python-deps.md
    ```

    Output:
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
    ```

=== "Node.js Project"

    ```bash
    contextcraft deps
    ```

    Output:
    ```markdown
    # Project Dependencies

    ## Node.js Dependencies

    ### Dependencies (package.json)
    - express: ^4.18.0
    - lodash: ^4.17.21

    ### Development Dependencies (package.json)
    - typescript: ^4.9.0
    - jest: ^29.0.0
    ```

=== "Multi-Language Project"

    ```bash
    contextcraft deps --output all-deps.md
    ```

    Output includes both Python and Node.js dependencies.

## 👋 hello - Example Command

A simple example command for testing and demonstration.

### Basic Usage

```bash
# Default greeting
contextcraft hello

# Custom name
contextcraft hello --name "Developer"
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--name` |  | `str` | Name to greet |
| `--help` |  | | Show command help |

### Examples

```bash
# Default
contextcraft hello
# Output: Hello World from ContextCraft!

# Custom name
contextcraft hello --name "Alice"
# Output: Hello Alice from ContextCraft!
```

## 🔧 Global Options

These options work with all commands:

### Help and Version

```bash
# Show general help
contextcraft --help

# Show version
contextcraft --version

# Command-specific help
contextcraft tree --help
contextcraft flatten --help
contextcraft deps --help
```

### Environment Variables

Set global behavior via environment variables:

```bash
# Debug mode
export CONTEXTCRAFT_DEBUG=1
contextcraft tree

# Custom output directory
export CONTEXTCRAFT_OUTPUT_DIR=~/contextcraft-outputs
contextcraft flatten . --output code.md  # Saves to ~/contextcraft-outputs/code.md
```

## 🎯 Command Combinations

### Comprehensive Project Context

Generate complete project context:

```bash
# Create project overview
contextcraft tree --output docs/structure.txt

# Create code summary
contextcraft flatten . \
  --include "*.py" --include "*.md" --include "*.toml" \
  --output docs/codebase.md

# Create dependency report
contextcraft deps --output docs/dependencies.md
```

### Selective Context for Different Audiences

=== "For Code Review"

    ```bash
    # Focus on source code
    contextcraft flatten src/ tests/ --output review-context.md

    # Include project structure
    contextcraft tree src/ tests/ --output review-structure.txt
    ```

=== "For Documentation"

    ```bash
    # Include documentation and config
    contextcraft flatten . \
      --include "*.md" --include "*.rst" --include "*.toml" \
      --output docs-context.md
    ```

=== "For Debugging"

    ```bash
    # Include logs and config (temporarily)
    contextcraft flatten . \
      --include "*.py" --include "*.log" --include "*.json" \
      --output debug-context.md
    ```

## 🚨 Error Handling

ContextCraft provides helpful error messages:

### Common Errors and Solutions

!!! error "Directory Not Found"
    ```bash
    contextcraft tree /nonexistent
    # Error: Invalid value for 'ROOT_DIR': Directory '/nonexistent' does not exist.
    ```

    **Solution**: Check the path and ensure the directory exists.

!!! error "Permission Denied"
    ```bash
    contextcraft flatten / --output /etc/output.md
    # Error: Permission denied when writing to '/etc/output.md'
    ```

    **Solution**: Choose a writable output location or check permissions.

!!! error "Configuration Error"
    ```bash
    # With invalid pyproject.toml
    contextcraft tree
    # Warning: Expected list for 'global_exclude_patterns', got str. Using default.
    ```

    **Solution**: Fix the configuration type in `pyproject.toml`.

### Rich Error Output

ContextCraft uses Rich for beautiful error messages:

```bash
contextcraft flatten /nonexistent
```

Shows colorized, well-formatted error with context and suggestions.

## 🔍 Debugging Commands

### Verbose Output (Future Feature)

```bash
# Show detailed processing information
contextcraft tree --verbose
contextcraft flatten . --verbose --include "*.py"
```

### Dry Run (Future Feature)

```bash
# See what would be processed without actually doing it
contextcraft flatten . --dry-run --include "*.py"
```

## 📚 Next Steps

Now that you know the commands:

1. **Practice**: Try different combinations on your projects
2. **Configure**: Set up [Configuration](configuration.md) for your workflow
3. **Automate**: Use commands in scripts and [CI/CD](../tutorials/cicd-integration.md)
4. **Advanced**: Learn [Advanced Workflows](../tutorials/advanced-workflows.md)

---

*Need more examples? Check out our [Tutorials](../tutorials/basic-usage.md) and [Examples](../examples/python-projects.md).*
