# Python Projects Examples

Comprehensive examples for using codebrief with Python projects, from simple scripts to complex applications.

## 🐍 Python Project Types

### Simple Python Script

For single-file or small Python projects:

```bash
# Basic context for a simple script
codebrief flatten . \
  --include "*.py" \
  --include "*.md" \
  --include "requirements.txt" \
  --output simple-script-context.md

# With Git context
codebrief bundle \
  --exclude-deps \
  --flatten . \
  --git-log-count 5 \
  --output script-with-git.md
```

### Python Package/Library

For structured Python packages:

```bash
# Complete library context
codebrief bundle \
  --output python-library-context.md \
  --flatten src/ tests/ README.md setup.py pyproject.toml

# Development-focused bundle
codebrief bundle \
  --git-log-count 15 \
  --git-full-diff \
  --flatten src/ tests/ \
  --output library-dev-context.md
```

### Web Application (Flask/Django)

For Python web applications:

```bash
# Flask application
codebrief bundle \
  --output flask-app-context.md \
  --flatten app/ templates/ static/ requirements.txt \
  --git-log-count 10

# Django project
codebrief bundle \
  --output django-project-context.md \
  --flatten myproject/ manage.py requirements.txt \
  --git-log-count 12
```

### Data Science Project

For data science and ML projects:

```bash
# Data science bundle
codebrief bundle \
  --output data-science-context.md \
  --flatten notebooks/ src/ data/ requirements.txt \
  --exclude-tree \
  --git-log-count 8

# ML model development
codebrief bundle \
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
codebrief git-info \
  --log-count 10 \
  --diff-options "--stat" \
  --output "daily-context/$DATE-git-activity.md"

# Code changes bundle
codebrief bundle \
  --exclude-tree \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/ \
  --output "daily-context/$DATE-code-changes.md"

# Dependency check
codebrief deps \
  --output "daily-context/$DATE-dependencies.md"

echo "Daily context saved to daily-context/"
```

### Testing and Quality Assurance

Context for testing workflows:

```bash
# Test-focused bundle
codebrief bundle \
  --exclude-deps \
  --flatten tests/ src/ pytest.ini tox.ini \
  --git-log-count 5 \
  --output testing-context.md

# Quality assurance bundle
codebrief bundle \
  --flatten src/ tests/ .pre-commit-config.yaml pyproject.toml \
  --git-log-count 8 \
  --output qa-context.md
```

### Code Review Preparation

Prepare comprehensive review materials:

```bash
# Pull request bundle
codebrief bundle \
  --output "reviews/pr-$(git branch --show-current).md" \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/

# Feature review bundle
FEATURE=$(git branch --show-current | cut -d'/' -f2)
codebrief bundle \
  --flatten "src/*$FEATURE*" "tests/*$FEATURE*" \
  --git-log-count 3 \
  --output "reviews/feature-$FEATURE-review.md"
```

## 📦 Package Management

### Poetry Projects

For Poetry-managed Python projects:

```bash
# Poetry project bundle
codebrief bundle \
  --output poetry-project-context.md \
  --flatten src/ tests/ pyproject.toml poetry.lock README.md

# Development environment context
codebrief bundle \
  --flatten src/ pyproject.toml \
  --git-log-count 10 \
  --output poetry-dev-context.md
```

### pip/setuptools Projects

For traditional pip-based projects:

```bash
# Traditional Python project
codebrief bundle \
  --output pip-project-context.md \
  --flatten src/ tests/ setup.py requirements.txt MANIFEST.in

# Multiple requirements files
codebrief bundle \
  --flatten src/ requirements/ setup.py \
  --git-log-count 8 \
  --output multi-req-context.md
```

### Conda Environment Projects

For Conda-managed projects:

```bash
# Conda project bundle
codebrief bundle \
  --output conda-project-context.md \
  --flatten src/ tests/ environment.yml setup.py

# Data science with Conda
codebrief bundle \
  --flatten notebooks/ src/ environment.yml \
  --exclude-tree \
  --output conda-datascience.md
```

## 🏗️ Framework-Specific Examples

### FastAPI Application

```bash
# FastAPI project context
codebrief bundle \
  --output fastapi-context.md \
  --flatten app/ tests/ requirements.txt Dockerfile \
  --git-log-count 10

# API development bundle
codebrief bundle \
  --flatten app/routers/ app/models/ app/schemas/ \
  --git-log-count 5 \
  --output api-development.md
```

### Django Application

```bash
# Django project bundle
codebrief bundle \
  --output django-context.md \
  --flatten myproject/ manage.py requirements.txt \
  --git-log-count 12

# Django app-specific context
codebrief bundle \
  --flatten myproject/myapp/ myproject/settings/ \
  --git-log-count 8 \
  --output django-app-context.md
```

### Flask Application

```bash
# Flask application bundle
codebrief bundle \
  --output flask-context.md \
  --flatten app/ templates/ static/ requirements.txt \
  --git-log-count 10

# Flask blueprint context
codebrief bundle \
  --flatten app/blueprints/ app/models/ \
  --git-log-count 6 \
  --output flask-blueprints.md
```

