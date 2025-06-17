# Configuration

Configure codebrief to match your workflow and project needs. This guide covers all configuration options and best practices.

## 📁 Configuration Files

codebrief supports multiple configuration methods, applied in order of precedence:

1. **CLI Arguments** (highest precedence)
2. **Environment Variables**
3. **Project Configuration** (`pyproject.toml`)
4. **Default Values** (lowest precedence)

## 🛠️ Project Configuration

### pyproject.toml Integration

The recommended way to configure codebrief is through your project's `pyproject.toml` file:

```toml
[tool.codebrief]
# Default output filenames (relative to project root)
default_output_filename_tree = "docs/project-structure.txt"
default_output_filename_flatten = "docs/codebase-summary.md"
default_output_filename_deps = "docs/dependencies.md"
default_output_filename_git_info = "docs/git-context.md"
default_output_filename_bundle = "docs/project-bundle.md"

# Global patterns applied to all commands
global_include_patterns = [
    "*.py",
    "*.js",
    "*.ts",
    "*.md",
    "*.toml",
    "*.json"
]

global_exclude_patterns = [
    "*.log",
    "*.tmp",
    "*.cache",
    "__pycache__/",
    ".venv/",
    "node_modules/",
    ".git/",
    "build/",
    "dist/"
]
```

### Configuration Options Reference

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `default_output_filename_tree` | `string` | Default tree output filename | `None` |
| `default_output_filename_flatten` | `string` | Default flatten output filename | `None` |
| `default_output_filename_deps` | `string` | Default deps output filename | `None` |
| `default_output_filename_git_info` | `string` | Default git-info output filename | `None` |
| `default_output_filename_bundle` | `string` | Default bundle output filename | `None` |
| `global_include_patterns` | `list[string]` | Patterns to include globally | `[]` |
| `global_exclude_patterns` | `list[string]` | Patterns to exclude globally | `[]` |

### Configuration Validation

codebrief validates your configuration on startup:

```bash
# Check if your configuration is valid
codebrief tree --help  # Will show warnings for invalid config
```

!!! warning "Type Validation"
    codebrief validates configuration types and shows warnings for invalid values:

    ```toml
    [tool.codebrief]
    # ❌ Invalid: should be string
    default_output_filename_tree = 123

    # ❌ Invalid: should be list
    global_exclude_patterns = "*.log"

    # ✅ Valid
    default_output_filename_tree = "tree.txt"
    global_exclude_patterns = ["*.log", "*.tmp"]
    ```

## 🌍 Environment Variables

Configure codebrief behavior with environment variables:

### Core Configuration

```bash
# Set default output directory
export codebrief_OUTPUT_DIR="$HOME/codebrief-outputs"

# Set default configuration file path
export codebrief_CONFIG="$HOME/.codebrief.toml"

# Enable debug mode
export codebrief_DEBUG=1

# Set log level (DEBUG, INFO, WARNING, ERROR)
export codebrief_LOG_LEVEL=INFO
```

### Command-Specific Defaults

```bash
# Tree command defaults
export codebrief_TREE_OUTPUT="project-tree.txt"

# Flatten command defaults
export codebrief_FLATTEN_OUTPUT="project-code.md"
export codebrief_FLATTEN_INCLUDE="*.py,*.md"

# Deps command defaults
export codebrief_DEPS_OUTPUT="dependencies.md"

# Git-info command defaults
export codebrief_GIT_INFO_OUTPUT="git-context.md"
export codebrief_GIT_LOG_COUNT=10

# Bundle command defaults
export codebrief_BUNDLE_OUTPUT="project-bundle.md"
```

### Shell Configuration

Add to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

```bash
# ~/.bashrc or ~/.zshrc

# codebrief environment variables
export codebrief_OUTPUT_DIR="$HOME/Documents/codebrief"
export codebrief_LOG_LEVEL=WARNING

# Create output directory if it doesn't exist
[ ! -d "$codebrief_OUTPUT_DIR" ] && mkdir -p "$codebrief_OUTPUT_DIR"

# Optional: Add alias for common commands
alias ccf='codebrief flatten'
alias cct='codebrief tree'
alias ccd='codebrief deps'
alias ccg='codebrief git-info'
alias ccb='codebrief bundle'
```

## 📋 Ignore Patterns (.llmignore)

### Creating .llmignore Files

Create a `.llmignore` file in your project root with `.gitignore`-style syntax:

```gitignore
# .llmignore

# Build artifacts
build/
dist/
*.egg-info/

# Cache directories
__pycache__/
.mypy_cache/
.pytest_cache/
.ruff_cache/
node_modules/

# Virtual environments
.venv/
venv/
env/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Logs and temporary files
*.log
*.tmp
*.temp

# OS-specific files
.DS_Store
Thumbs.db

# Sensitive files
.env
secrets/
*.key
*.pem

# Large media files
*.jpg
*.png
*.gif
*.mp4
*.zip
*.tar.gz

# Keep important files (negation)
!README.md
!LICENSE
!pyproject.toml
!package.json
```

### Ignore Pattern Precedence

codebrief applies ignore patterns in this order:

1. **Core System Exclusions** (`.git`, etc.) - always ignored
2. **`.llmignore` patterns** - project-specific ignores
3. **Configuration `global_exclude_patterns`** - from `pyproject.toml`
4. **CLI `--exclude` options** - command-line excludes

### Advanced Ignore Patterns

