# Git Provider

::: codebrief.tools.git_provider

## Overview

The `git_provider` module provides comprehensive Git repository context extraction functionality. It safely executes Git commands to gather repository information including branch status, commit history, and change diffs.

## Key Features

- **Safe Git Command Execution**: Robust subprocess handling with timeout protection
- **Comprehensive Context**: Branch info, status, commits, and diffs
- **Error Resilience**: Graceful handling of non-Git repos and command failures
- **Security Compliant**: Bandit-approved subprocess usage for Git operations
- **Configurable Output**: Flexible diff options and commit count limits

## Functions

### get_git_context

Extract complete Git repository context information.

**Parameters:**
- `project_root` (Path): Root directory of the project/repository
- `log_count` (int, optional): Number of recent commits to include (default: 10)
- `full_diff` (bool, optional): Include full diff of uncommitted changes (default: False)
- `diff_options` (str, optional): Custom git diff options (default: None)

**Returns:**
- `str`: Formatted Markdown string containing Git context

**Raises:**
- No exceptions raised - all errors are handled gracefully and returned as informative messages

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from contextcraft.tools.git_provider import get_git_context

# Get basic Git context
context = get_git_context(Path("."))
print(context)
```

### Advanced Usage

```python
# Get detailed context with full diff
context = get_git_context(
    project_root=Path("/path/to/repo"),
    log_count=5,
    full_diff=True,
    diff_options="--stat --color=never"
)
```

### CLI Integration

```python
# This is how the CLI command uses the function
from contextcraft.tools.git_provider import get_git_context

def git_info_command(
    root_dir: Path,
    output: Optional[Path] = None,
    log_count: int = 10,
    full_diff: bool = False,
    diff_options: Optional[str] = None,
):
    context = get_git_context(
        project_root=root_dir,
        log_count=log_count,
        full_diff=full_diff,
        diff_options=diff_options,
    )

    if output:
        output.write_text(context, encoding="utf-8")
    else:
        console.print(context)
```

## Output Format

The function returns a structured Markdown document:

```markdown
# Git Context

## Repository Information
- **Current Branch:** main
- **Repository Status:** Clean working directory

## Recent Commits (Last 10)
1. **feat: add new feature** (2024-01-15 14:30:25)
   - Author: Developer <dev@example.com>
   - Hash: abc123f

2. **fix: resolve parsing issue** (2024-01-14 09:15:42)
   - Author: Developer <dev@example.com>
   - Hash: def456a

## Uncommitted Changes
*No uncommitted changes*

## Full Diff
[Included when full_diff=True]

## Diff (--stat)
[Included when diff_options provided]
```

## Error Handling

The module handles various error scenarios gracefully:

### Non-Git Repository
```python
context = get_git_context(Path("/tmp"))
# Returns: "# Git Context\n\nNot a Git repository or no Git history.\n"
```

### Git Not Available
```python
# When Git is not installed
# Returns: "# Git Context\n\nError: Git executable not found..."
```

### Permission Issues
```python
# When Git commands fail due to permissions
# Returns appropriate error message with context
```

## Security Considerations

- All subprocess calls use explicit command arrays (not shell strings)
- Timeout protection prevents hanging on slow Git operations
- Input validation ensures safe path handling
- Bandit security compliance with appropriate `# nosec` annotations

## Testing

The module includes comprehensive test coverage:

- **13 test cases** covering all functionality
- **Error scenario testing** for robustness
- **Integration testing** with real Git repositories
- **Parameter validation** testing
- **Security compliance** verification

## Configuration Integration

Works seamlessly with ContextCraft's configuration system:

```toml
[tool.contextcraft]
default_output_filename_git_info = "git-context.md"
```

## Dependencies

- **subprocess**: For Git command execution
- **pathlib**: For path handling
- **typing**: For type annotations

## Related Modules

- [`bundler`](bundler.md): Uses git_provider for bundle Git sections
- [`config_manager`](../config_manager.md): Provides configuration defaults
- [`main`](../main.md): CLI integration and command handling
