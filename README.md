<div align="center">

# codebrief

[![CI](https://github.com/Shorzinator/codebrief/workflows/codebrief%20CI/badge.svg)](https://github.com/Shorzinator/codebrief/actions)
[![Coverage](https://img.shields.io/badge/coverage-77%25-yellow)](https://github.com/Shorzinator/codebrief)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**The missing link between your codebase and AI assistants.**

*Stop copying files. Start solving problems.*

</div>

codebrief is a production-ready CLI toolkit that solves the core problem developers face when working with AI assistants: manually preparing context from their projects. Whether you're debugging with ChatGPT, explaining your codebase to Claude, or preparing documentation for any LLM, codebrief provides the essential tools to create rich, contextual project summaries in seconds, not minutes.

## Core Problem Solved

Developers waste 5-10 minutes manually copying files, explaining project structure, and gathering context every time they need AI assistance. codebrief reduces this to a single command that takes seconds.

## Essential Features

### **Smart Directory Trees**
- Hierarchical project structure visualization
- Rich console output with intelligent formatting
- Advanced filtering with `.llmignore` support
- Clean file output for documentation

### **Code Flattening**
- Concatenate multiple files into organized documents
- Clear file markers and intelligent content handling
- Support for include/exclude patterns
- Binary file detection and graceful handling

### **Dependency Analysis**
- Multi-language dependency extraction (Python, Node.js)
- Support for Poetry, pip, npm, and yarn
- Clean Markdown output with language grouping
- Extensible architecture for additional languages

### **Git Context**
- Current branch and status information
- Recent commit history with configurable depth
- Diff analysis for understanding changes
- Graceful handling of non-Git repositories

### **Context Bundling**
- Aggregate multiple tools into comprehensive bundles
- Configurable section inclusion/exclusion
- Well-structured Markdown with navigation
- Optimized for LLM consumption

### **Clipboard Integration**
- Copy output directly to clipboard with `--to-clipboard` or `-c`
- Available for all commands (tree, flatten, deps, git-info, bundle)
- Smart behavior: only works when no output file specified
- Cross-platform support with graceful error handling

### **Intelligent Filtering**
- `.llmignore` files with `.gitignore`-style syntax
- Configurable global patterns via `pyproject.toml`
- Smart precedence hierarchy
- Tool-specific fallback exclusions

---

## Quick Start

### Installation

```bash
# Install from PyPI
pip install codebrief

# Or install with Poetry
poetry add codebrief
```

### Basic Usage

```bash
# Generate a directory tree
codebrief tree

# Save tree to file
codebrief tree -o project_structure.txt

# Copy tree to clipboard
codebrief tree --to-clipboard

# Flatten code files
codebrief flatten src/ -o flattened_code.md

# Copy flattened code to clipboard
codebrief flatten src/ -c

# Analyze dependencies
codebrief deps

# Get Git context
codebrief git-info

# Create a comprehensive bundle
codebrief bundle -o project_context.md

# Copy bundle to clipboard
codebrief bundle --to-clipboard
```

### Configuration

Create a `.llmignore` file to exclude files and directories:

```gitignore
# .llmignore
*.log
__pycache__/
node_modules/
.env
build/
dist/
```

Configure defaults in `pyproject.toml`:

```toml
[tool.codebrief]
default_output_filename_tree = "project_tree.txt"
default_output_filename_flatten = "flattened_code.md"
default_output_filename_deps = "dependencies.md"
default_output_filename_git_info = "git_context.md"
default_output_filename_bundle = "project_bundle.md"

global_exclude_patterns = [
    "*.tmp",
    "temp/",
    ".cache/"
]
```

## Documentation

**[Live Documentation Website](https://shorzinator.github.io/codebrief/)**

Comprehensive documentation including:

- **[Getting Started](https://shorzinator.github.io/codebrief/getting-started/installation/)** - Installation and basic usage
- **[CLI Commands](https://shorzinator.github.io/codebrief/user-guide/cli-commands/)** - Complete command reference
- **[Configuration](https://shorzinator.github.io/codebrief/getting-started/configuration/)** - Advanced configuration options
- **[API Reference](https://shorzinator.github.io/codebrief/reference/)** - Detailed API documentation
- **[Examples](https://shorzinator.github.io/codebrief/examples/)** - Real-world usage examples
- **[Tutorials](https://shorzinator.github.io/codebrief/tutorials/)** - Step-by-step guides

## Development

### Prerequisites

- Python 3.9+
- Poetry
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Shorzinator/codebrief.git
cd codebrief

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/codebrief --cov-report=html
```

### Code Quality

We maintain high code quality standards:

- **Linting**: Ruff for fast Python linting
- **Formatting**: Ruff formatter for consistent code style
- **Security**: Bandit for security vulnerability scanning
- **Testing**: Pytest with 77%+ coverage
- **Commits**: Conventional Commits for clear history

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Reporting bugs and requesting features
- Development setup and workflow
- Code standards and testing
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI framework
- Styled with [Rich](https://rich.readthedocs.io/) for clean terminal output
- Powered by [Poetry](https://python-poetry.org/) for dependency management
- Quality assured with [Ruff](https://github.com/astral-sh/ruff) and [Pytest](https://pytest.org/)

## Project Status

codebrief is actively developed and maintained. Current status:

- **Core Tools**: All primary tools implemented and tested
- **CLI Interface**: Complete command-line interface
- **Documentation**: Comprehensive docs with examples
- **Testing**: 175+ tests with 77% coverage
- **CI/CD**: Automated testing and quality checks
- **V1.0.2**: Production-ready with critical fixes resolved

---

<div align="center">

**[Documentation](https://shorzinator.github.io/codebrief/) • [Issues](https://github.com/Shorzinator/codebrief/issues) • [Discussions](https://shorzinator.github.io/codebrief/community/)**

Made for the developer community

</div>
