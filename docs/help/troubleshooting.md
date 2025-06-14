# Troubleshooting

Common issues and solutions for ContextCraft users.

## Installation Issues

### Poetry Installation Problems

**Problem**: `poetry install` fails or takes too long

**Solutions**:
```bash
# Clear poetry cache
poetry cache clear pypi --all

# Install with verbose output
poetry install -vvv

# Use pip install as fallback
pip install -e .
```

### Python Version Compatibility

**Problem**: Unsupported Python version errors

**Solutions**:
```bash
# Check your Python version
python --version

# Install compatible Python version (3.9+)
# macOS with Homebrew
brew install python@3.11

# Ubuntu/Debian
sudo apt install python3.11

# Use pyenv for version management
pyenv install 3.11.0
pyenv local 3.11.0
```

### Permission Errors

**Problem**: Permission denied during installation

**Solutions**:
```bash
# Use virtual environment
python -m venv contextcraft-env
source contextcraft-env/bin/activate  # Linux/macOS
# contextcraft-env\Scripts\activate  # Windows

# Install in user directory
pip install --user -e .
```

## Runtime Issues

### Command Not Found

**Problem**: `contextcraft: command not found`

**Solutions**:
```bash
# Activate poetry shell
poetry shell

# Use poetry run prefix
poetry run contextcraft --help

# Check installation
which contextcraft
poetry show contextcraft
```

### Git Repository Not Found

**Problem**: "Not a git repository" errors

**Solutions**:
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Run from project root
cd /path/to/your/project
contextcraft tree

# Specify project path
contextcraft tree /path/to/project
```

### File Permission Issues

**Problem**: Permission denied when reading/writing files

**Solutions**:
```bash
# Check file permissions
ls -la

# Fix permissions
chmod 755 /path/to/directory
chmod 644 /path/to/file

# Run with appropriate user
sudo chown -R $USER:$USER /path/to/project
```

## Output Issues

### Empty or Missing Output

**Problem**: Commands complete but produce no output

**Check List**:
1. **File Patterns**: Verify include/exclude patterns
2. **Directory Path**: Ensure correct project path
3. **File Extensions**: Check if files match patterns
4. **Permissions**: Verify read access to files

**Debug Steps**:
```bash
# Test with verbose output
contextcraft tree --help

# Check file detection
ls -la src/  # Verify files exist

# Test basic command
contextcraft tree .
```

### Encoding Issues

**Problem**: Unicode/encoding errors in output

**Solutions**:
```bash
# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Force UTF-8 output
contextcraft tree --output output.md
file output.md  # Check file encoding
```

### Large Output Files

**Problem**: Output files are too large or cause performance issues

**Solutions**:
```bash
# Use focused context
contextcraft flatten src/ --include "*.py" --exclude "*test*"

# Exclude large directories
contextcraft tree --ignore "node_modules/" "venv/" "__pycache__/"

# Split into smaller files
contextcraft flatten src/core/ --output core.md
contextcraft flatten src/utils/ --output utils.md
```

## Configuration Issues

### Configuration Not Loading

**Problem**: Settings in `pyproject.toml` not applied

**Solutions**:
```bash
# Verify file location
ls -la pyproject.toml

# Check TOML syntax
poetry check

# Test with explicit config
contextcraft tree --output custom-output.txt
```

### Invalid Configuration Format

**Problem**: Configuration validation errors

**Solutions**:
```toml
# Correct configuration format
[tool.contextcraft]
default_output_filename_tree = "project-tree.txt"
global_exclude_patterns = [
    "*.log",
    "*.tmp",
    "__pycache__/"
]
```

## Git Integration Issues

### Git Command Failures

**Problem**: Git-related commands fail

**Solutions**:
```bash
# Check git installation
git --version

# Verify repository status
git status

# Check git configuration
git config --list

# Test git log access
git log --oneline -n 5
```

### Missing Git History

**Problem**: Git info shows no commits or limited history

**Solutions**:
```bash
# Check git log
git log --oneline

# Verify repository depth (for clones)
git log --oneline | wc -l

# For shallow clones
git fetch --unshallow
```

### Git Diff Issues

**Problem**: Git diff output is empty or incorrect

**Solutions**:
```bash
# Check for staged changes
git status

# Verify diff options
git diff --stat

# Use specific git options
contextcraft git-info --diff-options "--name-only"
```

## Performance Issues

### Slow Execution

**Problem**: Commands take too long to complete

**Optimization Strategies**:
```bash
# Use focused patterns
contextcraft flatten src/ --include "*.py"

