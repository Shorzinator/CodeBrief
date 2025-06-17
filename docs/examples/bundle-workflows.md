# Bundle Workflow Examples

Discover powerful ways to use codebrief's bundle command for comprehensive project context generation across different scenarios and workflows.

## 🎯 Bundle Fundamentals

### Complete Project Bundle

Generate a comprehensive overview of your entire project:

```bash
# Full project context
codebrief bundle --output complete-project.md

# Customized complete bundle
codebrief bundle \
  --output project-overview-$(date +%Y%m%d).md \
  --git-log-count 15
```

**Output Structure:**
```markdown
# codebrief Bundle

## Table of Contents
- [Directory Tree](#directory-tree)
- [Git Context](#git-context)
- [Dependencies](#dependencies)
- [Files: /path/to/project](#files-pathtoproject)

## Directory Tree
[Visual project structure]

## Git Context
[Branch, commits, status]

## Dependencies
[Python, Node.js dependencies]

## Files: /path/to/project
[Flattened file contents]
```

### Selective Bundles

Create focused bundles for specific purposes:

```bash
# Code-only bundle (no dependencies)
codebrief bundle \
  --exclude-deps \
  --exclude-tree \
  --output code-only.md

# Documentation bundle (no Git info)
codebrief bundle \
  --exclude-git \
  --flatten docs/ README.md CHANGELOG.md \
  --output documentation.md

# Git-focused bundle (no file contents)
codebrief bundle \
  --exclude-files \
  --git-log-count 25 \
  --git-full-diff \
  --output git-analysis.md
```

## 🔍 Development Scenarios

### Feature Development

Track feature development progress:

```bash
# Feature branch bundle
FEATURE_BRANCH=$(git branch --show-current)
codebrief bundle \
  --output "features/${FEATURE_BRANCH}-context.md" \
  --git-log-count 10 \
  --flatten "src/features/" "tests/features/"

# Feature comparison bundle
codebrief bundle \
  --git-diff-options "--name-only" \
  --flatten src/ tests/ \
  --output "feature-changes-$(date +%Y%m%d).md"
```

### Bug Investigation

Create focused bundles for debugging:

```bash
# Bug investigation bundle
codebrief bundle \
  --output "bugs/investigation-$(date +%Y%m%d-%H%M).md" \
  --git-log-count 20 \
  --git-full-diff \
  --flatten src/problematic/ tests/failing/

# Minimal bug context
codebrief bundle \
  --exclude-deps \
  --exclude-tree \
  --git-log-count 5 \
  --flatten src/core/buggy_module.py \
  --output bug-minimal.md
```

### Code Review Preparation

Generate comprehensive review materials:

```bash
# Pull request bundle
codebrief bundle \
  --output "reviews/pr-$(git branch --show-current).md" \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/

# Review checklist bundle
codebrief bundle \
  --exclude-deps \
  --git-log-count 3 \
  --flatten src/ tests/ docs/REVIEW_CHECKLIST.md \
  --output review-ready.md
```

## 🏗️ Project Types

### Python Projects

Optimize bundles for Python development:

```bash
# Python web application
codebrief bundle \
  --output python-webapp-context.md \
  --flatten src/ tests/ requirements.txt pyproject.toml \
  --git-log-count 10

# Python library
codebrief bundle \
  --flatten src/ tests/ README.md setup.py \
  --exclude-tree \
  --output library-context.md

# Django project
codebrief bundle \
  --flatten myproject/ manage.py requirements.txt \
  --git-log-count 8 \
  --output django-context.md
```

### JavaScript/Node.js Projects

Tailor bundles for JavaScript development:

```bash
# React application
codebrief bundle \
  --flatten src/ public/ package.json \
  --git-log-count 12 \
  --output react-app-context.md

# Node.js API
codebrief bundle \
  --flatten routes/ models/ controllers/ package.json \
  --git-log-count 10 \
  --output nodejs-api-context.md

# Full-stack project
codebrief bundle \
  --flatten frontend/ backend/ package.json \
  --git-log-count 15 \
  --output fullstack-context.md
```

### Documentation Projects

Create bundles for documentation workflows:

