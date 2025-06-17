# Bundler

::: codebrief.tools.bundler

## Overview

The `bundler` module provides comprehensive context aggregation functionality, combining multiple codebrief tools into structured, well-organized bundles. It orchestrates the execution of tree generation, Git context extraction, dependency analysis, and file flattening to create comprehensive project context documents.

## Key Features

- **Multi-Tool Integration**: Combines tree, git-info, deps, and flatten tools
- **Flexible Configuration**: Selective inclusion/exclusion of context sections
- **Structured Output**: Well-organized Markdown with table of contents
- **Path Flexibility**: Support for multiple flatten paths and custom configurations
- **Error Resilience**: Graceful handling of tool failures and missing components

## Functions

### create_bundle

Create a comprehensive context bundle combining multiple tools.

**Parameters:**
- `project_root` (Path): Root directory of the project
- `output_file_path` (Optional[Path]): Output file path (None for stdout)
- `exclude_tree` (bool, optional): Skip directory tree section (default: False)
- `exclude_git` (bool, optional): Skip Git context section (default: False)
- `exclude_deps` (bool, optional): Skip dependencies section (default: False)
- `exclude_files` (bool, optional): Skip flattened files section (default: False)
- `flatten_paths` (Optional[List[Path]]): Specific paths to flatten (default: [project_root])
- `git_log_count` (int, optional): Number of Git commits to include (default: 10)
- `git_full_diff` (bool, optional): Include full Git diff (default: False)
- `git_diff_options` (Optional[str]): Custom Git diff options (default: None)

**Returns:**
- None (outputs to file or stdout)

**Raises:**
- `FileNotFoundError`: If project_root doesn't exist
- `PermissionError`: If output file cannot be written
- Various exceptions from underlying tools (handled gracefully)

### Helper Functions

#### generate_tree_content
Generate directory tree content for the bundle.

**Parameters:**
- `project_root` (Path): Root directory
- `config_global_excludes` (List[str]): Global exclude patterns

**Returns:**
- `str`: Formatted tree content

#### generate_git_content
Generate Git context content for the bundle.

**Parameters:**
- `project_root` (Path): Root directory
- `log_count` (int): Number of commits
- `full_diff` (bool): Include full diff
- `diff_options` (Optional[str]): Custom diff options

**Returns:**
- `str`: Formatted Git content

#### generate_deps_content
Generate dependencies content for the bundle.

**Parameters:**
- `project_root` (Path): Root directory

**Returns:**
- `str`: Formatted dependencies content

#### generate_flatten_content
Generate flattened files content for the bundle.

**Parameters:**
- `project_root` (Path): Root directory
- `flatten_paths` (List[Path]): Paths to flatten
- `config_global_excludes` (List[str]): Global exclude patterns

**Returns:**
- `str`: Formatted flattened content

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from codebrief.tools.bundler import create_bundle

# Create complete bundle
create_bundle(
    project_root=Path("."),
    output_file_path=Path("project-bundle.md")
)
```

### Advanced Configuration

```python
# Create selective bundle for code review
create_bundle(
    project_root=Path("."),
    output_file_path=Path("review-bundle.md"),
    exclude_deps=True,
    flatten_paths=[Path("src"), Path("tests")],
    git_log_count=5,
    git_full_diff=True
)
```

### CLI Integration

```python
# This is how the CLI command uses the function
from codebrief.tools.bundler import create_bundle

def bundle_command(
    root_dir: Path,
    output: Optional[Path] = None,
    exclude_tree: bool = False,
    exclude_git: bool = False,
    exclude_deps: bool = False,
    exclude_files: bool = False,
    flatten: Optional[List[Path]] = None,
    git_log_count: int = 10,
    git_full_diff: bool = False,
    git_diff_options: Optional[str] = None,
):
    create_bundle(
        project_root=root_dir,
        output_file_path=output,
        exclude_tree=exclude_tree,
        exclude_git=exclude_git,
        exclude_deps=exclude_deps,
        exclude_files=exclude_files,
        flatten_paths=flatten or [root_dir],
        git_log_count=git_log_count,
        git_full_diff=git_full_diff,
        git_diff_options=git_diff_options,
    )
