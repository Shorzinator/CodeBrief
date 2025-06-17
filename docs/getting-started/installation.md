# Installation

Get codebrief up and running on your system in just a few minutes!

## Prerequisites

!!! info "System Requirements"
    - **Python**: 3.9 or higher
    - **Git**: For cloning the repository
    - **Poetry**: For dependency management (recommended)

### Installing Prerequisites

#### macOS

```bash
# Install Python via Homebrew
brew install python@3.11

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.11 python3.11-pip python3.11-venv

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows

```powershell
# Install Python from Microsoft Store or python.org
# Then install Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

#### Other Systems

Visit [Python.org](https://www.python.org/downloads/) for Python installation and [Poetry's documentation](https://python-poetry.org/docs/#installation) for Poetry setup.

## Installation Methods

### 🚀 Quick Install (Recommended)

The fastest way to get started with codebrief:

```bash
# Clone the repository
git clone https://github.com/Shorzinator/codebrief.git
cd codebrief

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Verify installation
codebrief --version
```

### 📦 PyPI Installation


```bash
pip install codebrief
```

### 🛠️ Development Installation

For contributors and developers who want to work on codebrief itself:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/codebrief.git
cd codebrief

# Install with development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests to verify everything works
poetry run pytest

# Activate the virtual environment
poetry shell
```

## Verification

After installation, verify that codebrief is working correctly:

### Basic Verification

```bash
# Check version
codebrief --version

# View help
codebrief --help

# Test tree generation
codebrief tree --help
```

### Comprehensive Test

```bash
# Create a test directory
mkdir codebrief-test
cd codebrief-test

# Create some test files
echo "print('Hello, World!')" > hello.py
echo "# Test Project" > README.md
mkdir src
echo "def main(): pass" > src/main.py

# Test all commands
codebrief tree
codebrief flatten . --include "*.py"
codebrief deps

# Clean up
cd ..
rm -rf codebrief-test
```

### Environment Variables

Configure codebrief behavior with environment variables:

```bash
# Set default output directory
export codebrief_OUTPUT_DIR=~/context-outputs

# Enable debug mode
export codebrief_DEBUG=1

# Set default config file location
export codebrief_CONFIG=~/.codebrief.toml
```

## Troubleshooting

### Common Issues

!!! warning "Python Version Issues"
    **Problem**: `codebrief: command not found` after installation

    **Solution**: Ensure you're in the Poetry virtual environment:
    ```bash
    poetry shell
    # or use
    poetry run codebrief --version
    ```

!!! warning "Permission Errors"
    **Problem**: Permission denied when installing Poetry or running commands

    **Solution**: Don't use `sudo` with Poetry. Install Poetry for your user only:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

!!! warning "Import Errors"
    **Problem**: `ModuleNotFoundError` when running codebrief

    **Solution**: Reinstall dependencies:
    ```bash
    poetry install --sync
    ```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](../help/troubleshooting.md)
2. Search [existing issues](https://github.com/YOUR_USERNAME/codebrief/issues)
3. Create a [new issue](https://github.com/YOUR_USERNAME/codebrief/issues/new) if needed

## Next Steps

Now that codebrief is installed:

- 📚 Read the [Quick Start Guide](quick-start.md)
- ⚙️ Set up [Configuration](configuration.md)
- 🎯 Follow the [Basic Usage Tutorial](../tutorials/basic-usage.md)
- 📖 Explore the [User Guide](../user-guide/cli-commands.md)

---

*Installation issues? We're here to help! Check our [Support page](../help/support.md) for assistance.*
