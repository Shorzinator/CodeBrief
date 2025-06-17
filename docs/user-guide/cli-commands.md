# CLI Commands

Complete reference for all codebrief commands, options, and usage patterns.

## 📋 Command Overview

codebrief provides six main commands for different types of context generation:

| Command | Purpose | Output Format |
|---------|---------|---------------|
| `tree` | Generate directory structure | Text tree or Rich console |
| `flatten` | Concatenate file contents | Markdown with file separators |
| `deps` | Analyze project dependencies | Markdown with dependency tables |
| `git-info` | Extract Git context information | Markdown with Git status and history |
| `bundle` | Create comprehensive context bundles | Structured Markdown with multiple sections |
| `hello` | Example/test command | Console output |

## 🌳 tree - Directory Tree Generation

Generate visual representations of your project structure.

### Basic Usage

```bash
# Generate tree for current directory
codebrief tree

# Generate tree for specific directory
codebrief tree /path/to/project

# Save tree to file
codebrief tree --output project-structure.txt
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--to-clipboard` | `-c` | `Flag` | Copy output to clipboard (cannot be used with --output) |
| `--ignore` | `-i` | `List[str]` | Patterns to ignore (repeatable) |
| `--help` |  | | Show command help |

### Examples

=== "Basic Tree"

    ```bash
    codebrief tree
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
    codebrief tree --ignore "*.pyc" --ignore "__pycache__"
    ```

=== "Save to File"

    ```bash
    codebrief tree --output docs/project-structure.txt
    ```

=== "Copy to Clipboard"

    ```bash
    # Copy tree output directly to clipboard
    codebrief tree --to-clipboard
    # or use short form
    codebrief tree -c
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
codebrief tree
```

### Configuration Integration

Use `pyproject.toml` for default settings:

```toml
[tool.codebrief]
default_output_filename_tree = "docs/structure.txt"
global_exclude_patterns = ["*.log", "tmp/"]
```

```bash
# Uses configuration defaults
codebrief tree  # Creates docs/structure.txt
```

## 📄 flatten - Code Flattening

Concatenate multiple files into a single, LLM-friendly document.

### Basic Usage

```bash
# Flatten all default file types
codebrief flatten

# Flatten specific directory
codebrief flatten src/

# Flatten with custom patterns
codebrief flatten . --include "*.py" --include "*.md"
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--to-clipboard` | `-c` | `Flag` | Copy output to clipboard (cannot be used with --output) |
| `--include` | `-inc` | `List[str]` | Include patterns (repeatable) |
| `--exclude` | `-exc` | `List[str]` | Exclude patterns (repeatable) |
| `--help` |  | | Show command help |

### Examples

=== "Python Project"

    ```bash
    codebrief flatten . \
      --include "*.py" \
      --include "*.md" \
      --include "*.toml" \
      --output python-context.md
    ```

=== "Web Project"

    ```bash
    codebrief flatten . \
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
    codebrief flatten src/ --output source-only.md

    # Only tests
    codebrief flatten tests/ --include "*.py" --output tests-only.md

    # Copy flattened code to clipboard
    codebrief flatten src/ --to-clipboard
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

codebrief gracefully handles binary files:

```bash
codebrief flatten . --include "*"
```

Output includes:
```markdown
# --- Skipped binary or non-UTF-8 file: image.png ---

# --- File: script.py ---
# Python content here...
```

## 📦 deps - Dependency Analysis {#deps-command}

Analyze and document project dependencies across multiple languages.

### Basic Usage

```bash
# Analyze dependencies in current project
codebrief deps

# Save dependency report
codebrief deps --output dependencies.md
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--to-clipboard` | `-c` | `Flag` | Copy output to clipboard (cannot be used with --output) |
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
    codebrief deps --output python-deps.md
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
    codebrief deps
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
    codebrief deps --output all-deps.md
    ```

    Output includes both Python and Node.js dependencies.

## 🔄 git-info - Git Context Extraction

Extract comprehensive Git repository information for context generation.

### Basic Usage

```bash
# Generate Git context for current directory
codebrief git-info

# Generate Git context for specific repository
codebrief git-info /path/to/repo

# Save Git context to file
codebrief git-info --output git-context.md
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--to-clipboard` | `-c` | `Flag` | Copy output to clipboard (cannot be used with --output) |
| `--log-count` | `-n` | `int` | Number of recent commits to include (default: 10) |
| `--full-diff` |  | `bool` | Include full diff of uncommitted changes |
| `--diff-options` |  | `str` | Custom git diff options (e.g., "--stat", "--name-only") |
| `--help` |  | | Show command help |

### Examples

=== "Basic Git Info"

    ```bash
    codebrief git-info
    ```

    Output:
    ```markdown
    # Git Context

    ## Repository Information
    - **Current Branch:** main
    - **Repository Status:** Clean working directory

    ## Recent Commits (Last 10)
    1. **feat: add new feature** (2024-01-15)
       - Author: Developer <dev@example.com>
       - Hash: abc123f

    2. **fix: resolve bug in parser** (2024-01-14)
       - Author: Developer <dev@example.com>
       - Hash: def456a
    ```

