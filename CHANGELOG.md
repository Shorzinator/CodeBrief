# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of ContextCraft CLI toolkit
- Core functionality for project context generation

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 13-Jun-2025

### Added
- **Tree Generation**: Smart directory tree visualization with filtering
- **Code Flattening**: Concatenate multiple files into organized documents
- **Dependency Analysis**: Multi-language dependency extraction (Python, Node.js)
- **Git Context**: Current branch, status, and commit history
- **Context Bundling**: Aggregate multiple tools into comprehensive bundles
- **Intelligent Filtering**: Support for `.llmignore` files and global patterns
- **CLI Interface**: Complete command-line interface with Typer and Rich
- **Configuration**: Support for `pyproject.toml` configuration
- **Documentation**: Comprehensive documentation with MkDocs
- **Testing**: 165+ tests with 77% coverage
- **Quality Assurance**: Ruff linting, formatting, and pre-commit hooks
- **Security**: Bandit security scanning
- **CI/CD**: GitHub Actions for automated testing and quality checks

### Technical Details
- **Languages**: Python 3.9+ support
- **Dependencies**: Typer, Rich, Pathspec, TOML
- **Development**: Poetry for dependency management
- **Code Quality**: Ruff, Pytest, Bandit, Pre-commit
- **Documentation**: MkDocs with Material theme

### Performance
- Fast directory traversal with intelligent filtering
- Efficient file processing with binary detection
- Optimized Git operations with configurable depth
- Memory-efficient large file handling

---

## Release Notes

### Version 0.1.0
This is the initial release of ContextCraft, a powerful CLI toolkit designed to generate comprehensive project context for Large Language Models (LLMs).

**Key Features:**
- Complete project analysis and documentation generation
- Intelligent filtering and content aggregation
- Professional-grade CLI interface
- Extensive testing and quality assurance
- Comprehensive documentation

**Getting Started:**
```bash
pip install contextcraft
contextcraft --help
```

**Documentation:** [https://contextcraft.readthedocs.io](https://contextcraft.readthedocs.io)

---

For detailed information about each release, see the [GitHub Releases](https://github.com/Shorzinator/ContextCraft/releases) page.