## 🧪 Testing Scenarios

### Unit Testing Context

```bash
# Unit testing bundle
codebrief bundle \
  --flatten src/ tests/unit/ pytest.ini \
  --git-log-count 5 \
  --output unit-testing-context.md

# Test coverage analysis
codebrief bundle \
  --flatten tests/ .coveragerc pytest.ini \
  --git-diff-options "--stat" \
  --output coverage-analysis.md
```

### Integration Testing

```bash
# Integration testing context
codebrief bundle \
  --flatten src/ tests/integration/ docker-compose.yml \
  --git-log-count 8 \
  --output integration-testing.md
```

### Performance Testing

```bash
# Performance testing bundle
codebrief bundle \
  --flatten src/ tests/performance/ requirements-dev.txt \
  --git-log-count 6 \
  --output performance-testing.md
```

## 🚀 Deployment and Production

### Docker Deployment

```bash
# Docker deployment context
codebrief bundle \
  --output docker-deployment.md \
  --flatten src/ Dockerfile docker-compose.yml requirements.txt \
  --git-log-count 10

# Multi-stage Docker build
codebrief bundle \
  --flatten Dockerfile* requirements* src/ \
  --git-log-count 5 \
  --output docker-multistage.md
```

### Cloud Deployment

```bash
# AWS deployment context
codebrief bundle \
  --flatten src/ aws/ requirements.txt serverless.yml \
  --git-log-count 8 \
  --output aws-deployment.md

# Heroku deployment
codebrief bundle \
  --flatten src/ Procfile runtime.txt requirements.txt \
  --git-log-count 6 \
  --output heroku-deployment.md
```

## 📊 Data Science Workflows

### Jupyter Notebook Projects

```bash
# Notebook project context
codebrief bundle \
  --output notebook-project.md \
  --flatten notebooks/ src/ data/ requirements.txt \
  --exclude-tree \
  --git-log-count 10

# Research notebook bundle
codebrief bundle \
  --flatten notebooks/research/ src/analysis/ \
  --git-log-count 5 \
  --output research-context.md
```

### Machine Learning Pipeline

```bash
# ML pipeline context
codebrief bundle \
  --output ml-pipeline.md \
  --flatten src/pipeline/ models/ training/ \
  --git-log-count 12

# Model training context
codebrief bundle \
  --flatten training/ models/ config/ \
  --git-log-count 8 \
  --output model-training.md
```

## 🔧 Configuration Examples

### Project-Specific Configuration

```toml
# pyproject.toml for Python projects
[tool.codebrief]
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
alias ccpy='codebrief bundle --flatten src/ tests/ --git-log-count 10'
alias cctest='codebrief bundle --flatten tests/ --exclude-deps --git-log-count 5'
alias ccdev='codebrief bundle --git-full-diff --flatten src/'

# Project type aliases
alias ccflask='codebrief bundle --flatten app/ templates/ requirements.txt'
alias ccdjango='codebrief bundle --flatten myproject/ manage.py requirements.txt'
alias ccfastapi='codebrief bundle --flatten app/ requirements.txt'

# Data science aliases
alias ccnotebook='codebrief bundle --flatten notebooks/ src/ --exclude-tree'
alias ccml='codebrief bundle --flatten models/ training/ src/'
```

## 🎯 Best Practices for Python Projects

### Code Organization

```bash
# Well-organized Python project structure
codebrief tree --output project-structure.txt

# Source code focus
codebrief bundle \
  --flatten src/ \
  --exclude-deps \
  --git-log-count 8 \
  --output source-code-context.md

# Test organization
codebrief bundle \
  --flatten tests/ \
  --exclude-deps \
  --git-log-count 5 \
  --output test-organization.md
```

### Documentation Generation

```bash
# Documentation bundle
codebrief bundle \
  --exclude-git \
  --flatten docs/ README.md CHANGELOG.md \
  --output documentation-bundle.md

# API documentation context
codebrief bundle \
  --flatten src/ docs/api/ \
  --exclude-deps \
  --output api-docs-context.md
```

### Performance Optimization

```bash
# Large Python project optimization
codebrief bundle \
  --exclude-tree \
  --git-log-count 5 \
  --flatten src/core/ \
  --output optimized-python-context.md

# Memory-efficient for huge codebases
codebrief bundle \
  --exclude-files \
  --git-log-count 10 \
  --output metadata-only-python.md
```

## 🚨 Troubleshooting Python Projects

### Common Issues

```bash
# Virtual environment conflicts
codebrief bundle \
  --exclude-deps \
  --flatten src/ requirements.txt \
  --output venv-safe-context.md

# Large dependency trees
codebrief bundle \
  --exclude-deps \
  --flatten src/ tests/ \
  --output no-deps-context.md

# Binary file handling
codebrief bundle \
  --flatten src/ \
  --git-diff-options "--name-only" \
  --output binary-safe-context.md
```

---

*These examples demonstrate how to effectively use codebrief across different Python project types and development workflows.*
