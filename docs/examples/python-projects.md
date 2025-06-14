# Python Projects Examples

Comprehensive examples for using ContextCraft with Python projects, from simple scripts to complex applications.

## 🐍 Python Project Types

### Simple Python Script

For single-file or small Python projects:

```bash
# Basic context for a simple script
contextcraft flatten . \
  --include "*.py" \
  --include "*.md" \
  --include "requirements.txt" \
  --output simple-script-context.md

# With Git context
contextcraft bundle \
  --exclude-deps \
  --flatten . \
  --git-log-count 5 \
  --output script-with-git.md
```

### Python Package/Library

For structured Python packages:

```bash
# Complete library context
contextcraft bundle \
  --output python-library-context.md \
  --flatten src/ tests/ README.md setup.py pyproject.toml

# Development-focused bundle
contextcraft bundle \
  --git-log-count 15 \
  --git-full-diff \
  --flatten src/ tests/ \
  --output library-dev-context.md
```

### Web Application (Flask/Django)

For Python web applications:

```bash
# Flask application
contextcraft bundle \
  --output flask-app-context.md \
  --flatten app/ templates/ static/ requirements.txt \
  --git-log-count 10

# Django project
contextcraft bundle \
  --output django-project-context.md \
  --flatten myproject/ manage.py requirements.txt \
  --git-log-count 12
```

### Data Science Project

For data science and ML projects:

```bash
# Data science bundle
contextcraft bundle \
  --output data-science-context.md \
  --flatten notebooks/ src/ data/ requirements.txt \
  --exclude-tree \
  --git-log-count 8

# ML model development
contextcraft bundle \
  --flatten models/ training/ evaluation/ \
  --git-log-count 10 \
  --output ml-development.md
```

## 🔧 Development Workflows

### Local Development

Daily development context generation:

```bash
#!/bin/bash
# daily-python-context.sh

DATE=$(date +%Y-%m-%d)
PROJECT_NAME=$(basename $(pwd))

echo "Generating daily context for $PROJECT_NAME..."

# Git activity summary
contextcraft git-info \
  --log-count 10 \
  --diff-options "--stat" \
  --output "daily-context/$DATE-git-activity.md"

# Code changes bundle
contextcraft bundle \
  --exclude-tree \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/ \
  --output "daily-context/$DATE-code-changes.md"

# Dependency check
contextcraft deps \
  --output "daily-context/$DATE-dependencies.md"

echo "Daily context saved to daily-context/"
```

### Testing and Quality Assurance

Context for testing workflows:

```bash
# Test-focused bundle
contextcraft bundle \
  --exclude-deps \
  --flatten tests/ src/ pytest.ini tox.ini \
  --git-log-count 5 \
  --output testing-context.md

# Quality assurance bundle
contextcraft bundle \
  --flatten src/ tests/ .pre-commit-config.yaml pyproject.toml \
  --git-log-count 8 \
  --output qa-context.md
```

### Code Review Preparation

Prepare comprehensive review materials:

```bash
# Pull request bundle
contextcraft bundle \
  --output "reviews/pr-$(git branch --show-current).md" \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/

# Feature review bundle
FEATURE=$(git branch --show-current | cut -d'/' -f2)
contextcraft bundle \
  --flatten "src/*$FEATURE*" "tests/*$FEATURE*" \
  --git-log-count 3 \
  --output "reviews/feature-$FEATURE-review.md"
```

## 📦 Package Management

### Poetry Projects

For Poetry-managed Python projects:

```bash
# Poetry project bundle
contextcraft bundle \
  --output poetry-project-context.md \
  --flatten src/ tests/ pyproject.toml poetry.lock README.md

# Development environment context
contextcraft bundle \
  --flatten src/ pyproject.toml \
  --git-log-count 10 \
  --output poetry-dev-context.md
```

### pip/setuptools Projects

For traditional pip-based projects:

```bash
# Traditional Python project
contextcraft bundle \
  --output pip-project-context.md \
  --flatten src/ tests/ setup.py requirements.txt MANIFEST.in

# Multiple requirements files
contextcraft bundle \
  --flatten src/ requirements/ setup.py \
  --git-log-count 8 \
  --output multi-req-context.md
```

### Conda Environment Projects

For Conda-managed projects:

```bash
# Conda project bundle
contextcraft bundle \
  --output conda-project-context.md \
  --flatten src/ tests/ environment.yml setup.py

# Data science with Conda
contextcraft bundle \
  --flatten notebooks/ src/ environment.yml \
  --exclude-tree \
  --output conda-datascience.md
```

## 🏗️ Framework-Specific Examples

### FastAPI Application

```bash
# FastAPI project context
contextcraft bundle \
  --output fastapi-context.md \
  --flatten app/ tests/ requirements.txt Dockerfile \
  --git-log-count 10

# API development bundle
contextcraft bundle \
  --flatten app/routers/ app/models/ app/schemas/ \
  --git-log-count 5 \
  --output api-development.md
```

### Django Application

```bash
# Django project bundle
contextcraft bundle \
  --output django-context.md \
  --flatten myproject/ manage.py requirements.txt \
  --git-log-count 12

# Django app-specific context
contextcraft bundle \
  --flatten myproject/myapp/ myproject/settings/ \
  --git-log-count 8 \
  --output django-app-context.md
```

### Flask Application

```bash
# Flask application bundle
contextcraft bundle \
  --output flask-context.md \
  --flatten app/ templates/ static/ requirements.txt \
  --git-log-count 10

# Flask blueprint context
contextcraft bundle \
  --flatten app/blueprints/ app/models/ \
  --git-log-count 6 \
  --output flask-blueprints.md
```

## 🧪 Testing Scenarios

### Unit Testing Context