# Exclude large directories
contextcraft tree --ignore "node_modules/" "build/" "dist/"

# Process in parallel (custom script)
# See Advanced Workflows documentation
```

### Memory Issues

**Problem**: Out of memory errors with large projects

**Solutions**:
```bash
# Process smaller sections
contextcraft flatten src/module1/ --output module1.md
contextcraft flatten src/module2/ --output module2.md

# Use exclude patterns
contextcraft tree --ignore "*.log" "*.tmp" "__pycache__/"

# Limit git history
contextcraft git-info --log-count 5
```

## Dependency Analysis Issues

### No Dependencies Found

**Problem**: `contextcraft deps` shows no dependencies

**Check List**:
1. **File Names**: Verify dependency files exist
2. **File Formats**: Check supported formats (pyproject.toml, package.json)
3. **File Content**: Ensure files have valid syntax
4. **Directory**: Run from project root

**Debug Steps**:
```bash
# List dependency files
ls -la pyproject.toml package.json requirements*.txt

# Verify file content
head pyproject.toml
python -c "import toml; print(toml.load('pyproject.toml'))"
```

### Parsing Errors

**Problem**: Dependency file parsing fails

**Solutions**:
```bash
# Validate TOML files
poetry check  # For pyproject.toml

# Validate JSON files
python -m json.tool package.json  # For package.json

# Check file encoding
file pyproject.toml
```

## CI/CD Integration Issues

### GitHub Actions Failures

**Problem**: ContextCraft fails in CI/CD pipelines

**Common Solutions**:
```yaml
# Ensure full git history
- uses: actions/checkout@v4
  with:
    fetch-depth: 0

# Install dependencies properly
- name: Install Poetry
  uses: snok/install-poetry@v1

- name: Install Dependencies
  run: poetry install

# Set proper permissions
- name: Fix Permissions
  run: chmod -R 755 .
```

### Test Environment Differences

**Problem**: Works locally but fails in CI

**Debug Steps**:
1. **Environment Variables**: Check `env` output
2. **File Permissions**: Verify file access
3. **Dependencies**: Ensure same versions
4. **Git Configuration**: Check git setup

```yaml
- name: Debug Environment
  run: |
    pwd
    ls -la
    python --version
    poetry --version
    git status
```

## Common Error Messages

### "No such file or directory"

**Cause**: File path is incorrect or file doesn't exist

**Solution**:
```bash
# Check current directory
pwd

# List files
ls -la

# Use absolute paths
contextcraft tree /full/path/to/project
```

### "Permission denied"

**Cause**: Insufficient file/directory permissions

**Solution**:
```bash
# Fix permissions
chmod 755 directory/
chmod 644 file.txt

# Check ownership
ls -la
sudo chown $USER:$USER file.txt
```

### "Not a git repository"

**Cause**: Running git commands outside git repository

**Solution**:
```bash
# Initialize git
git init

# Or run from correct directory
cd /path/to/git/repo
contextcraft git-info
```

### "Command not found"

**Cause**: ContextCraft not in PATH or not installed

**Solution**:
```bash
# Activate poetry environment
poetry shell

# Or use poetry run
poetry run contextcraft --help

# Check installation
which contextcraft
```

## Getting Help

### Debug Information

When reporting issues, include:

```bash
# System information
uname -a                    # System details
python --version           # Python version
poetry --version           # Poetry version
git --version             # Git version

# ContextCraft information
poetry run contextcraft --version
poetry show contextcraft

# Environment details
pwd                        # Current directory
ls -la                    # Directory contents
git status                # Git status (if applicable)
```

### Community Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/Shorzinator/ContextCraft/issues)
- **GitHub Discussions**: [Community help and questions](https://github.com/Shorzinator/ContextCraft/discussions)
- **Documentation**: [Complete documentation](../index.md)

### Professional Support

For enterprise users requiring dedicated support:
- Contact through [GitHub Issues](https://github.com/Shorzinator/ContextCraft/issues) with `[Enterprise]` tag
- See [Security Policy](https://github.com/Shorzinator/ContextCraft/security) for security-related issues

## Prevention Tips

### Best Practices

1. **Use Virtual Environments**: Always use poetry or venv
2. **Regular Updates**: Keep dependencies updated
3. **Test Locally**: Test commands before CI/CD
4. **Configuration Management**: Use consistent configurations
5. **Documentation**: Keep team documentation updated

### Regular Maintenance

```bash
# Update dependencies
poetry update

# Clean cache
poetry cache clear pypi --all

# Verify installation
poetry run contextcraft --help

# Test basic functionality
poetry run contextcraft tree
```
