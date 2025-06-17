# Contributing to codebrief

Thank you for your interest in contributing to codebrief! We welcome contributions from developers of all skill levels. This guide will help you get started with contributing to our project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**: codebrief requires Python 3.9 or higher
- **Poetry**: For dependency management and virtual environments
- **Git**: For version control
- **Pre-commit**: For automated code quality checks

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/codebrief.git
   cd codebrief
   ```

2. **Install Dependencies**
   ```bash
   # Install all dependencies including development tools
   poetry install --with dev
   ```

3. **Set Up Pre-commit Hooks**
   ```bash
   # Install pre-commit hooks for automated quality checks
   poetry run pre-commit install
   ```

4. **Verify Installation**
   ```bash
   # Run tests to ensure everything is working
   poetry run pytest

   # Run the CLI to verify installation
   poetry run codebrief --help
   ```

## 🤝 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new functionality
- **📝 Documentation**: Improve or add documentation
- **🧪 Tests**: Add or improve test coverage
- **🔧 Code**: Fix bugs or implement new features
- **🎨 UI/UX**: Improve the CLI interface and user experience

## 🐛 Reporting Bugs

Before creating a bug report, please check the [existing issues](https://github.com/Shorzinator/codebrief/issues) to avoid duplicates.

### Bug Report Template

When reporting bugs, please use our [issue template](.github/ISSUE_TEMPLATE.md) and include:

- **Clear Description**: What happened vs. what you expected
- **Reproduction Steps**: Detailed steps to reproduce the issue
- **Environment**: OS, Python version, codebrief version
- **Error Messages**: Full error messages and stack traces
- **Sample Files**: Minimal example files if relevant

**Example:**
```markdown
**Bug Description**
The `codebrief tree` command crashes when encountering symlinks.

**Steps to Reproduce**
1. Create a symlink: `ln -s /path/to/target symlink`
2. Run: `codebrief tree`
3. Observe the error

**Expected Behavior**
The command should handle symlinks gracefully.

**Environment**
- OS: macOS 14.0
- Python: 3.11.5
- codebrief: 0.1.0
```

## ✨ Requesting Features

We love feature requests! Please check [existing feature requests](https://github.com/Shorzinator/codebrief/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) first.

### Feature Request Guidelines

- **Clear Use Case**: Explain the problem you're trying to solve
- **Proposed Solution**: Describe your ideal solution
- **Alternatives**: Consider alternative approaches
- **Implementation**: Suggest how it might be implemented
- **Breaking Changes**: Note any potential breaking changes

## 🔄 Development Workflow

### Branching Strategy

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make Your Changes**
   - Write code following our [coding standards](#coding-standards)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run the full test suite
   poetry run pytest

   # Run with coverage
   poetry run pytest --cov=src/codebrief --cov-report=html

   # Run pre-commit checks
   poetry run pre-commit run --all-files
   ```

4. **Commit Your Changes**
   ```bash
   # Use conventional commit format
   git commit -m "feat: add support for YAML configuration files"
   git commit -m "fix: handle symlinks in tree generation"
   git commit -m "docs: update installation instructions"
   ```

## 📏 Coding Standards

We maintain high code quality standards using automated tools:

### Code Style

- **Formatter**: [Ruff](https://github.com/astral-sh/ruff) for consistent formatting
- **Linter**: Ruff for code quality and style enforcement
- **Line Length**: 88 characters maximum
- **Quotes**: Double quotes for strings
- **Imports**: Sorted and organized automatically

### Code Quality Tools

```bash
# Format code
poetry run ruff format

# Lint code
poetry run ruff check

# Fix auto-fixable issues
poetry run ruff check --fix

# Security scanning
poetry run bandit -r src/
```

### Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear commit history:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

**Examples:**
```bash
feat(tree): add support for custom tree symbols
fix(bundler): resolve encoding issues with non-UTF8 files
docs: add examples for advanced configuration
test: improve coverage for git provider module
```

### Type Hints

- Use type hints for all function parameters and return values
- Import types from `typing` module when needed
- Use `Optional[T]` for nullable values
- Document complex types in docstrings

### Documentation

- **Docstrings**: Use Google-style docstrings for all public functions
- **Comments**: Explain complex logic and business decisions
- **README**: Update README.md for user-facing changes
- **API Docs**: Update API documentation for new features

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── tools/           # Tool-specific tests
├── utils/           # Utility function tests
├── conftest.py      # Shared test fixtures
└── test_main.py     # CLI integration tests
```

### Writing Tests

1. **Test Coverage**: Aim for 80%+ coverage for new code
2. **Test Types**:
   - Unit tests for individual functions
   - Integration tests for CLI commands
   - Edge case testing for error conditions

3. **Test Naming**: Use descriptive test names
   ```python
   def test_tree_generator_handles_permission_errors():
       """Test that tree generation gracefully handles permission errors."""
   ```

4. **Fixtures**: Use pytest fixtures for common test data
5. **Assertions**: Prefer content-based assertions over brittle snapshot tests

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/tools/test_tree_generator.py

# Run with coverage
poetry run pytest --cov=src/codebrief --cov-report=html

# Run tests matching a pattern
poetry run pytest -k "test_tree"
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update Documentation**: Ensure all documentation is current
2. **Add Tests**: Include tests for new functionality
3. **Run Quality Checks**: Ensure all pre-commit hooks pass
4. **Update Changelog**: Add entry to CHANGELOG.md if applicable

### PR Guidelines

1. **Clear Title**: Use conventional commit format
2. **Detailed Description**: Explain what and why
3. **Link Issues**: Reference related issues with `Fixes #123`
4. **Small PRs**: Keep changes focused and reviewable
5. **Draft PRs**: Use draft PRs for work-in-progress

### PR Template

We provide a [PR template](.github/PULL_REQUEST_TEMPLATE.md) that includes:

- Description of changes
- Type of change (bug fix, feature, etc.)
- Testing checklist
- Documentation updates
- Breaking changes

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Reviewers will test functionality
4. **Documentation**: Ensure docs are clear and complete
5. **Merge**: Maintainers will merge approved PRs

## 🚀 Release Process

### Version Management

- We use [Semantic Versioning](https://semver.org/)
- Versions are managed through Poetry
- Releases are tagged in Git

### Release Checklist

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release PR
4. Tag release after merge
5. Publish to PyPI (maintainers only)

## 🆘 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check our [comprehensive docs](docs/)

### Maintainer Contact

For sensitive issues or questions, contact the maintainers directly through GitHub.

## 🎉 Recognition

Contributors are recognized in:

- CHANGELOG.md for significant contributions
- GitHub contributors page
- Release notes for major features

Thank you for contributing to codebrief! Your efforts help make this tool better for the entire developer community. 🚀
