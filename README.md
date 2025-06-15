# <center>ContextCraft</center>

<div align="center">

[![CI](https://github.com/Shorzinator/ContextCraft/workflows/ContextCraft%20CI/badge.svg)](https://github.com/Shorzinator/ContextCraft/actions)
[![Coverage](https://img.shields.io/badge/coverage-77%25-yellow)](https://github.com/Shorzinator/ContextCraft)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>


**<center>A powerful CLI toolkit to generate comprehensive project context for Large Language Models (LLMs).</center>**


ContextCraft transforms your codebase into well-structured, LLM-friendly documentation by intelligently aggregating directory trees, code files, dependencies, and Git context into clean, consumable formats. It's like a translator between your repo and the digital mind you just hired to read it.

Transform your entire codebase into AI-ready context with one command.
No more copy-paste nightmares. No more explaining your project structure.
Just instant, comprehensive context that LLMs actually understand.

## ✨ Features

### 🌳 **Smart Directory Trees**
- Beautiful, hierarchical project structure visualization
- Rich console output with emojis and colors
- Intelligent filtering with `.llmignore` support
- Clean file output for documentation

### 📄 **Code Flattening**
- Concatenate multiple files into organized documents
- Clear file markers and intelligent content handling
- Support for include/exclude patterns
- Binary file detection and graceful handling

### 📦 **Dependency Analysis**
- Multi-language dependency extraction (Python, Node.js)
- Support for Poetry, pip, npm, and yarn
- Clean Markdown output with language grouping
- Extensible architecture for additional languages

### 🔄 **Git Context**
- Current branch and status information
- Recent commit history with configurable depth
- Diff analysis for understanding changes
- Graceful handling of non-Git repositories

### 📋 **Context Bundling**
- Aggregate multiple tools into comprehensive bundles
- Configurable section inclusion/exclusion
- Well-structured Markdown with navigation
- Perfect for LLM consumption

### 📋 **Clipboard Integration**
- Copy output directly to clipboard with `--to-clipboard` or `-c`
- Available for all commands (tree, flatten, deps, git-info, bundle)
- Smart behavior: only works when no output file specified
- Cross-platform support with graceful error handling

### 🎯 **Intelligent Filtering**
- `.llmignore` files with `.gitignore`-style syntax
- Configurable global patterns via `pyproject.toml`
- Smart precedence hierarchy
- Tool-specific fallback exclusions

---

## 💬 What Developers Are Saying

<div id="testimonials-container">
  <div class="testimonial-bubble" data-delay="0">
    <div class="testimonial-content">
      <div class="testimonial-quote">"⭐⭐⭐⭐⭐ Saves me 30 minutes every day. This tool is incredible for working with AI assistants!"</div>
      <div class="testimonial-author">- @alexdev</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="200">
    <div class="testimonial-content">
      <div class="testimonial-quote">"Game changer! Fixed a complex bug in 60 seconds by feeding the bundle to ChatGPT."</div>
      <div class="testimonial-author">- @sarahcodes</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="400">
    <div class="testimonial-content">
      <div class="testimonial-quote">"Our team onboarding went from hours to minutes. ContextCraft + AI = magic."</div>
      <div class="testimonial-author">- @miketheteam</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="600">
    <div class="testimonial-content">
      <div class="testimonial-quote">"No more 'it doesn't work' issues without context. Our OSS project loves this!"</div>
      <div class="testimonial-author">- @opensource_emma</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="800">
    <div class="testimonial-content">
      <div class="testimonial-quote">"The clipboard integration is genius. Copy → paste → profit!"</div>
      <div class="testimonial-author">- @devtools_lover</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="1000">
    <div class="testimonial-content">
      <div class="testimonial-quote">"Finally, a tool that speaks LLM. My AI pair programming just got 10x better."</div>
      <div class="testimonial-author">- @aidev2024</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="1200">
    <div class="testimonial-content">
      <div class="testimonial-quote">"Bundle command is pure gold. One command, complete context, happy AI."</div>
      <div class="testimonial-author">- @productivityhacker</div>
    </div>
  </div>

  <div class="testimonial-bubble" data-delay="1400">
    <div class="testimonial-content">
      <div class="testimonial-quote">"Elegant, simple, effective. This is how developer tools should be built."</div>
      <div class="testimonial-author">- @cleancode_advocate</div>
    </div>
  </div>
</div>

<style>
#testimonials-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: flex-start;
  margin: 2rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.testimonial-bubble {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  margin: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  max-width: 320px;
  min-width: 250px;
  position: relative;
  cursor: pointer;
  opacity: 0;
  transform: translateY(20px) scale(0.95);
  animation: bubbleFloat 0.6s ease-out forwards;
  border: 2px solid transparent;
}

.testimonial-bubble:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  z-index: 10;
  border-color: #3b82f6;
}

.testimonial-bubble::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(45deg, #3b82f6, #06b6d4, #10b981, #f59e0b);
  border-radius: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.testimonial-bubble:hover::before {
  opacity: 0.3;
}

.testimonial-content {
  position: relative;
  z-index: 2;
}

.testimonial-quote {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 1rem;
  font-style: italic;
  position: relative;
}

.testimonial-quote::before {
  content: '"';
  font-size: 2rem;
  color: #3b82f6;
  position: absolute;
  top: -0.5rem;
  left: -0.5rem;
  font-family: Georgia, serif;
}

.testimonial-author {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.9rem;
  text-align: right;
}

@keyframes bubbleFloat {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.9);
  }
  50% {
    opacity: 0.8;
    transform: translateY(-5px) scale(0.98);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes gentleFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

.testimonial-bubble:nth-child(odd) {
  animation-delay: 0.1s;
}

.testimonial-bubble:nth-child(even) {
  animation-delay: 0.3s;
}

.testimonial-bubble:nth-child(3n) {
  animation-delay: 0.5s;
}

.testimonial-bubble:hover {
  animation: gentleFloat 2s ease-in-out infinite;
}

@media (max-width: 768px) {
  #testimonials-container {
    padding: 1rem;
  }

  .testimonial-bubble {
    min-width: 100%;
    max-width: 100%;
    margin: 0.5rem 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .testimonial-bubble {
    animation: none;
    opacity: 1;
    transform: none;
  }

  .testimonial-bubble:hover {
    animation: none;
    transform: translateY(-4px) scale(1.01);
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const bubbles = document.querySelectorAll('.testimonial-bubble');

  // Stagger the animation of bubbles
  bubbles.forEach((bubble, index) => {
    const delay = parseInt(bubble.dataset.delay) || index * 200;
    setTimeout(() => {
      bubble.style.animationDelay = '0s';
      bubble.classList.add('animate');
    }, delay);
  });

  // Add subtle random movement
  bubbles.forEach(bubble => {
    const randomDelay = Math.random() * 2000;
    setTimeout(() => {
      bubble.style.animationDelay = `${Math.random() * 2}s`;
    }, randomDelay);
  });

  // Add click effect
  bubbles.forEach(bubble => {
    bubble.addEventListener('click', function() {
      this.style.transform = 'scale(0.98)';
      setTimeout(() => {
        this.style.transform = '';
      }, 150);
    });
  });
});
</script>

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install contextcraft

# Or install from source
git clone https://github.com/Shorzinator/ContextCraft.git
cd ContextCraft
poetry install
```

### Basic Usage

```bash
# Generate a directory tree
contextcraft tree

# Save tree to file
contextcraft tree -o project_structure.txt

# Copy tree to clipboard
contextcraft tree --to-clipboard

# Flatten code files
contextcraft flatten src/ -o flattened_code.md

# Copy flattened code to clipboard
contextcraft flatten src/ -c

# Analyze dependencies
contextcraft deps

# Get Git context
contextcraft git-info

# Create a comprehensive bundle
contextcraft bundle -o project_context.md

# Copy bundle to clipboard
contextcraft bundle --to-clipboard
```

### Configuration

Create a `.llmignore` file to exclude files and directories:

```gitignore
# .llmignore
*.log
__pycache__/
node_modules/
.env
build/
dist/
```

Configure defaults in `pyproject.toml`:

```toml
[tool.contextcraft]
default_output_filename_tree = "project_tree.txt"
default_output_filename_flatten = "flattened_code.md"
default_output_filename_deps = "dependencies.md"
default_output_filename_git_info = "git_context.md"
default_output_filename_bundle = "project_bundle.md"

global_exclude_patterns = [
    "*.tmp",
    "temp/",
    ".cache/"
]
```

## 📖 Documentation

**🌐 [Live Documentation Website](https://shorzinator.github.io/ContextCraft/)**

Comprehensive documentation including:

- **[Getting Started](https://shorzinator.github.io/ContextCraft/getting-started/installation/)** - Installation and basic usage
- **[CLI Commands](https://shorzinator.github.io/ContextCraft/user-guide/cli-commands/)** - Complete command reference
- **[Configuration](https://shorzinator.github.io/ContextCraft/getting-started/configuration/)** - Advanced configuration options
- **[API Reference](https://shorzinator.github.io/ContextCraft/reference/)** - Detailed API documentation
- **[Examples](https://shorzinator.github.io/ContextCraft/examples/)** - Real-world usage examples
- **[Tutorials](https://shorzinator.github.io/ContextCraft/tutorials/)** - Step-by-step guides

## 🛠️ Development

### Prerequisites

- Python 3.9+
- Poetry
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Shorzinator/ContextCraft.git
cd ContextCraft

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/contextcraft --cov-report=html
```

### Code Quality

We maintain high code quality standards. Some say it's obsessive. We say it's... necessary:

- **Linting**: Ruff for fast Python linting (not a dog, but still keeps your repo clean)
- **Formatting**: Ruff formatter for consistent code style
- **Security**: Bandit for security vulnerability scanning
- **Testing**: Pytest with 77%+ coverage (because 100% would be... suspicious)
- **Commits**: Conventional Commits for clear history and less git shame

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Reporting bugs and requesting features
- Development setup and workflow
- Code standards and testing
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (TL;DR: Use it, don’t sue us.)

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI framework
- Styled with [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- Powered by [Poetry](https://python-poetry.org/) for dependency management
- Quality assured with [Ruff](https://github.com/astral-sh/ruff) and [Pytest](https://pytest.org/)

## 📊 Project Status

ContextCraft is actively developed and maintained. Current status:

- ✅ **Core Tools**: All primary tools implemented and tested
- ✅ **CLI Interface**: Complete command-line interface
- ✅ **Documentation**: Comprehensive docs with examples
- ✅ **Testing**: 175+ tests with 77% coverage
- ✅ **CI/CD**: Automated testing and quality checks
- 🚀 **V1.0**: Feature-complete and production-ready

---

<div align="center">

**[📖 Documentation](https://shorzinator.github.io/ContextCraft/) • [🐛 Issues](https://github.com/Shorzinator/ContextCraft/issues) • [💬 Discussions](https://shorzinator.github.io/ContextCraft/community/)**

Made with ❤️ for the developer community

</div>
