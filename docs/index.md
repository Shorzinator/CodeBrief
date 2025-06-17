# Welcome to CodeBrief

!!! tip "Quick Start"
    Ready to streamline your LLM workflows? Jump to [Quick Start](getting-started/quick-start.md) or [Installation](getting-started/installation.md).

## The Missing Link Between Your Codebase and AI Assistants

**CodeBrief** is a production-ready Command Line Interface (CLI) toolkit designed to solve the core problem developers face when working with AI assistants: manually preparing context from their projects. Whether you're debugging with ChatGPT, explaining your codebase to Claude, or preparing documentation for any LLM, CodeBrief provides the essential tools to create rich, contextual project summaries in seconds, not minutes.

## Stop Copying Files. Start Solving Problems.

Developers waste 10+ minutes per day copying and pasting project files, directory structures, and configuration details to provide context every time they need AI assistance. CodeBrief reduces this to a single command that takes seconds.

## Core Problem Solved

Developers waste 5-10 minutes manually copying files, explaining project structure, and gathering context every time they need AI assistance. CodeBrief reduces this to a single command that takes seconds.

## Essential Features

### Directory Tree Generation
Generate hierarchical representations of your project structure with intelligent filtering and customization options.

### Code Flattening
Concatenate code from multiple files into a single, well-organized document with clear file markers and intelligent content handling.

### Dependency Analysis
Extract and analyze project dependencies across multiple languages and package managers (Python, Node.js, and more).

### Git Context Extraction
Comprehensive Git repository information including branch status, commit history, and change diffs for enhanced development context.

### Context Bundling
Powerful aggregation tool that combines directory trees, Git context, dependencies, and flattened code into structured, comprehensive bundles.

### Intelligent Ignore System
Sophisticated `.llmignore` file support with `.gitignore`-style syntax for precise control over what gets included.

### Advanced Configuration
Flexible configuration system via `pyproject.toml` with support for default outputs, global patterns, and project-specific settings.

### Clipboard Integration
Copy output directly to clipboard with `--to-clipboard` or `-c` flag on all commands. Cross-platform support with graceful error handling and user feedback.

## Quick Start

Get started with CodeBrief in minutes:

=== "pip"
    ```bash
    pip install codebrief
    ```

=== "poetry"
    ```bash
    poetry add codebrief
    ```

=== "Basic tree generation"
    ```bash
    codebrief tree
    ```

=== "Copy tree to clipboard"
    ```bash
    codebrief tree --to-clipboard
    ```

=== "Flatten Python files to a single output"
    ```bash
    codebrief flatten . --include "*.py" --output context.md
    ```

=== "Flatten Python files to clipboard"
    ```bash
    codebrief flatten . --include "*.py" -c
    ```

=== "Extract dependencies"
    ```bash
    codebrief deps --output deps.md
    ```

=== "Git context extraction"
    ```bash
    codebrief git-info --output git-context.md
    ```

=== "Bundle everything"
    ```bash
    codebrief bundle --output project-bundle.md
    ```

=== "Bundle to clipboard"
    ```bash
    codebrief bundle -c
    ```

=== "Complex bundle with specific paths"
    ```bash
    codebrief bundle \
        --output comprehensive-context.md \
        --flatten src/ --flatten tests/ \
        --git-log-count 10 --git-full-diff
    ```

=== "Bundle selective sections"
    ```bash
    codebrief bundle \
        --exclude-deps --exclude-git \
        --flatten src/core/ \
        --output focused-context.md
    ```

### Advanced Workflow

```bash
# Create comprehensive project context with bundle
codebrief bundle \
    --output complete-context.md \
    --git-log-count 15 \
    --flatten src/ tests/

# Focused code review bundle
codebrief bundle \
    --exclude-deps \
    --git-full-diff \
    --flatten src/ tests/ \
    --output review-bundle.md

# Use .llmignore for fine-grained control
echo "*.log\n__pycache__/\n.venv/" > .llmignore
```

## Primary Use Cases

<div class="grid cards" markdown>

-   **AI-Assisted Debugging**

    ---

    Generate focused context that helps LLMs understand your project structure and identify issues quickly.

-   **Code Reviews**

    ---

    Create comprehensive review bundles with Git context, code changes, and project structure for thorough reviews.

-   **Legacy Codebase Explanation**

    ---

    Quickly share your project structure, dependencies, and relevant code with team members or AI tools for faster understanding.

-   **Development Documentation**

    ---

    Create comprehensive project overviews for onboarding, code reviews, and technical documentation.