```bash
# Documentation site
codebrief bundle \
  --exclude-git \
  --flatten docs/ README.md mkdocs.yml \
  --output docs-bundle.md

# API documentation
codebrief bundle \
  --flatten docs/api/ openapi.yaml README.md \
  --exclude-deps \
  --output api-docs-context.md
```

## 🚀 Automation Patterns

### Scheduled Context Generation

Automate regular context generation:

```bash
#!/bin/bash
# scheduled-context.sh

# Daily development summary
codebrief bundle \
  --output "daily/$(date +%Y-%m-%d)-summary.md" \
  --git-log-count 10 \
  --git-diff-options "--stat"

# Weekly comprehensive review
if [ $(date +%u) -eq 1 ]; then  # Monday
  codebrief bundle \
    --output "weekly/week-$(date +%Y-W%U)-review.md" \
    --git-log-count 50 \
    --git-full-diff
fi
```

### Git Hook Integration

Integrate with Git hooks for automatic context generation:

```bash
#!/bin/bash
# .git/hooks/post-commit

# Generate context after each commit
codebrief bundle \
  --output ".codebrief/latest-commit-context.md" \
  --git-log-count 3 \
  --git-full-diff \
  --flatten src/

echo "Context updated: .codebrief/latest-commit-context.md"
```

### CI/CD Pipeline Integration

Integrate bundles into continuous integration:

```yaml
# .github/workflows/context-bundle.yml
name: Generate Context Bundle

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  generate-bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install codebrief
        run: pip install codebrief

      - name: Generate Bundle
        run: |
          codebrief bundle \
            --output "context-${{ github.sha }}.md" \
            --git-log-count 10

      - name: Upload Bundle
        uses: actions/upload-artifact@v3
        with:
          name: context-bundle
          path: "context-${{ github.sha }}.md"
```

## 🎨 Advanced Customization

### Multi-Path Flattening

Create bundles with multiple specific paths:

```bash
# Multi-component bundle
codebrief bundle \
  --flatten src/auth/ \
  --flatten src/api/ \
  --flatten src/utils/ \
  --flatten tests/auth/ \
  --flatten tests/api/ \
  --output multi-component-context.md

# Cross-cutting concerns
codebrief bundle \
  --flatten src/logging/ \
  --flatten src/config/ \
  --flatten src/middleware/ \
  --exclude-deps \
  --output infrastructure-context.md
```

### Conditional Bundle Generation

Generate different bundles based on conditions:

```bash
#!/bin/bash
# conditional-bundle.sh

BRANCH=$(git branch --show-current)
HAS_CHANGES=$(git status --porcelain | wc -l)

if [ "$BRANCH" = "main" ]; then
  # Production bundle
  codebrief bundle \
    --output "production-context.md" \
    --git-log-count 20 \
    --exclude-files
elif [[ "$BRANCH" == feature/* ]]; then
  # Feature development bundle
  codebrief bundle \
    --output "feature-development.md" \
    --git-log-count 5 \
    --git-full-diff \
    --flatten src/ tests/
elif [ "$HAS_CHANGES" -gt 0 ]; then
  # Work-in-progress bundle
  codebrief bundle \
    --output "wip-context.md" \
    --git-log-count 3 \
    --git-full-diff
else
  # Standard development bundle
  codebrief bundle \
    --output "dev-context.md" \
    --git-log-count 10
fi
```

### Template-Based Bundles

Create reusable bundle templates:

```bash
# Template functions
bundle_for_review() {
  codebrief bundle \
    --exclude-deps \
    --git-log-count 5 \
    --git-full-diff \
    --flatten src/ tests/ \
    --output "${1:-review-bundle.md}"
}

bundle_for_onboarding() {
  codebrief bundle \
    --git-log-count 25 \
    --flatten README.md docs/ src/core/ \
    --output "${1:-onboarding-bundle.md}"
}

bundle_for_debugging() {
  codebrief bundle \
    --exclude-tree \
    --git-log-count 10 \
    --git-full-diff \
    --flatten "${1:-src/}" \
    --output "${2:-debug-bundle.md}"
}

# Usage
bundle_for_review "pr-123-review.md"
bundle_for_onboarding "new-dev-context.md"
bundle_for_debugging "src/problematic/" "bug-investigation.md"
```

## 📊 Analysis and Reporting

### Project Health Bundles

Generate bundles for project analysis:

