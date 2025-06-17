# Basic Usage Tutorial

Learn codebrief through hands-on examples and real-world scenarios. This tutorial covers the most common use cases and workflows.

## 🎯 Tutorial Overview

In this tutorial, you'll learn to:

1. Generate your first project tree
2. Flatten code for LLM consumption
3. Analyze project dependencies
4. Combine commands for comprehensive context
5. Set up efficient workflows

## 📋 Prerequisites

- codebrief installed and working
- A sample project to work with (or use our examples)

!!! tip "Using Your Own Project"
    While this tutorial uses examples, you can follow along with any project. Adjust the commands and patterns to match your project structure.

## 🚀 Hands-On Walkthrough

### Step 1: Setting Up a Sample Project

Let's create a sample project to demonstrate codebrief features:

```bash
# Create a sample Python project
mkdir codebrief-demo
cd codebrief-demo

# Create project structure
mkdir -p src/myapp tests docs
touch README.md pyproject.toml

# Create some Python files
cat > src/myapp/__init__.py << 'EOF'
"""My demo application."""
__version__ = "0.1.0"
EOF

cat > src/myapp/main.py << 'EOF'
"""Main application module."""

def greet(name: str = "World") -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

def main():
    """Entry point for the application."""
    message = greet("codebrief")
    print(message)

if __name__ == "__main__":
    main()
EOF

cat > tests/test_main.py << 'EOF'
"""Tests for the main module."""
import pytest
from src.myapp.main import greet

def test_greet_default():
    """Test default greeting."""
    assert greet() == "Hello, World!"

def test_greet_custom():
    """Test custom greeting."""
    assert greet("Alice") == "Hello, Alice!"
EOF

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "myapp"
version = "0.1.0"
description = "A demo application"
authors = ["Shourya Maheshwari <shorz2905@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
EOF

cat > README.md << 'EOF'
# My Demo App

A simple demonstration application for codebrief tutorial.

## Features

- Greeting functionality
- Command-line interface
- Comprehensive tests

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m myapp.main
```
EOF
```

Your project structure should now look like:

```
codebrief-demo/
├── README.md
├── pyproject.toml
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
└── docs/
```

### Step 2: Your First Tree

Let's generate a visual representation of our project:

```bash
# Basic tree generation
codebrief tree
```

You'll see output like:

```
📁 codebrief-demo/
├── 📄 README.md
├── 📄 pyproject.toml
├── 📁 src/
│   └── 📁 myapp/
│       ├── 📄 __init__.py
│       └── 📄 main.py
├── 📁 tests/
│   └── 📄 test_main.py
└── 📁 docs/
```

Now let's save it to a file:

```bash
# Save tree to file
codebrief tree --output project-structure.txt

# Check the output
cat project-structure.txt
```

### Step 3: Flattening Your Code

Let's create a comprehensive code context for an LLM:

```bash
# Flatten all Python files
codebrief flatten . --include "*.py" --output code-context.md

# View the result
head -20 code-context.md
```

The output will look like:

```markdown
# --- File: src/myapp/__init__.py ---
"""My demo application."""
__version__ = "0.1.0"


# --- File: src/myapp/main.py ---
"""Main application module."""

def greet(name: str = "World") -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

def main():
    """Entry point for the application."""
    message = greet("codebrief")
    print(message)

if __name__ == "__main__":
    main()


# --- File: tests/test_main.py ---
"""Tests for the main module."""
import pytest
from src.myapp.main import greet

def test_greet_default():
    """Test default greeting."""
    assert greet() == "Hello, World!"

def test_greet_custom():
    """Test custom greeting."""
    assert greet("Alice") == "Hello, Alice!"
```

### Step 4: Including Documentation and Config

Let's create a more comprehensive context including documentation:

```bash
# Include Python files, Markdown, and TOML files
codebrief flatten . \
  --include "*.py" \
  --include "*.md" \
  --include "*.toml" \
  --output comprehensive-context.md

# Check what we got
wc -l comprehensive-context.md
```

### Step 5: Analyzing Dependencies

Now let's analyze our project dependencies:

```bash
# Generate dependency report
codebrief deps --output dependencies.md

# View the dependencies
cat dependencies.md
```

You'll see:

```markdown
# Project Dependencies

## Python Dependencies

### Main Dependencies (pyproject.toml)
- click: ^8.0.0

### Development Dependencies (pyproject.toml)
- pytest: ^7.0.0
- black: ^23.0.0
```

## 🎨 Customizing Your Workflow

### Setting Up .llmignore

Create a `.llmignore` file to control what gets included:

```bash
cat > .llmignore << 'EOF'
# Ignore cache and temporary files
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/

# Ignore build artifacts
build/
dist/
*.egg-info/

# Ignore IDE files
.vscode/
.idea/
*.swp

# Keep important config files
!pyproject.toml
!README.md
EOF
```

Now test the ignore patterns:

```bash
# Create some files that should be ignored
mkdir __pycache__
touch __pycache__/main.cpython-39.pyc
touch temp.log

# Generate tree - these should be excluded
codebrief tree
```

### Using Configuration

Set up project configuration in `pyproject.toml`:

```bash
# Add codebrief configuration
cat >> pyproject.toml << 'EOF'

[tool.codebrief]
default_output_filename_tree = "docs/project-structure.txt"
default_output_filename_flatten = "docs/codebase-summary.md"
default_output_filename_deps = "docs/dependencies.md"
global_exclude_patterns = ["*.log", "*.tmp"]
global_include_patterns = ["*.py", "*.md", "*.toml"]
EOF
```

Now you can use commands without specifying output files:

```bash
# Uses default output filenames from config
codebrief tree      # Creates docs/project-structure.txt
codebrief flatten . # Creates docs/codebase-summary.md
codebrief deps      # Creates docs/dependencies.md