-   **Workflow Automation**

    ---

    Streamline your development workflow with automated context generation for various scenarios and CI/CD integration.

-   **Git-Based Context**

    ---

    Integrate with Git workflows for branch-specific context, commit analysis, and development progress tracking.

</div>

## Architecture

CodeBrief is built with modern Python best practices:

- **CLI Framework**: [Typer](https://typer.tiangolo.com/) for intuitive command-line interfaces
- **Rich Output**: [Rich](https://rich.readthedocs.io/) for clean terminal output
- **Modular Design**: Clean separation between tools, utilities, and CLI commands
- **Comprehensive Testing**: 175+ tests with 77%+ coverage
- **Security Compliant**: Bandit security scanning with proper subprocess handling
- **Code Quality**: Ruff, pre-commit hooks, and conventional commits for maintainable code
- **Professional Infrastructure**: Complete documentation, security policies, and contributor guidelines

## Documentation Sections

<div class="grid cards" markdown>

-   **Getting Started**

    ---

    Installation, quick start guide, and basic configuration

    [:octicons-arrow-right-24: Get Started](getting-started/installation.md)

-   **User Guide**

    ---

    Comprehensive guides for all CLI commands and features

    [:octicons-arrow-right-24: User Guide](user-guide/cli-commands.md)

-   **Tutorials**

    ---

    Step-by-step tutorials for common workflows and use cases

    [:octicons-arrow-right-24: Tutorials](tutorials/basic-usage.md)

-   **API Reference**

    ---

    Complete API documentation for all modules and functions

    [:octicons-arrow-right-24: API Reference](reference/main.md)

-   **Examples**

    ---

    Real-world examples for Git workflows, bundle patterns, and automation

    [:octicons-arrow-right-24: Examples](examples/git-workflows.md)

-   **Contributing**

    ---

    Developer guides, contribution guidelines, and community standards

    [:octicons-arrow-right-24: Contributing](development/contributing.md)

</div>

## What's New in v1.0.2

### Critical Fixes & Compatibility Improvements

**Installation Issues Resolved:**

- Fixed `ModuleNotFoundError: No module named 'src'` when installing via Poetry
- Improved Python version compatibility (`>=3.9,<4.0`)
- Resolved help system compatibility with Click/Typer versions
- Enhanced test suite reliability across environments

**Production Quality:**

- 175 comprehensive tests with 77% coverage
- Cross-platform compatibility verified
- Professional documentation and distribution
- Complete CLI integration with help documentation

## Core Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `tree` | Directory structure visualization | Rich console output, file filtering |
| `flatten` | Code file aggregation | Multi-file concatenation, binary handling |
| `deps` | Dependency analysis | Python & Node.js support, extensible |
| `git-info` | Git context extraction | Branch info, commits, diffs, status |
| `bundle` | Multi-tool context aggregation | Configurable, structured output |

## Community & Support

<div class="grid cards" markdown>

-   **Issues & Bug Reports**

    ---

    Found a bug or have a feature request? Open an issue with our detailed templates.

    [:octicons-arrow-right-24: Report Issues](https://github.com/Shorzinator/ContextCraft/issues)

-   **Discussions**

    ---

    Join the community discussion for questions, ideas, and collaboration.

    [:octicons-arrow-right-24: Join Discussion](https://github.com/Shorzinator/ContextCraft/discussions)

-   **Security**

    ---

    Report security vulnerabilities through our responsible disclosure process.

    [:octicons-arrow-right-24: Security Policy](https://github.com/Shorzinator/ContextCraft/security)

-   **Contributing**

    ---

    Help improve CodeBrief! Read our comprehensive contribution guidelines.

    [:octicons-arrow-right-24: Contribute](development/contributing.md)

</div>

## Quick Links

- **[Installation Guide](getting-started/installation.md)** - Get up and running in minutes
- **[CLI Commands Reference](user-guide/cli-commands.md)** - Complete command documentation
- **[Configuration Guide](getting-started/configuration.md)** - Advanced setup and customization
- **[Bundle Workflows](examples/bundle-workflows.md)** - Real-world usage examples
- **[Contributing Guidelines](development/contributing.md)** - Join the development community
- **[Security Policy](https://github.com/Shorzinator/ContextCraft/blob/main/SECURITY.md)** - Report vulnerabilities responsibly

---

<div align="center">
  <p><strong>Ready to transform your development workflow?</strong></p>
  <p><a href="getting-started/installation.md" class="md-button md-button--primary">Get Started Now</a></p>
</div>
