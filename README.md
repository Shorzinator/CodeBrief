# ContextCraft

[![CI](https://github.com/Shorzinator/ContextCraft/workflows/ContextCraft%20CI/badge.svg)](https://github.com/Shorzinator/ContextCraft/actions)
[![Coverage](https://img.shields.io/badge/coverage-77%25-yellow)](https://github.com/Shorzinator/ContextCraft)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**A powerful CLI toolkit to generate comprehensive project context for Large Language Models (LLMs).**

ContextCraft transforms your codebase into well-structured, LLM-friendly documentation by intelligently aggregating directory trees, code files, dependencies, and Git context into clean, consumable formats.

## ✨ Features

### 🌳 **Smart Directory Trees**
- Beautiful, hierarchical project structure visualization
- Rich console output with emojis and colors
- Intelligent filtering with `.llmignore` support
- Clean file output for documentation

### 📄 **Code Flattening**
- Concatenate multiple files into organized documents
- Clear file markers and intelligent content handling
- Support for include/exclude patterns
- Binary file detection and graceful handling

### 📦 **Dependency Analysis**
- Multi-language dependency extraction (Python, Node.js)
- Support for Poetry, pip, npm, and yarn
- Clean Markdown output with language grouping
- Extensible architecture for additional languages

### 🔄 **Git Context**
- Current branch and status information
- Recent commit history with configurable depth
- Diff analysis for understanding changes
- Graceful handling of non-Git repositories

### 📋 **Context Bundling**
- Aggregate multiple tools into comprehensive bundles
- Configurable section inclusion/exclusion
- Well-structured Markdown with navigation
- Perfect for LLM consumption

### 🎯 **Intelligent Filtering**
- `.llmignore` files with `.gitignore`-style syntax
- Configurable global patterns via `pyproject.toml`
- Smart precedence hierarchy
- Tool-specific fallback exclusions

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install contextcraft

# Or install from source
git clone https://github.com/Shorzinator/ContextCraft.git
cd ContextCraft
poetry install
```

### Basic Usage

```bash
# Generate a directory tree
contextcraft tree

# Save tree to file
contextcraft tree -o project_structure.txt

# Flatten code files
contextcraft flatten src/ -o flattened_code.md

# Analyze dependencies
contextcraft deps

# Get Git context
contextcraft git-info

# Create a comprehensive bundle
contextcraft bundle -o project_context.md
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
[tool.contextcraft]
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

## 📖 Documentation

- **[Getting Started](docs/getting-started/quick-start.md)** - Installation and basic usage
- **[CLI Commands](docs/user-guide/cli-commands.md)** - Complete command reference
- **[Configuration](docs/getting-started/configuration.md)** - Advanced configuration options
- **[API Reference](docs/reference/)** - Detailed API documentation
- **[Examples](docs/examples/)** - Real-world usage examples

## 🛠️ Development

### Prerequisites

- Python 3.9+
- Poetry
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Shorzinator/ContextCraft.git
cd ContextCraft

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/contextcraft --cov-report=html
```

### Code Quality

We maintain high code quality standards:

- **Linting**: Ruff for fast Python linting
- **Formatting**: Ruff formatter for consistent code style
- **Security**: Bandit for security vulnerability scanning
- **Testing**: Pytest with 77%+ coverage
- **Commits**: Conventional Commits for clear history

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Reporting bugs and requesting features
- Development setup and workflow
- Code standards and testing
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI framework
- Styled with [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- Powered by [Poetry](https://python-poetry.org/) for dependency management
- Quality assured with [Ruff](https://github.com/astral-sh/ruff) and [Pytest](https://pytest.org/)

## 📊 Project Status

ContextCraft is actively developed and maintained. Current status:

- ✅ **Core Tools**: All primary tools implemented and tested
- ✅ **CLI Interface**: Complete command-line interface
- ✅ **Documentation**: Comprehensive docs with examples
- ✅ **Testing**: 165+ tests with 77% coverage
- ✅ **CI/CD**: Automated testing and quality checks
- 🚀 **V1.0**: Feature-complete and production-ready

---

<div align="center">

**[Documentation](docs/) • [Issues](https://github.com/Shorzinator/ContextCraft/issues) • [Discussions](https://github.com/Shorzinator/ContextCraft/discussions)**

Made with ❤️ for the developer community

</div>