=== "With Full Diff"

    ```bash
    codebrief git-info --full-diff --log-count 5
    ```

    Includes complete diff of uncommitted changes.

=== "Custom Diff Options"

    ```bash
    codebrief git-info --diff-options "--stat --color=never"
    ```

    Uses custom git diff options for change summary.

### Error Handling

The git-info command gracefully handles various scenarios:

- **Non-Git Repository**: Returns informative message
- **Git Not Installed**: Provides installation guidance
- **Permission Issues**: Clear error messages
- **Network Timeouts**: Handles slow Git operations

### Configuration Integration

```toml
[tool.codebrief]
default_output_filename_git_info = "docs/git-context.md"
```

```bash
# Uses configuration default
codebrief git-info  # Creates docs/git-context.md
```

## 📦 bundle - Comprehensive Context Bundling

Create structured bundles combining multiple context tools for comprehensive project understanding.

### Basic Usage

```bash
# Create complete project bundle
codebrief bundle

# Create bundle for specific directory
codebrief bundle /path/to/project

# Save bundle to file
codebrief bundle --output project-bundle.md
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output` | `-o` | `Path` | Output file path |
| `--to-clipboard` | `-c` | `Flag` | Copy output to clipboard (cannot be used with --output) |
| `--exclude-tree` |  | `bool` | Exclude directory tree section |
| `--exclude-git` |  | `bool` | Exclude Git context section |
| `--exclude-deps` |  | `bool` | Exclude dependencies section |
| `--exclude-files` |  | `bool` | Exclude flattened files section |
| `--flatten` |  | `List[Path]` | Specific paths to flatten (repeatable) |
| `--git-log-count` |  | `int` | Number of Git commits to include |
| `--git-full-diff` |  | `bool` | Include full Git diff |
| `--git-diff-options` |  | `str` | Custom Git diff options |
| `--help` |  | | Show command help |

### Examples

=== "Complete Bundle"

    ```bash
    codebrief bundle --output complete-context.md
    ```

    Creates a comprehensive bundle with all sections:
    - Table of Contents
    - Directory Tree
    - Git Context
    - Dependencies
    - Flattened Files

=== "Code Review Bundle"

    ```bash
    codebrief bundle \
      --exclude-deps \
      --flatten src/ tests/ \
      --git-log-count 5 \
      --output review-bundle.md
    ```

    Focused bundle for code review with recent Git history.

=== "Documentation Bundle"

    ```bash
    codebrief bundle \
      --exclude-git \
      --flatten docs/ README.md \
      --output docs-bundle.md
    ```

    Documentation-focused bundle without Git information.

=== "Clipboard Bundle"

    ```bash
    # Copy comprehensive bundle directly to clipboard
    codebrief bundle --to-clipboard

    # Copy focused bundle to clipboard
    codebrief bundle --flatten src/ -c
    ```

### Bundle Structure

The bundle command creates well-organized output:

```markdown
# codebrief Bundle

## Table of Contents
- [Directory Tree](#directory-tree)
- [Git Context](#git-context)
- [Dependencies](#dependencies)
- [Files: src/codebrief/tools](#files-srccodebrieftools)

## Directory Tree
📁 my-project/
├── 📄 README.md
├── 📁 src/
└── 📁 tests/

## Git Context
**Current Branch:** main
**Repository Status:** Clean

## Dependencies
### Python Dependencies (pyproject.toml)
- typer: ^0.9.0
- rich: ^13.0.0

## Files: src/codebrief/tools
# --- File: src/codebrief/tools/bundler.py ---
[File contents...]
```

### Advanced Configuration

```toml
[tool.codebrief]
default_output_filename_bundle = "context-bundle.md"
global_exclude_patterns = ["*.pyc", "__pycache__/"]
```

### Integration with Other Tools

The bundle command leverages all other codebrief tools:

- **tree**: For directory structure
- **git-info**: For Git context
- **deps**: For dependency analysis
- **flatten**: For file content aggregation

## 👋 hello - Example Command

A simple example command for testing and demonstration.

### Basic Usage

```bash
# Default greeting
codebrief hello

# Custom name
codebrief hello --name "Developer"
```

### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--name` |  | `str` | Name to greet |
| `--help` |  | | Show command help |

### Examples

```bash
# Default
codebrief hello
# Output: Hello World from codebrief!

# Custom name
codebrief hello --name "Alice"
# Output: Hello Alice from codebrief!
```

## 📋 Clipboard Integration

All codebrief commands support clipboard functionality through the `--to-clipboard` or `-c` flag:

### Usage

```bash
# Copy any command output to clipboard
codebrief tree --to-clipboard
codebrief flatten . -c
codebrief deps --to-clipboard
codebrief git-info -c
codebrief bundle --to-clipboard
```

