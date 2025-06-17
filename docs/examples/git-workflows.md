# Git Workflow Examples

Learn how to integrate codebrief's Git tools into your development workflow for enhanced context generation and code review processes.

## 🔄 Git Context Extraction

### Basic Git Information

Extract essential Git context for your current project:

```bash
# Get basic Git context
codebrief git-info

# Save to file for sharing
codebrief git-info --output git-context.md
```

**Output Example:**
```markdown
# Git Context

## Repository Information
- **Current Branch:** feature/user-authentication
- **Repository Status:** Modified files present

## Recent Commits (Last 10)
1. **feat: add user login validation** (2024-01-15 14:30:25)
   - Author: Alice Developer <alice@example.com>
   - Hash: a1b2c3d

2. **fix: resolve password hashing issue** (2024-01-15 09:15:42)
   - Author: Bob Reviewer <bob@example.com>
   - Hash: e4f5g6h

## Uncommitted Changes
- Modified: src/auth/login.py
- Modified: tests/test_auth.py
- Added: docs/authentication.md
```

### Advanced Git Context

Get detailed Git information with full diffs:

```bash
# Include full diff of uncommitted changes
codebrief git-info --full-diff --log-count 5

# Custom diff options for specific information
codebrief git-info --diff-options "--stat --color=never"
```

## 📦 Bundle Integration

### Code Review Bundle

Create comprehensive bundles for code review:

```bash
# Complete review bundle
codebrief bundle \
  --output review-$(git branch --show-current).md \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/

# Focused review without dependencies
codebrief bundle \
  --exclude-deps \
  --flatten src/auth/ tests/auth/ \
  --git-log-count 3 \
  --output auth-review.md
```

### Feature Development Bundle

Document feature development progress:

```bash
# Feature branch context
codebrief bundle \
  --output feature-$(git branch --show-current)-context.md \
  --git-log-count 10 \
  --flatten src/features/$(git branch --show-current | cut -d'/' -f2)/
```

## 🚀 CI/CD Integration

### Pre-commit Hook

Add codebrief to your pre-commit workflow:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: codebrief-bundle
        name: Generate context bundle
        entry: codebrief bundle --output .codebrief/pre-commit-bundle.md
        language: system
        pass_filenames: false
        always_run: true
```

### GitHub Actions Workflow

Automate context generation in CI:

```yaml
# .github/workflows/context-generation.yml
name: Generate Context

on:
  pull_request:
    branches: [main, develop]

jobs:
  generate-context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git-info

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install codebrief
        run: |
          pip install codebrief

      - name: Generate PR Context Bundle
        run: |
          codebrief bundle \
            --output pr-context-${{ github.event.number }}.md \
            --git-log-count 10 \
            --git-full-diff \
            --exclude-deps

      - name: Upload Context Artifact
        uses: actions/upload-artifact@v3
        with:
          name: pr-context-${{ github.event.number }}
          path: pr-context-${{ github.event.number }}.md
```

## 🔍 Development Workflows

### Daily Development Context

Generate context for daily development work:

```bash
#!/bin/bash
# daily-context.sh

DATE=$(date +%Y-%m-%d)
BRANCH=$(git branch --show-current)

echo "Generating daily context for $BRANCH on $DATE..."

# Git context with recent activity
codebrief git-info \
  --log-count 15 \
  --output "daily-context/$DATE-git.md"

# Code changes bundle
codebrief bundle \
  --exclude-tree \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ \
  --output "daily-context/$DATE-changes.md"

echo "Context saved to daily-context/"
```

### Bug Investigation Bundle

Create focused bundles for bug investigation:

```bash
# Bug investigation context
codebrief bundle \
  --output bug-investigation-$(date +%Y%m%d).md \
  --git-log-count 20 \
  --git-diff-options "--name-only" \
  --flatten src/problematic_module/ tests/test_problematic/
```

### Release Preparation

Generate comprehensive release context:

```bash
# Release context bundle
codebrief bundle \
  --output release-v$(git describe --tags --abbrev=0)-context.md \
  --git-log-count 50 \
  --flatten CHANGELOG.md README.md docs/
```

## 🎯 Team Collaboration

### Code Review Templates

Create standardized review contexts:

```bash
# Template for feature reviews
codebrief bundle \
  --output templates/feature-review-template.md \
  --exclude-deps \
  --git-log-count 5 \
  --flatten src/ tests/ docs/

# Template for hotfix reviews
codebrief bundle \
  --output templates/hotfix-review-template.md \
  --git-log-count 3 \
  --git-full-diff \
  --flatten src/