```

## Output Structure

The bundler creates well-organized Markdown documents:

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
│   └── 📁 codebrief/
└── 📁 tests/

## Git Context
# Git Context

## Repository Information
- **Current Branch:** main
- **Repository Status:** Clean working directory

## Recent Commits (Last 10)
[Git commit history...]

## Dependencies
# Dependencies

## Python Dependencies (pyproject.toml)
- typer: ^0.9.0
- rich: ^13.0.0

## Files: src/codebrief/tools
# --- File: src/codebrief/tools/bundler.py ---
[File contents...]

# --- File: src/codebrief/tools/git_provider.py ---
[File contents...]
```

## Bundle Sections

### Directory Tree Section
- Uses the `tree_generator` module
- Respects `.llmignore` and configuration patterns
- Provides visual project structure overview

### Git Context Section
- Uses the `git_provider` module
- Includes branch info, status, and commit history
- Optional full diff and custom diff options

### Dependencies Section
- Uses the `dependency_lister` module
- Analyzes Python and Node.js dependencies
- Supports multiple dependency file formats

### Files Section
- Uses the `flattener` module
- Aggregates file contents from specified paths
- Intelligent file filtering and binary file handling

## Error Handling

The bundler handles various error scenarios:

### Missing Tools
```python
# If a tool fails, the section is skipped with a note
create_bundle(Path("."))
# Output includes: "## Git Context\n*Git context unavailable*"
```

### Invalid Paths
```python
# Graceful handling of non-existent flatten paths
create_bundle(
    project_root=Path("."),
    flatten_paths=[Path("nonexistent")]
)
# Skips invalid paths, continues with valid ones
```

### Permission Issues
```python
# Clear error messages for file access issues
create_bundle(
    project_root=Path("."),
    output_file_path=Path("/etc/bundle.md")
)
# Raises PermissionError with helpful message
```

## Configuration Integration

Works seamlessly with codebrief's configuration system:

```toml
[tool.codebrief]
default_output_filename_bundle = "project-bundle.md"
global_exclude_patterns = ["*.pyc", "__pycache__/", ".venv/"]
```

## Performance Considerations

- **Parallel Processing**: Tools run independently where possible
- **Memory Efficient**: Streams output to files for large projects
- **Configurable Scope**: Selective inclusion reduces processing time
- **Caching**: Reuses configuration and ignore patterns across tools

## Testing

The module includes comprehensive test coverage:

- **7 test cases** covering core functionality
- **Helper function testing** for individual components
- **Integration testing** with real project structures
- **Error scenario testing** for robustness
- **Configuration integration** testing

## Dependencies

- **pathlib**: For path handling
- **typing**: For type annotations
- **io.StringIO**: For output capture and manipulation
- **codebrief.tools.tree_generator**: Directory tree generation
- **codebrief.tools.git_provider**: Git context extraction
- **codebrief.tools.dependency_lister**: Dependency analysis
- **codebrief.tools.flattener**: File content aggregation
- **codebrief.utils.config_manager**: Configuration management

## Related Modules

- [`tree_generator`](../tree_generator.md): Directory structure visualization
- [`git_provider`](git_provider.md): Git context extraction
- [`dependency_lister`](dependency_lister.md): Dependency analysis
- [`flattener`](../flattener.md): File content aggregation
- [`config_manager`](../config_manager.md): Configuration management
- [`main`](../main.md): CLI integration and command handling

## Best Practices

### Bundle Composition
```python
# For code review
create_bundle(
    exclude_deps=True,
    flatten_paths=[Path("src"), Path("tests")],
    git_log_count=5
)

# For documentation
create_bundle(
    exclude_git=True,
    flatten_paths=[Path("docs"), Path("README.md")]
)

# For debugging
create_bundle(
    git_full_diff=True,
    flatten_paths=[Path("src")]
)
```

### Performance Optimization
```python
# Large projects - selective flattening
create_bundle(
    flatten_paths=[Path("src/core")],  # Specific paths only
    exclude_deps=True,  # Skip if not needed
    git_log_count=3     # Limit Git history
)
```