```bash
# Health check bundle
codebrief bundle \
  --git-log-count 30 \
  --git-diff-options "--stat --numstat" \
  --flatten README.md CHANGELOG.md \
  --output health-check.md

# Technical debt analysis
codebrief bundle \
  --exclude-deps \
  --git-log-count 50 \
  --flatten src/ docs/technical-debt.md \
  --output tech-debt-analysis.md
```

### Performance Monitoring

Track bundle generation performance:

```bash
#!/bin/bash
# performance-bundle.sh

echo "Starting bundle generation at $(date)"
START_TIME=$(date +%s)

codebrief bundle \
  --output "performance-test-$(date +%Y%m%d-%H%M%S).md" \
  --git-log-count 20

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "Bundle generated in ${DURATION} seconds"
echo "Bundle size: $(du -h performance-test-*.md | tail -1)"
```

## 🔧 Configuration Patterns

### Project-Specific Bundle Configuration

Configure bundles for specific project needs:

```toml
# pyproject.toml
[tool.codebrief]
default_output_filename_bundle = "context/project-bundle.md"

# Optimize for Python projects
global_exclude_patterns = [
    "__pycache__/",
    "*.pyc",
    ".pytest_cache/",
    ".mypy_cache/",
    ".venv/",
    "venv/",
    "*.egg-info/",
    "build/",
    "dist/"
]

# Include common Python files
global_include_patterns = [
    "*.py",
    "*.md",
    "*.toml",
    "*.txt",
    "*.yml",
    "*.yaml"
]
```

### Environment-Specific Configuration

Set up different configurations for different environments:

```bash
# Development environment
export codebrief_BUNDLE_OUTPUT="dev-context.md"
export codebrief_GIT_LOG_COUNT=10

# Production environment
export codebrief_BUNDLE_OUTPUT="prod-context.md"
export codebrief_GIT_LOG_COUNT=25

# CI environment
export codebrief_BUNDLE_OUTPUT="ci-context-${CI_BUILD_ID}.md"
export codebrief_GIT_LOG_COUNT=15
```

## 🎯 Best Practices

### Bundle Organization

Organize your bundles effectively:

```bash
# Directory structure for bundles
mkdir -p {daily,weekly,features,releases,reviews,debugging}

# Daily bundles
codebrief bundle \
  --output "daily/$(date +%Y-%m-%d).md" \
  --git-log-count 5

# Feature bundles
codebrief bundle \
  --output "features/$(git branch --show-current).md" \
  --git-log-count 8

# Release bundles
codebrief bundle \
  --output "releases/v$(git describe --tags --abbrev=0).md" \
  --git-log-count 30
```

### Performance Optimization

Optimize bundle generation for large projects:

```bash
# Fast bundle for quick reviews
codebrief bundle \
  --exclude-tree \
  --exclude-deps \
  --git-log-count 3 \
  --flatten src/core/ \
  --output quick-review.md

# Comprehensive but optimized
codebrief bundle \
  --git-log-count 15 \
  --flatten src/ tests/ \
  --output optimized-comprehensive.md
```

### Team Collaboration

Establish team standards for bundle usage:

```bash
# Team review template
codebrief bundle \
  --exclude-deps \
  --git-log-count 5 \
  --flatten src/ tests/ docs/REVIEW.md \
  --output "reviews/$(git branch --show-current)-$(date +%Y%m%d).md"

# Handoff bundle for team transitions
codebrief bundle \
  --git-log-count 20 \
  --flatten README.md docs/ src/core/ \
  --output "handoffs/$(whoami)-to-team-$(date +%Y%m%d).md"
```

## 🚨 Troubleshooting

### Common Issues and Solutions

```bash
# Large repository optimization
codebrief bundle \
  --exclude-tree \
  --git-log-count 5 \
  --flatten src/specific-module/ \
  --output focused-bundle.md

# Memory-efficient bundle for huge projects
codebrief bundle \
  --exclude-files \
  --git-log-count 10 \
  --output metadata-only.md

# Network-friendly bundle (no large diffs)
codebrief bundle \
  --git-diff-options "--name-only" \
  --exclude-tree \
  --output network-friendly.md
```

---

*These examples showcase the versatility and power of codebrief's bundle command for various development workflows and project types.*