### Features

- **Cross-platform**: Works on Windows, macOS, and Linux
- **Smart behavior**: Only available when no output file is specified
- **User feedback**: Shows success/error messages
- **Graceful errors**: Handles clipboard access issues gracefully

### Examples

```bash
# ✅ Valid - copy to clipboard
codebrief tree -c

# ❌ Invalid - cannot use both clipboard and file output
codebrief tree -c --output file.txt

# ✅ Valid - save to file (no clipboard)
codebrief tree --output file.txt
```

### Error Handling

When clipboard access fails, codebrief provides helpful feedback:

```bash
codebrief tree -c
# Success: 📋 Output successfully copied to clipboard!

# If clipboard access fails:
# Warning: Failed to copy to clipboard: [error details]
```

## 🔧 Global Options

These options work with all commands:

### Help and Version

```bash
# Show general help
codebrief --help

# Show version
codebrief --version

# Command-specific help
codebrief tree --help
codebrief flatten --help
codebrief deps --help
codebrief git-info --help
codebrief bundle --help
```

### Environment Variables

Set global behavior via environment variables:

```bash
# Debug mode
export codebrief_DEBUG=1
codebrief tree

# Custom output directory
export codebrief_OUTPUT_DIR=~/codebrief-outputs
codebrief flatten . --output code.md  # Saves to ~/codebrief-outputs/code.md
```

## 🎯 Command Combinations

### Comprehensive Project Context

Generate complete project context:

```bash
# Option 1: Use the bundle command (recommended)
codebrief bundle --output complete-project-context.md

# Option 2: Generate individual components
codebrief tree --output docs/structure.txt
codebrief git-info --output docs/git-context.md
codebrief deps --output docs/dependencies.md
codebrief flatten . \
  --include "*.py" --include "*.md" --include "*.toml" \
  --output docs/codebase.md
```

### Selective Context for Different Audiences

=== "For Code Review"

    ```bash
    # Focus on source code
    codebrief flatten src/ tests/ --output review-context.md

    # Include project structure
    codebrief tree src/ tests/ --output review-structure.txt

    # Quick clipboard sharing for review
    codebrief bundle --flatten src/ tests/ --exclude-deps -c
    ```

=== "For Documentation"

    ```bash
    # Include documentation and config
    codebrief flatten . \
      --include "*.md" --include "*.rst" --include "*.toml" \
      --output docs-context.md

    # Copy docs to clipboard for sharing
    codebrief flatten docs/ --include "*.md" -c
    ```

=== "For Debugging"

    ```bash
    # Include logs and config (temporarily)
    codebrief flatten . \
      --include "*.py" --include "*.log" --include "*.json" \
      --output debug-context.md

    # Quick debug context to clipboard
    codebrief bundle --flatten src/ --git-full-diff -c
    ```

=== "For Quick LLM Sharing"

    ```bash
    # Everything to clipboard for AI assistance
    codebrief bundle -c

    # Just source code and structure
    codebrief flatten src/ -c && codebrief tree -c

    # Git context and recent changes
    codebrief git-info --full-diff -c
    ```

## 🚨 Error Handling

codebrief provides helpful error messages:

### Common Errors and Solutions

!!! error "Directory Not Found"
    ```bash
    codebrief tree /nonexistent
    # Error: Invalid value for 'ROOT_DIR': Directory '/nonexistent' does not exist.
    ```

    **Solution**: Check the path and ensure the directory exists.

!!! error "Permission Denied"
    ```bash
    codebrief flatten / --output /etc/output.md
    # Error: Permission denied when writing to '/etc/output.md'
    ```

    **Solution**: Choose a writable output location or check permissions.

!!! error "Configuration Error"
    ```bash
    # With invalid pyproject.toml
    codebrief tree
    # Warning: Expected list for 'global_exclude_patterns', got str. Using default.
    ```

    **Solution**: Fix the configuration type in `pyproject.toml`.

### Rich Error Output

codebrief uses Rich for beautiful error messages:

```bash
codebrief flatten /nonexistent
```

Shows colorized, well-formatted error with context and suggestions.

## 🔍 Debugging Commands

### Verbose Output (Future Feature)

```bash
# Show detailed processing information
codebrief tree --verbose
codebrief flatten . --verbose --include "*.py"
```

### Dry Run (Future Feature)

```bash
# See what would be processed without actually doing it
codebrief flatten . --dry-run --include "*.py"
```

## 📚 Next Steps

Now that you know the commands:

1. **Practice**: Try different combinations on your projects
2. **Configure**: Set up [Configuration](configuration.md) for your workflow
3. **Automate**: Use commands in scripts and [CI/CD](../tutorials/cicd-integration.md)
4. **Advanced**: Learn [Advanced Workflows](../tutorials/advanced-workflows.md)

---

*Need more examples? Check out our [Tutorials](../tutorials/basic-usage.md) and [Examples](../examples/python-projects.md).*
