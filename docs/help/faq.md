# Frequently Asked Questions

Common questions and answers about ContextCraft usage, troubleshooting, and best practices.

## 🚀 Getting Started

### Q: What is ContextCraft and why should I use it?

**A:** ContextCraft is a CLI toolkit that generates structured, comprehensive context from your projects for use with Large Language Models (LLMs). It's perfect for:

- **LLM Integration**: Creating context that ChatGPT, Claude, and other AI tools can easily understand
- **Debugging**: Quickly sharing project structure and code with others
- **Documentation**: Generating project overviews and code summaries
- **Code Review**: Preparing comprehensive context for reviewers

### Q: How is ContextCraft different from other tools?

**A:** ContextCraft is specifically designed for LLM consumption with features like:

- **Smart File Separation**: Clear markers between files in flattened output
- **Intelligent Ignoring**: `.llmignore` support with `.gitignore`-style syntax
- **Multi-Language Support**: Dependency analysis across Python, Node.js, and more
- **Rich CLI Experience**: Beautiful terminal output with helpful error messages
- **Flexible Configuration**: Project-level config via `pyproject.toml`

### Q: What file types does ContextCraft support?

**A:** ContextCraft works with any text-based file. Default includes:

**Programming Languages:**
- Python (`.py`, `.pyi`)
- JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)
- Web files (`.html`, `.css`, `.scss`)
- Many others (see [CLI Commands](../user-guide/cli-commands.md))

**Configuration & Documentation:**
- Markdown (`.md`)
- TOML, JSON, YAML files
- Requirements files, package.json, etc.

You can customize included file types with `--include` patterns.

## 🛠️ Installation & Setup

### Q: I get "contextcraft: command not found" after installation

**A:** This usually means you're not in the Poetry virtual environment:

```bash
# Solution 1: Activate the environment
poetry shell
contextcraft --version

# Solution 2: Run via Poetry
poetry run contextcraft --version

# Solution 3: Check PATH
echo $PATH | grep poetry
```

### Q: Can I install ContextCraft via pip?

**A:** PyPI installation is coming soon! For now, install from source:

```bash
git clone https://github.com/Shorzinator/ContextCraft.git
cd ContextCraft
poetry install
poetry shell
```

### Q: Does ContextCraft work on Windows/macOS/Linux?

**A:** Yes! ContextCraft is built with Python and works on all major platforms:

- **Windows** (PowerShell, Command Prompt, WSL)
- **macOS** (Terminal, iTerm2)
- **Linux** (All major distributions)

## 📄 Using ContextCraft

### Q: How do I generate context for my entire project?

**A:** Use a combination of commands:

```bash
# Project structure
contextcraft tree --output structure.txt

# Source code (adjust patterns for your language)
contextcraft flatten . --include "*.py" --include "*.js" --output code.md

# Dependencies
contextcraft deps --output dependencies.md
```

### Q: The output is too large for my LLM. How can I reduce it?

**A:** Several strategies to reduce output size:

1. **Be selective with directories:**
   ```bash
   contextcraft flatten src/ --output source-only.md
   ```

2. **Use specific include patterns:**
   ```bash
   contextcraft flatten . --include "*.py" --exclude "tests/"
   ```

3. **Use .llmignore for project-wide exclusions:**
   ```gitignore
   # .llmignore
   tests/
   docs/
   __pycache__/
   *.log
   ```

4. **Focus on changed files:**
   ```bash
   # If using git
   git diff --name-only | xargs contextcraft flatten --output changes.md
   ```

### Q: How do I include/exclude specific files or directories?

**A:** ContextCraft provides multiple ways to control what's included:

1. **CLI options (highest precedence):**
   ```bash
   contextcraft flatten . --include "*.py" --exclude "tests/"
   ```

2. **`.llmignore` file (project-specific):**
   ```gitignore
   # .llmignore
   __pycache__/
   *.pyc
   .venv/
   !important.py  # Negation to include
   ```

3. **Configuration (`pyproject.toml`):**
   ```toml
   [tool.contextcraft]
   global_exclude_patterns = ["*.log", "tmp/"]
   global_include_patterns = ["*.py", "*.md"]
   ```

