# Quick Start

Get up and running with codebrief in under 5 minutes! This guide will walk you through the most common use cases and essential commands.

## 🎯 Your First Context

Let's generate your first project context using a real example:

### Step 1: Basic Tree Generation

```bash
# Generate a simple directory tree
codebrief tree

# Save tree to a file
codebrief tree --output project-structure.txt
```

This creates a visual representation of your project structure:

```
📁 my-project/
├── 📄 README.md
├── 📄 pyproject.toml
├── 📁 src/
│   └── 📄 main.py
└── 📁 tests/
    └── 📄 test_main.py
```

### Step 2: Flatten Your Code

```bash
# Flatten all Python files
codebrief flatten . --include "*.py" --output code-context.md

# Flatten specific directory
codebrief flatten src/ --output src-code.md
```

This creates a single file containing all your code with clear separators:

```markdown
# --- File: src/main.py ---
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()


# --- File: tests/test_main.py ---
import pytest
from src.main import hello_world

def test_hello_world():
    # Test implementation here
    pass
```

### Step 3: Analyze Dependencies

```bash
# Analyze project dependencies
codebrief deps --output dependencies.md
```

This generates a comprehensive dependency report:

```markdown
# Project Dependencies

## Python Dependencies

### Main Dependencies (pyproject.toml)
- typer: ^0.9.0
- rich: ^13.0.0
- pathspec: ^0.12.1

### Development Dependencies
- pytest: ^7.0.0
- mypy: ^1.0.0
```

## 🎨 Customizing Output

### Using Include/Exclude Patterns

```bash
# Include only specific file types
codebrief flatten . --include "*.py" --include "*.md" --include "*.toml"

# Exclude certain patterns
codebrief flatten . --exclude "*.log" --exclude "__pycache__/" --exclude ".git/"

# Combine both
codebrief flatten . \
  --include "*.py" --include "*.md" \
  --exclude "tests/" --exclude ".venv/"
```

### Ignoring Files with .llmignore

Create a `.llmignore` file in your project root (similar to `.gitignore`):

```gitignore
# .llmignore
*.log
*.tmp
__pycache__/
.venv/
.git/
node_modules/
.mypy_cache/
.pytest_cache/

# Keep important config files
!pyproject.toml
!package.json
```

Now all codebrief commands will respect these ignore patterns:

```bash
# This will automatically exclude files matching .llmignore patterns
codebrief tree
codebrief flatten .
```

## ⚙️ Configuration

### Project Configuration

Create a `pyproject.toml` configuration section:

```toml
[tool.codebrief]
default_output_filename_tree = "project-tree.txt"
default_output_filename_flatten = "project-code.md"
default_output_filename_deps = "project-deps.md"
global_exclude_patterns = ["*.log", "tmp/"]
global_include_patterns = ["*.py", "*.md", "*.toml"]
```

Now you can run commands without specifying output files:

```bash
# Uses default output filenames from config
codebrief tree      # Creates project-tree.txt
codebrief flatten . # Creates project-code.md
codebrief deps      # Creates project-deps.md
```

## 🚀 Common Workflows

### Workflow 1: Debugging with LLMs

When you need to share your project with ChatGPT or Claude for debugging:

```bash
# Create comprehensive context
codebrief tree --output structure.txt
codebrief flatten src/ --include "*.py" --output code.md
codebrief deps --output deps.md

# Now copy the contents to your LLM chat
```

### Workflow 2: Code Review Preparation

Prepare context for code reviews:

```bash
# Focus on source code and tests
codebrief flatten . \
  --include "*.py" \
  --exclude "__pycache__/" \
  --exclude ".venv/" \
  --output review-context.md

# Include project structure
codebrief tree --output project-overview.txt
```

### Workflow 3: Documentation Generation

Generate project documentation:

```bash
# Create comprehensive project summary
codebrief tree --output docs/project-structure.txt
codebrief flatten . \
  --include "*.py" --include "*.md" --include "*.toml" \
  --output docs/codebase-summary.md
codebrief deps --output docs/dependencies.md
```

## 🎯 Pro Tips

!!! tip "Combine with Other Tools"
    ```bash
    # Combine with grep for specific searches
    codebrief flatten . --include "*.py" | grep -n "TODO"

    # Count lines of code
    codebrief flatten . --include "*.py" | wc -l

    # Use with clipboard (macOS)
    codebrief tree | pbcopy
    ```

!!! tip "Large Codebases"
    For large projects, be selective:
    ```bash
    # Focus on specific directories
    codebrief flatten src/core/ src/api/ --output core-api.md

    # Use more specific include patterns
    codebrief flatten . --include "src/**/*.py" --include "tests/**/*.py"
    ```

!!! tip "CI/CD Integration"
    ```bash
    # Generate context for CI pipelines
    codebrief tree --output artifacts/project-structure.txt
    codebrief deps --output artifacts/dependencies.md
    ```

## 🔍 Exploring Your Output

### Tree Output Features

The tree command provides rich information:

- 📁 Directory indicators
- 📄 File indicators
- Size information (when available)
- Nested structure visualization
- Respect for ignore patterns

### Flattened Code Features

The flatten command creates LLM-friendly output:

- Clear file separators with `# --- File: path/to/file.py ---`
- Preserves original formatting and indentation
- Handles binary files gracefully
- Maintains relative path context
- Efficient processing of large codebases

### Dependency Analysis Features

The deps command provides comprehensive insights:

- Multi-language support (Python, Node.js, etc.)
- Dependency grouping (main, dev, optional)
- Version information where available
- Clean Markdown formatting
- Extensible architecture for new languages

## 🚦 What's Next?

Now that you've mastered the basics:

1. **Explore Advanced Features**: Check out [User Guide](../user-guide/cli-commands.md) for detailed command options
2. **Learn Configuration**: Deep dive into [Configuration](configuration.md) for project setup
3. **Follow Tutorials**: Try our [Tutorials](../tutorials/basic-usage.md) for specific use cases
4. **See Examples**: Browse [Examples](../examples/python-projects.md) for real-world projects

## 🆘 Need Help?

- 📖 Read the [User Guide](../user-guide/cli-commands.md)
- ❓ Check the [FAQ](../help/faq.md)
- 🐛 Report issues on [GitHub](https://github.com/YOUR_USERNAME/codebrief/issues)
- 💬 Get [Support](../help/support.md)

---

*Ready to become a codebrief power user? Continue to the [User Guide](../user-guide/cli-commands.md)!*
