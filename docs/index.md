# Welcome to ContextCraft

<div align="center">
  <h2>A Powerful CLI Toolkit for LLM-Ready Project Context</h2>
  <p><em>Transform your codebase into comprehensive, structured context that Large Language Models love!</em></p>
</div>

---

**ContextCraft** is a sophisticated, production-ready Command Line Interface (CLI) toolkit designed to help developers generate comprehensive, structured context from their projects. Whether you're debugging with ChatGPT, explaining your codebase to Claude, or preparing documentation for any LLM, ContextCraft provides the perfect tools to create rich, contextual project summaries.

## Features

### Directory Tree Generation
Generate beautiful, hierarchical representations of your project structure with intelligent filtering and customization options.

### Code Flattening
Concatenate code from multiple files into a single, well-organized document with clear file markers and intelligent content handling.

### Dependency Analysis
Extract and analyze project dependencies across multiple languages and package managers (Python, Node.js, and more).

### Intelligent Ignore System
Sophisticated `.llmignore` file support with `.gitignore`-style syntax for precise control over what gets included.

### Advanced Configuration
Flexible configuration system via `pyproject.toml` with support for default outputs, global patterns, and project-specific settings.

### Rich CLI Experience
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
    ```

=== "Advanced Workflow"

    ```bash
    # Create comprehensive project context
    contextcraft tree --output tree.txt
    contextcraft flatten src/ --output code.md
    contextcraft deps --output dependencies.md

    # Use .llmignore for fine-grained control
    echo "*.log\n__pycache__/\n.venv/" > .llmignore
    ```

## Perfect For

<div class="grid cards" markdown>

-   :material-robot: **LLM Integration**

    ---

    Generate context that's perfectly formatted for ChatGPT, Claude, Copilot, and other AI coding assistants.

-   :material-bug: **Debugging**

    ---

    Quickly share your project structure and relevant code with others or AI tools for faster problem resolution.

-   :material-book-open: **Documentation**

    ---

    Create comprehensive project overviews for onboarding, code reviews, and technical documentation.

-   :material-rocket: **Development**

    ---

    Streamline your workflow with automated context generation for various development scenarios.

</div>

## Architecture

ContextCraft is built with modern Python best practices:

- **CLI Framework**: [Typer](https://typer.tiangolo.com/) for intuitive command-line interfaces
- **Rich Output**: [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- **Modular Design**: Clean separation between tools, utilities, and CLI commands
- **Comprehensive Testing**: 145+ tests with 85%+ coverage
- **Type Safety**: Full MyPy type checking for reliability
- **Code Quality**: Ruff, Bandit, and pre-commit hooks for maintainable code

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

</div>

## What's New in v1.0

!!! success "Production Ready Features"

    - **Complete Tool Suite**: Tree generation, code flattening, and dependency analysis
    - **Advanced Configuration**: `pyproject.toml` integration with type validation
    - **Sophisticated Ignore System**: `.llmignore` with full `.gitignore` syntax support
    - **Rich Error Handling**: Safe markup processing and user-friendly error messages
    - **Comprehensive Testing**: 145 tests covering edge cases and integrations
    - **Beautiful Documentation**: This comprehensive documentation site!

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
[View Examples :material-arrow-right:](examples/python-projects.md){ .md-button }
[API Reference :material-arrow-right:](reference/main.md){ .md-button }