### Q: Can I use ContextCraft with non-Python projects?

**A:** Absolutely! ContextCraft works with any project. Examples:

**Node.js Project:**
```bash
contextcraft flatten . --include "*.js" --include "*.ts" --include "*.json"
```

**Java Project:**
```bash
contextcraft flatten . --include "*.java" --include "*.xml" --include "*.properties"
```

**Mixed Project:**
```bash
contextcraft flatten . --include "*.py" --include "*.js" --include "*.java"
```

## ⚙️ Configuration

### Q: How do I set default output filenames?

**A:** Configure in your `pyproject.toml`:

```toml
[tool.contextcraft]
default_output_filename_tree = "docs/project-structure.txt"
default_output_filename_flatten = "docs/codebase-summary.md"
default_output_filename_deps = "docs/dependencies.md"
```

Then run commands without `--output`:
```bash
contextcraft tree       # Creates docs/project-structure.txt
contextcraft flatten .  # Creates docs/codebase-summary.md
```

### Q: What's the difference between .llmignore and global_exclude_patterns?

**A:** They work together but serve different purposes:

- **`.llmignore`**: Project-specific ignore patterns (like `.gitignore`)
- **`global_exclude_patterns`**: Configuration-based patterns in `pyproject.toml`

**Precedence order:**
1. Core system exclusions (`.git`, etc.)
2. `.llmignore` patterns
3. Configuration `global_exclude_patterns`
4. CLI `--exclude` options

### Q: Can I have different configurations for different environments?

**A:** Yes! Use environment variables or different config files:

```bash
# Different configs
export CONTEXTCRAFT_CONFIG="pyproject.dev.toml"
contextcraft tree

# Environment-specific patterns
export CONTEXTCRAFT_EXCLUDE="*.log,tmp/"
contextcraft flatten .
```

## 🎯 Advanced Usage

### Q: How do I integrate ContextCraft with my CI/CD pipeline?

**A:** ContextCraft works great in automated environments:

```yaml
# GitHub Actions example
- name: Generate project context
  run: |
    poetry run contextcraft tree --output artifacts/structure.txt
    poetry run contextcraft deps --output artifacts/dependencies.md

- name: Upload context artifacts
  uses: actions/upload-artifact@v3
  with:
    name: project-context
    path: artifacts/
```

### Q: Can I pipe ContextCraft output to other tools?

**A:** Yes! ContextCraft works well in Unix pipelines:

```bash
# Search for TODOs in flattened code
contextcraft flatten . --include "*.py" | grep -n "TODO"

# Count lines of code
contextcraft flatten src/ --include "*.py" | wc -l

# Copy to clipboard (macOS)
contextcraft tree | pbcopy

# Send via email (with appropriate tools)
contextcraft flatten . --include "*.py" | mail -s "Code Review" reviewer@company.com
```

### Q: How do I generate context for just my recent changes?

**A:** Combine with Git commands:

```bash
# Files changed in last commit
git diff --name-only HEAD~1 | xargs contextcraft flatten --output recent-changes.md

# Modified files (not committed)
git ls-files -m | xargs contextcraft flatten --output working-changes.md

# Files in a specific branch
git diff --name-only main..feature-branch | xargs contextcraft flatten --output branch-changes.md
```

## 🐛 Troubleshooting

### Q: ContextCraft is including files I don't want

**A:** Check the ignore precedence and patterns:

1. **Verify your `.llmignore` syntax:**
   ```bash
   # Test with a simple pattern first
   echo "*.log" > .llmignore
   contextcraft tree
   ```

2. **Check pattern matching:**
   ```bash
   # Use absolute paths to debug
   contextcraft tree --ignore "absolute/path/to/unwanted/dir"
   ```

3. **Validate configuration:**
   ```bash
   # Check if config is being loaded
   contextcraft tree --help  # Shows warnings for invalid config
   ```

### Q: I'm getting "Permission denied" errors

**A:** Common solutions:

1. **Check output directory permissions:**
   ```bash
   mkdir -p output-dir
   chmod 755 output-dir
   contextcraft tree --output output-dir/tree.txt
   ```