```bash
# Unit testing bundle
contextcraft bundle \
  --flatten src/ tests/unit/ pytest.ini \
  --git-log-count 5 \
  --output unit-testing-context.md

# Test coverage analysis
contextcraft bundle \
  --flatten tests/ .coveragerc pytest.ini \
  --git-diff-options "--stat" \
  --output coverage-analysis.md
```

### Integration Testing

```bash
# Integration testing context
contextcraft bundle \
  --flatten src/ tests/integration/ docker-compose.yml \
  --git-log-count 8 \
  --output integration-testing.md
```

### Performance Testing

```bash
# Performance testing bundle
contextcraft bundle \
  --flatten src/ tests/performance/ requirements-dev.txt \
  --git-log-count 6 \
  --output performance-testing.md
```

## 🚀 Deployment and Production

### Docker Deployment

```bash
# Docker deployment context
contextcraft bundle \
  --output docker-deployment.md \
  --flatten src/ Dockerfile docker-compose.yml requirements.txt \
  --git-log-count 10

# Multi-stage Docker build
contextcraft bundle \
  --flatten Dockerfile* requirements* src/ \
  --git-log-count 5 \
  --output docker-multistage.md
```

### Cloud Deployment

```bash
# AWS deployment context
contextcraft bundle \
  --flatten src/ aws/ requirements.txt serverless.yml \
  --git-log-count 8 \
  --output aws-deployment.md

# Heroku deployment
contextcraft bundle \
  --flatten src/ Procfile runtime.txt requirements.txt \
  --git-log-count 6 \
  --output heroku-deployment.md
```

## 📊 Data Science Workflows

### Jupyter Notebook Projects

```bash
# Notebook project context
contextcraft bundle \
  --output notebook-project.md \
  --flatten notebooks/ src/ data/ requirements.txt \
  --exclude-tree \
  --git-log-count 10

# Research notebook bundle
contextcraft bundle \
  --flatten notebooks/research/ src/analysis/ \
  --git-log-count 5 \
  --output research-context.md
```

### Machine Learning Pipeline

```bash
# ML pipeline context
contextcraft bundle \
  --output ml-pipeline.md \
  --flatten src/pipeline/ models/ training/ \
  --git-log-count 12

# Model training context
contextcraft bundle \
  --flatten training/ models/ config/ \
  --git-log-count 8 \
  --output model-training.md
```

## 🔧 Configuration Examples

### Project-Specific Configuration

```toml
# pyproject.toml for Python projects
[tool.contextcraft]
default_output_filename_bundle = "context/python-project-bundle.md"
default_output_filename_git_info = "context/git-info.md"

# Python-specific excludes
global_exclude_patterns = [
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    ".pytest_cache/",
    ".coverage",
    "htmlcov/",
    ".tox/",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*.cover",
    ".hypothesis/",
    ".venv/",
    "venv/",
    "ENV/",
    "env/",
    ".env"
]

# Python-specific includes
global_include_patterns = [
    "*.py",
    "*.pyx",
    "*.pxd",
    "*.pxi",
    "*.md",
    "*.rst",
    "*.txt",
    "*.toml",
    "*.cfg",
    "*.ini",
    "*.yml",
    "*.yaml",
    "*.json"
]
```

### Environment-Specific Aliases

```bash
# ~/.bashrc or ~/.zshrc

# Python development aliases
alias ccpy='contextcraft bundle --flatten src/ tests/ --git-log-count 10'
alias cctest='contextcraft bundle --flatten tests/ --exclude-deps --git-log-count 5'
alias ccdev='contextcraft bundle --git-full-diff --flatten src/'

# Project type aliases
alias ccflask='contextcraft bundle --flatten app/ templates/ requirements.txt'
alias ccdjango='contextcraft bundle --flatten myproject/ manage.py requirements.txt'
alias ccfastapi='contextcraft bundle --flatten app/ requirements.txt'

# Data science aliases
alias ccnotebook='contextcraft bundle --flatten notebooks/ src/ --exclude-tree'
alias ccml='contextcraft bundle --flatten models/ training/ src/'
```

## 🎯 Best Practices for Python Projects

### Code Organization

```bash
# Well-organized Python project structure
contextcraft tree --output project-structure.txt

# Source code focus
contextcraft bundle \
  --flatten src/ \
  --exclude-deps \
  --git-log-count 8 \
  --output source-code-context.md

# Test organization
contextcraft bundle \
  --flatten tests/ \
  --exclude-deps \
  --git-log-count 5 \
  --output test-organization.md
```

### Documentation Generation

```bash
# Documentation bundle
contextcraft bundle \
  --exclude-git \
  --flatten docs/ README.md CHANGELOG.md \
  --output documentation-bundle.md

# API documentation context
contextcraft bundle \
  --flatten src/ docs/api/ \
  --exclude-deps \
  --output api-docs-context.md
```

### Performance Optimization

```bash
# Large Python project optimization
contextcraft bundle \
  --exclude-tree \
  --git-log-count 5 \
  --flatten src/core/ \
  --output optimized-python-context.md

# Memory-efficient for huge codebases
contextcraft bundle \
  --exclude-files \
  --git-log-count 10 \
  --output metadata-only-python.md
```

## 🚨 Troubleshooting Python Projects

### Common Issues

```bash
# Virtual environment conflicts
contextcraft bundle \
  --exclude-deps \
  --flatten src/ requirements.txt \
  --output venv-safe-context.md

# Large dependency trees
contextcraft bundle \
  --exclude-deps \
  --flatten src/ tests/ \
  --output no-deps-context.md

# Binary file handling
contextcraft bundle \
  --flatten src/ \
  --git-diff-options "--name-only" \
  --output binary-safe-context.md
```

---

*These examples demonstrate how to effectively use ContextCraft across different Python project types and development workflows.*
