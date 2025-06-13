# Installation

Get ContextCraft up and running on your system in just a few minutes!

## Prerequisites

!!! info "System Requirements"
    - **Python**: 3.9 or higher
    - **Git**: For cloning the repository
    - **Poetry**: For dependency management (recommended)

### Installing Prerequisites

=== "macOS"

    ```bash
    # Install Python via Homebrew
    brew install python@3.11

    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 -
    ```

=== "Ubuntu/Debian"

    ```bash
    # Update package list
    sudo apt update

    # Install Python and pip
    sudo apt install python3.11 python3.11-pip python3.11-venv

    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 -
    ```

=== "Windows"

    ```powershell
    # Install Python from Microsoft Store or python.org
    # Then install Poetry
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

=== "Other Systems"

    Visit [Python.org](https://www.python.org/downloads/) for Python installation and [Poetry's documentation](https://python-poetry.org/docs/#installation) for Poetry setup.

## Installation Methods

### 🚀 Quick Install (Recommended)

The fastest way to get started with ContextCraft:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ContextCraft.git
cd ContextCraft

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Verify installation
contextcraft --version
```

### 📦 PyPI Installation (Coming Soon)

Once ContextCraft is published to PyPI, you'll be able to install it directly:

```bash
# This will be available soon!
pip install contextcraft
```

!!! note "PyPI Status"
    ContextCraft will be published to PyPI soon. For now, please use the source installation method above.

### 🛠️ Development Installation

For contributors and developers who want to work on ContextCraft itself:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ContextCraft.git
cd ContextCraft

# Install with development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests to verify everything works
poetry run pytest

# Activate the virtual environment
poetry shell
```

### 🐳 Docker Installation (Advanced)

For containerized environments:

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

ENTRYPOINT ["contextcraft"]
```

## Verification

After installation, verify that ContextCraft is working correctly:

### Basic Verification

```bash
# Check version
contextcraft --version

# View help
contextcraft --help

# Test tree generation
contextcraft tree --help
```

### Comprehensive Test

```bash
# Create a test directory
mkdir contextcraft-test
cd contextcraft-test

# Create some test files
echo "print('Hello, World!')" > hello.py
echo "# Test Project" > README.md
mkdir src
echo "def main(): pass" > src/main.py

# Test all commands
contextcraft tree
contextcraft flatten . --include "*.py"
contextcraft deps

# Clean up
cd ..
rm -rf contextcraft-test
```

## Configuration

### Shell Completion (Optional)

Enable command completion for your shell:

=== "Bash"

    ```bash
    # Add to ~/.bashrc
    eval "$(_CONTEXTCRAFT_COMPLETE=bash_source contextcraft)"
    ```

=== "Zsh"

    ```zsh
    # Add to ~/.zshrc
    eval "$(_CONTEXTCRAFT_COMPLETE=zsh_source contextcraft)"
    ```

=== "Fish"

    ```fish
    # Add to ~/.config/fish/config.fish
    eval (env _CONTEXTCRAFT_COMPLETE=fish_source contextcraft)
    ```

### Environment Variables

Configure ContextCraft behavior with environment variables:

```bash
# Set default output directory
export CONTEXTCRAFT_OUTPUT_DIR=~/context-outputs

# Enable debug mode
export CONTEXTCRAFT_DEBUG=1

# Set default config file location
export CONTEXTCRAFT_CONFIG=~/.contextcraft.toml
```

## Troubleshooting

### Common Issues

!!! warning "Python Version Issues"
    **Problem**: `contextcraft: command not found` after installation

    **Solution**: Ensure you're in the Poetry virtual environment:
    ```bash
    poetry shell
    # or use
    poetry run contextcraft --version
    ```

!!! warning "Permission Errors"
    **Problem**: Permission denied when installing Poetry or running commands

    **Solution**: Don't use `sudo` with Poetry. Install Poetry for your user only:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

!!! warning "Import Errors"
    **Problem**: `ModuleNotFoundError` when running ContextCraft

    **Solution**: Reinstall dependencies:
    ```bash
    poetry install --sync
    ```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](../help/troubleshooting.md)
2. Search [existing issues](https://github.com/YOUR_USERNAME/ContextCraft/issues)
3. Create a [new issue](https://github.com/YOUR_USERNAME/ContextCraft/issues/new) if needed

## Next Steps

Now that ContextCraft is installed:

- 📚 Read the [Quick Start Guide](quick-start.md)
- ⚙️ Set up [Configuration](configuration.md)
- 🎯 Follow the [Basic Usage Tutorial](../tutorials/basic-usage.md)
- 📖 Explore the [User Guide](../user-guide/cli-commands.md)

---

*Installation issues? We're here to help! Check our [Support page](../help/support.md) for assistance.*