2. **Don't use sudo with Poetry:**
   ```bash
   # ❌ Wrong
   sudo poetry run contextcraft tree

   # ✅ Correct
   poetry run contextcraft tree
   ```

3. **Use relative paths:**
   ```bash
   # ❌ Might fail
   contextcraft tree --output /etc/tree.txt

   # ✅ Better
   contextcraft tree --output ./docs/tree.txt
   ```

### Q: The output contains strange characters or is corrupted

**A:** This usually indicates binary files being processed:

```bash
# Check for binary files in output
contextcraft flatten . --include "*" | grep -a "binary"

# Exclude binary files explicitly
contextcraft flatten . \
  --include "*.py" --include "*.md" \
  --exclude "*.jpg" --exclude "*.png" --exclude "*.zip"
```

### Q: ContextCraft is very slow on my large project

**A:** Optimize for large projects:

1. **Be more selective:**
   ```bash
   # Focus on specific directories
   contextcraft flatten src/ app/ --output focused.md
   ```

2. **Use better ignore patterns:**
   ```gitignore
   # .llmignore - exclude large directories
   node_modules/
   .venv/
   build/
   dist/
   *.min.js
   ```

3. **Process in smaller chunks:**
   ```bash
   # Process modules separately
   contextcraft flatten src/module1/ --output module1.md
   contextcraft flatten src/module2/ --output module2.md
   ```

## 🔮 Future Features

### Q: Will ContextCraft support more programming languages?

**A:** Yes! We're actively working on expanding language support:

- **Planned**: Java (Maven/Gradle), Ruby (Gemfile), Go (go.mod), Rust (Cargo.toml)
- **Considering**: PHP (composer.json), C# (.csproj), Dart (pubspec.yaml)

### Q: Is a bundle command coming?

**A:** Yes! The bundle command will combine tree, flatten, deps, and git info into a single, well-structured Markdown output. It's high priority for v1.0.

### Q: Will there be a GUI or web interface?

**A:** We're exploring options for:
- VS Code extension
- Web-based interface
- Desktop application

The CLI will always remain our primary focus.

## 💡 Best Practices

### Q: What's the best workflow for sharing code with LLMs?

**A:** Our recommended workflow:

1. **Start with structure:**
   ```bash
   contextcraft tree --output structure.txt
   ```

2. **Add focused code:**
   ```bash
   contextcraft flatten src/ --include "*.py" --output code.md
   ```

3. **Include context:**
   ```bash
   contextcraft deps --output deps.md
   ```

4. **Create a summary:**
   ```markdown
   # Project Context

   ## Structure
   [paste structure.txt contents]

   ## Dependencies
   [paste deps.md contents]

   ## Code
   [paste relevant sections from code.md]
   ```

### Q: How often should I regenerate context?

**A:** Depends on your workflow:

- **During active development**: After significant changes
- **For code reviews**: Once per review cycle
- **For documentation**: Weekly or before releases
- **Automated**: Set up git hooks or CI for automatic generation

### Q: Should I commit generated context files?

**A:** It depends:

**Commit if:**
- Part of documentation strategy
- Used in CI/CD pipelines
- Shared with team regularly

**Don't commit if:**
- Generated frequently and changes often
- Contains sensitive information
- Used only for personal LLM interactions

Use `.gitignore` patterns for temporary context files:
```gitignore
# Generated context files
*-context.md
project-structure.txt
temp-*.md
```

## 🆘 Getting Help

### Q: Where can I get more help?

**A:** Several resources available:

1. **Documentation**: [User Guide](../user-guide/cli-commands.md), [Tutorials](../tutorials/basic-usage.md)
2. **GitHub Issues**: [Report bugs or request features](https://github.com/Shorzinator/ContextCraft/issues)
3. **Troubleshooting**: [Detailed troubleshooting guide](troubleshooting.md)
4. **Examples**: [Real-world examples](../examples/python-projects.md)

### Q: How can I contribute to ContextCraft?

**A:** We welcome contributions! See our [Contributing Guide](../development/contributing.md) for:

- Setting up development environment
- Code style guidelines
- Testing requirements
- Pull request process

---

*Don't see your question? [Open an issue](https://github.com/Shorzinator/ContextCraft/issues) or check our [Support page](support.md).*