# Check that files were created
ls docs/
```

## 🎯 Common Workflows

### Workflow 1: Preparing for Code Review

```bash
# Create focused context for code review
mkdir -p review

# Get project structure
codebrief tree src/ tests/ --output review/structure.txt

# Get source code and tests
codebrief flatten . \
  --include "*.py" \
  --exclude "__pycache__/" \
  --output review/code-changes.md

# Get configuration files
codebrief flatten . \
  --include "*.toml" --include "*.yaml" --include "*.json" \
  --output review/config-files.md

echo "Review context prepared in review/ directory"
ls review/
```

### Workflow 2: Creating LLM Context

```bash
# Create comprehensive context for LLM assistance
mkdir -p llm-context

# Project overview
codebrief tree --output llm-context/structure.txt

# All relevant code
codebrief flatten . \
  --include "*.py" --include "*.md" \
  --exclude "tests/" \
  --output llm-context/source-code.md

# Dependencies for context
codebrief deps --output llm-context/dependencies.md

# Create a combined context file
cat > llm-context/README.md << 'EOF'
# Project Context for LLM

This directory contains comprehensive project context:

- `structure.txt`: Project directory structure
- `source-code.md`: All source code (excluding tests)
- `dependencies.md`: Project dependencies

## How to Use

Copy the contents of these files to your LLM conversation for context about this project.
EOF

echo "LLM context prepared in llm-context/ directory"
ls llm-context/
```

### Workflow 3: Documentation Generation

```bash
# Generate documentation context
mkdir -p documentation

# Get all documentation files
codebrief flatten . \
  --include "*.md" --include "*.rst" \
  --output documentation/all-docs.md

# Get project structure for documentation
codebrief tree --output documentation/project-map.txt

# Get configuration for setup documentation
codebrief flatten . \
  --include "*.toml" --include "*.cfg" --include "*.ini" \
  --output documentation/configuration.md

echo "Documentation context prepared"
ls documentation/
```

## 🔄 Iterative Workflows

### Making Changes and Re-generating Context

```bash
# Make a change to your code
echo '
def farewell(name: str = "World") -> str:
    """Return a farewell message."""
    return f"Goodbye, {name}!"
' >> src/myapp/main.py

# Regenerate context to see the changes
codebrief flatten src/ --include "*.py" --output updated-code.md

# Compare with previous version
diff code-context.md updated-code.md
```

### Selective Context Updates

```bash
# Only update the main module context
codebrief flatten src/myapp/main.py --output main-module-only.md

# Only update tests
codebrief flatten tests/ --include "*.py" --output tests-only.md

# Combine specific parts
cat main-module-only.md tests-only.md > focused-context.md
```

## 🎉 Advanced Techniques

### Using Shell Scripting

Create a script to automate your context generation:

```bash
# Create a context generation script
cat > generate-context.sh << 'EOF'
#!/bin/bash

# codebrief automation script
echo "Generating comprehensive project context..."

# Create output directory
mkdir -p context-output

# Generate all contexts
echo "📁 Generating project structure..."
codebrief tree --output context-output/structure.txt

echo "📄 Generating source code context..."
codebrief flatten src/ --include "*.py" --output context-output/source-code.md

echo "🧪 Generating test context..."
codebrief flatten tests/ --include "*.py" --output context-output/tests.md

echo "📋 Generating dependencies..."
codebrief deps --output context-output/dependencies.md

echo "📝 Generating documentation..."
codebrief flatten . --include "*.md" --output context-output/docs.md

echo "✅ Context generation complete! Check context-output/ directory"
ls -la context-output/
EOF

chmod +x generate-context.sh
./generate-context.sh
```

### Integration with Git Hooks

Set up automatic context generation on commits:

```bash
# Create a git hook (if you're using git)
mkdir -p .git/hooks

cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Auto-generate context on commit

echo "Updating project context..."
codebrief tree --output docs/project-structure.txt
codebrief flatten . --include "*.py" --include "*.md" --output docs/project-context.md

# Add the generated files to the commit
git add docs/project-structure.txt docs/project-context.md
EOF

chmod +x .git/hooks/pre-commit
```

## 🎓 What You've Learned

Congratulations! You've learned:

- ✅ How to generate project trees with `codebrief tree`
- ✅ How to flatten code for LLM consumption with `codebrief flatten`
- ✅ How to analyze dependencies with `codebrief deps`
- ✅ How to use `.llmignore` files for fine-grained control
- ✅ How to configure codebrief via `pyproject.toml`
- ✅ How to create efficient workflows for different use cases
- ✅ How to automate context generation with scripts

## 🚀 Next Steps

Now that you're comfortable with the basics:

1. **Explore Advanced Features**: Try [Advanced Workflows](advanced-workflows.md)
2. **Learn LLM Integration**: Check out [LLM Integration](llm-integration.md)
3. **Set Up Automation**: Learn [CI/CD Integration](cicd-integration.md)
4. **Browse Examples**: See [Real Project Examples](../examples/python-projects.md)

## 🧹 Cleanup

If you created the demo project for this tutorial:

```bash
# Clean up the demo project
cd ..
rm -rf codebrief-demo
```

---

*Ready for more advanced techniques? Continue to [Advanced Workflows](advanced-workflows.md)!*