```gitignore
# Directory-specific ignores
src/**/*.pyc
tests/**/fixtures/

# Conditional ignores
*.log
!important.log

# Complex patterns
**/.DS_Store
**/node_modules/
src/**/build/

# Glob patterns
*.{jpg,jpeg,png,gif}
{build,dist,output}/
```

## 🎯 Use Case Configurations

### Configuration for Python Projects

```toml
[tool.codebrief]
default_output_filename_tree = "docs/project-structure.txt"
default_output_filename_flatten = "docs/python-code.md"
default_output_filename_deps = "docs/python-deps.md"

global_include_patterns = [
    "*.py",
    "*.pyi",
    "*.md",
    "*.toml",
    "*.txt",
    "requirements*.txt"
]

global_exclude_patterns = [
    "__pycache__/",
    "*.pyc",
    ".mypy_cache/",
    ".pytest_cache/",
    ".venv/",
    "venv/",
    "build/",
    "dist/",
    "*.egg-info/"
]
```

### Configuration for Node.js Projects

```toml
[tool.codebrief]
default_output_filename_tree = "docs/project-structure.txt"
default_output_filename_flatten = "docs/js-code.md"
default_output_filename_deps = "docs/js-deps.md"

global_include_patterns = [
    "*.js",
    "*.ts",
    "*.jsx",
    "*.tsx",
    "*.json",
    "*.md",
    "*.yml",
    "*.yaml"
]

global_exclude_patterns = [
    "node_modules/",
    "*.min.js",
    "*.bundle.js",
    "build/",
    "dist/",
    ".next/",
    "coverage/",
    ".nyc_output/"
]
```

### Configuration for Multi-Language Projects

```toml
[tool.codebrief]
default_output_filename_tree = "docs/full-structure.txt"
default_output_filename_flatten = "docs/all-code.md"
default_output_filename_deps = "docs/all-deps.md"

global_include_patterns = [
    # Python
    "*.py",
    "*.pyi",

    # JavaScript/TypeScript
    "*.js",
    "*.ts",
    "*.jsx",
    "*.tsx",

    # Web
    "*.html",
    "*.css",
    "*.scss",

    # Config & Documentation
    "*.json",
    "*.toml",
    "*.yaml",
    "*.yml",
    "*.md",
    "*.txt",

    # Build files
    "Dockerfile",
    "Makefile",
    "requirements*.txt",
    "package.json"
]

global_exclude_patterns = [
    # Python
    "__pycache__/",
    "*.pyc",
    ".mypy_cache/",
    ".pytest_cache/",
    ".venv/",
    "venv/",

    # JavaScript
    "node_modules/",
    "*.min.js",
    "*.bundle.js",

    # Build artifacts
    "build/",
    "dist/",
    "output/",
    "target/",

    # IDE & OS
    ".vscode/",
    ".idea/",
    ".DS_Store",

    # Logs & cache
    "*.log",
    "*.cache",
    "logs/"
]
```

## 🔧 Advanced Configuration

### Custom Configuration File Location

```bash
# Use a custom config file
export codebrief_CONFIG="/path/to/custom-config.toml"

# Or specify per command
codebrief tree --config /path/to/custom-config.toml
```

### Profile-Based Configuration

Create different configuration profiles:

```bash
# Development profile
cp pyproject.toml pyproject.dev.toml
# Edit dev-specific settings

# Production profile
cp pyproject.toml pyproject.prod.toml
# Edit prod-specific settings

# Use profiles
codebrief_CONFIG=pyproject.dev.toml codebrief tree
codebrief_CONFIG=pyproject.prod.toml codebrief flatten .
```

### Template Configurations

Keep template configurations for new projects:

```bash
# Create templates directory
mkdir -p ~/.codebrief/templates

# Save project-specific templates
cp pyproject.toml ~/.codebrief/templates/python-web.toml
cp pyproject.toml ~/.codebrief/templates/cli-app.toml

# Copy template to new project
cp ~/.codebrief/templates/python-web.toml ./pyproject.toml
```

## 🐛 Troubleshooting Configuration

### Checking Current Configuration

```bash
# View current configuration (coming soon)
codebrief config show

# Test configuration with dry run
codebrief tree --dry-run
```

### Common Configuration Issues

!!! warning "Invalid Configuration Types"
    **Problem**: Configuration values are wrong type

    **Solution**: Check the types in your `pyproject.toml`:
    ```toml
    # ❌ Wrong
    global_exclude_patterns = "*.log"

    # ✅ Correct
    global_exclude_patterns = ["*.log"]
    ```

!!! warning "Path Resolution Issues"
    **Problem**: Output files created in wrong location

    **Solution**: Use relative paths in configuration:
    ```toml
    # ❌ Absolute paths (not portable)
    default_output_filename_tree = "/home/user/tree.txt"

    # ✅ Relative paths (portable)
    default_output_filename_tree = "docs/tree.txt"
    ```

!!! warning "Ignore Patterns Not Working"
    **Problem**: Files not being ignored as expected

    **Solution**: Check pattern syntax and precedence:
    ```bash
    # Debug which files are being ignored
    codebrief tree --verbose  # (future feature)
    ```

## 📚 Next Steps

Now that you understand configuration:

1. **Set up your project**: Add a `[tool.codebrief]` section to `pyproject.toml`
2. **Create ignore patterns**: Add a `.llmignore` file for project-specific exclusions
3. **Customize workflow**: Set environment variables for your shell
4. **Explore commands**: Check out [CLI Commands](../user-guide/cli-commands.md)

---

*Need help with configuration? Check our [Troubleshooting Guide](../help/troubleshooting.md) or [get support](../help/support.md).*
