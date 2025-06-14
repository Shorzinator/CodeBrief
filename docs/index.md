# Welcome to ContextCraft

<div align="center">
  <h2>A Powerful CLI Toolkit for LLM-Ready Project Context</h2>
  <p><em>Transform your codebase into comprehensive, structured context that Large Language Models love!</em></p>
</div>

---

**ContextCraft** is a sophisticated, production-ready Command Line Interface (CLI) toolkit designed to help developers generate comprehensive, structured context from their projects. Whether you're debugging with ChatGPT, explaining your codebase to Claude, or preparing documentation for any LLM, ContextCraft provides the perfect tools to create rich, contextual project summaries.

## Features

### 🌳 Directory Tree Generation
Generate beautiful, hierarchical representations of your project structure with intelligent filtering and customization options.

### 📄 Code Flattening
Concatenate code from multiple files into a single, well-organized document with clear file markers and intelligent content handling.

### 📦 Dependency Analysis
Extract and analyze project dependencies across multiple languages and package managers (Python, Node.js, and more).

### 🔄 Git Context Extraction
Comprehensive Git repository information including branch status, commit history, and change diffs for enhanced development context.

### 📋 Context Bundling
Powerful aggregation tool that combines directory trees, Git context, dependencies, and flattened code into structured, comprehensive bundles.

### 🚫 Intelligent Ignore System
Sophisticated `.llmignore` file support with `.gitignore`-style syntax for precise control over what gets included.

### ⚙️ Advanced Configuration
Flexible configuration system via `pyproject.toml` with support for default outputs, global patterns, and project-specific settings.

### ✨ Rich CLI Experience
Beautiful, intuitive command-line interface powered by Typer and Rich with helpful error messages and progress indicators.

## Quick Start

Get started with ContextCraft in minutes:

=== "Installation"

    ```bash
    # Install from source (PyPI coming soon!)
    git clone https://github.com/Shorzinator/ContextCraft.git
    cd ContextCraft
    poetry install
    poetry shell
    ```

=== "Basic Usage"

    ```bash
    # Generate a directory tree
    contextcraft tree

    # Flatten your Python code
    contextcraft flatten . --include "*.py" --output context.md

    # Analyze dependencies
    contextcraft deps --output deps.md

    # Extract Git context
    contextcraft git-info --output git-context.md

    # Create comprehensive bundle
    contextcraft bundle --output project-bundle.md
    ```

=== "Advanced Workflow"

    ```bash
    # Create comprehensive project context with bundle
    contextcraft bundle \
      --output complete-context.md \
      --git-log-count 15 \
      --flatten src/ tests/

    # Focused code review bundle
    contextcraft bundle \
      --exclude-deps \
      --git-full-diff \
      --flatten src/ tests/ \
      --output review-bundle.md

    # Use .llmignore for fine-grained control
    echo "*.log\n__pycache__/\n.venv/" > .llmignore
    ```

## Perfect For

<div class="grid cards" markdown>

-   :material-robot: **LLM Integration**

    ---

    Generate context that's perfectly formatted for ChatGPT, Claude, Copilot, and other AI coding assistants.

-   :material-source-pull: **Code Reviews**

    ---

    Create comprehensive review bundles with Git context, code changes, and project structure for thorough reviews.

-   :material-bug: **Debugging**

    ---

    Quickly share your project structure, Git history, and relevant code with others or AI tools for faster problem resolution.

-   :material-book-open: **Documentation**

    ---

    Create comprehensive project overviews for onboarding, code reviews, and technical documentation.

-   :material-rocket: **Development**

    ---

    Streamline your workflow with automated context generation for various development scenarios and CI/CD integration.

-   :material-git: **Git Workflows**

    ---

    Integrate with Git workflows for branch-specific context, commit analysis, and development progress tracking.

</div>

## Architecture

ContextCraft is built with modern Python best practices:

- **CLI Framework**: [Typer](https://typer.tiangolo.com/) for intuitive command-line interfaces
- **Rich Output**: [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- **Modular Design**: Clean separation between tools, utilities, and CLI commands
- **Comprehensive Testing**: 165+ tests with 77%+ coverage
- **Security Compliant**: Bandit security scanning with proper subprocess handling
- **Code Quality**: Ruff, pre-commit hooks, and conventional commits for maintainable code

## Documentation Sections

<div class="grid cards" markdown>

-   [:octicons-rocket-24: **Getting Started**](getting-started/installation.md)

    ---

    Installation, quick start guide, and basic configuration

-   [:octicons-book-24: **User Guide**](user-guide/cli-commands.md)

    ---

    Comprehensive guides for all CLI commands and features

-   [:octicons-mortar-board-24: **Tutorials**](tutorials/basic-usage.md)

    ---

    Step-by-step tutorials for common workflows and use cases

-   [:octicons-code-24: **API Reference**](reference/main.md)

    ---

    Complete API documentation for all modules and functions

-   [:octicons-workflow-24: **Examples**](examples/git-workflows.md)

    ---

    Real-world examples for Git workflows, bundle patterns, and automation

</div>

## What's New in v1.0

!!! success "Production Ready - All Core Features Complete"

    - **Complete Tool Suite**: Tree generation, code flattening, dependency analysis, Git context, and bundling
    - **Git Integration**: Comprehensive Git context extraction with branch info, commits, and diffs
    - **Bundle System**: Powerful context aggregation combining all tools into structured documents
    - **Advanced Configuration**: `pyproject.toml` integration with type validation and new tool support
    - **Sophisticated Ignore System**: `.llmignore` with full `.gitignore` syntax support
    - **Rich Error Handling**: Safe markup processing and user-friendly error messages
    - **Comprehensive Testing**: 165 tests covering all functionality with robust content-based assertions
    - **Security Compliance**: Full Bandit security compliance with proper subprocess handling
    - **Beautiful Documentation**: This comprehensive documentation site with extensive examples!

## Core Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `tree` | Directory structure visualization | Rich console output, file filtering |
| `flatten` | Code file aggregation | Multi-file concatenation, binary handling |
| `deps` | Dependency analysis | Python & Node.js support, extensible |
| `git-info` | Git context extraction | Branch info, commits, diffs, error handling |
| `bundle` | Comprehensive context bundles | Multi-tool integration, selective inclusion |

## Community & Support

<div class="grid cards" markdown>

-   [:octicons-mark-github-24: **GitHub**](https://github.com/Shorzinator/ContextCraft)

    ---

    Source code, issues, and discussions

-   [:octicons-question-24: **FAQ**](help/faq.md)

    ---

    Frequently asked questions and common solutions

-   [:octicons-tools-24: **Contributing**](development/contributing.md)

    ---

    Guidelines for contributing to the project

-   [:octicons-bug-24: **Support**](help/support.md)

    ---

    Get help and report issues

</div>

## Ready to Get Started?

Choose your path to mastery:

[Get Started :material-arrow-right:](getting-started/installation.md){ .md-button .md-button--primary }
[View Examples :material-arrow-right:](examples/git-workflows.md){ .md-button }
[API Reference :material-arrow-right:](reference/main.md){ .md-button }