```

### Knowledge Sharing

Share project context with new team members:

```bash
# Onboarding bundle
codebrief bundle \
  --output onboarding/project-overview.md \
  --git-log-count 25 \
  --flatten README.md docs/ src/core/

# Architecture overview
codebrief bundle \
  --exclude-git \
  --flatten src/ docs/architecture/ \
  --output onboarding/architecture-context.md
```

## 🛠️ Advanced Patterns

### Multi-Repository Context

For projects spanning multiple repositories:

```bash
#!/bin/bash
# multi-repo-context.sh

REPOS=("frontend" "backend" "shared-lib")
OUTPUT_DIR="multi-repo-context"

mkdir -p "$OUTPUT_DIR"

for repo in "${REPOS[@]}"; do
  echo "Processing $repo..."
  cd "$repo"

  codebrief bundle \
    --output "../$OUTPUT_DIR/$repo-context.md" \
    --git-log-count 10

  cd ..
done

echo "Multi-repository context generated in $OUTPUT_DIR/"
```

### Conditional Context Generation

Generate different contexts based on branch or conditions:

```bash
#!/bin/bash
# conditional-context.sh

BRANCH=$(git branch --show-current)

case "$BRANCH" in
  main|master)
    # Production context - comprehensive
    codebrief bundle \
      --output "contexts/production-context.md" \
      --git-log-count 20
    ;;
  develop)
    # Development context - focus on recent changes
    codebrief bundle \
      --output "contexts/development-context.md" \
      --git-log-count 10 \
      --git-full-diff
    ;;
  feature/*)
    # Feature context - focused on feature files
    FEATURE_NAME=$(echo "$BRANCH" | cut -d'/' -f2)
    codebrief bundle \
      --output "contexts/feature-$FEATURE_NAME-context.md" \
      --git-log-count 5 \
      --flatten "src/*$FEATURE_NAME*" "tests/*$FEATURE_NAME*"
    ;;
  hotfix/*)
    # Hotfix context - minimal, focused
    codebrief bundle \
      --exclude-deps \
      --exclude-tree \
      --git-log-count 3 \
      --git-full-diff \
      --output "contexts/hotfix-context.md"
    ;;
esac
```

## 📊 Context Analysis

### Git Activity Analysis

Analyze development patterns:

```bash
# Recent activity summary
codebrief git-info \
  --log-count 50 \
  --diff-options "--stat" \
  --output analysis/recent-activity.md

# Author contribution context
codebrief git-info \
  --log-count 100 \
  --output analysis/contributor-activity.md
```

### Change Impact Assessment

Assess the impact of changes:

```bash
# Impact assessment bundle
codebrief bundle \
  --git-full-diff \
  --git-diff-options "--stat --numstat" \
  --flatten src/ tests/ \
  --output impact-assessment.md
```

## 🔧 Configuration Examples

### Project-Specific Configuration

Configure codebrief for Git workflows:

```toml
# pyproject.toml
[tool.codebrief]
default_output_filename_git_info = "docs/git-context.md"
default_output_filename_bundle = "context/project-bundle.md"

# Exclude common Git-related files
global_exclude_patterns = [
    ".git/",
    "*.patch",
    "*.diff",
    ".gitignore",
    ".gitattributes"
]
```

### Environment Configuration

Set up environment for Git workflows:

```bash
# ~/.bashrc or ~/.zshrc

# codebrief Git workflow aliases
alias ccgit='codebrief git-info'
alias ccreview='codebrief bundle --exclude-deps --git-log-count 5'
alias ccfeature='codebrief bundle --git-full-diff --flatten src/ tests/'

# Function for branch-specific context
ccbranch() {
    local branch=$(git branch --show-current)
    codebrief bundle \
        --output "context-$branch-$(date +%Y%m%d).md" \
        --git-log-count 10 \
        "$@"
}
```

## 🎉 Best Practices

### Context Generation Guidelines

1. **Regular Context Updates**: Generate context regularly during development
2. **Branch-Specific Context**: Create different contexts for different branches
3. **Focused Bundles**: Use selective inclusion for specific purposes
4. **Automated Generation**: Integrate into CI/CD for consistency
5. **Team Standards**: Establish team conventions for context generation

### Performance Optimization

```bash
# For large repositories - optimize performance
codebrief bundle \
  --exclude-tree \
  --git-log-count 5 \
  --flatten src/core/ \
  --output optimized-context.md

# For quick reviews - minimal context
codebrief git-info \
  --log-count 3 \
  --diff-options "--name-only"
```

---

*These examples demonstrate the power of combining Git context with codebrief's bundling capabilities for enhanced development workflows.*
