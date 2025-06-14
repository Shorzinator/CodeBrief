# Advanced Workflows

Master ContextCraft with sophisticated workflows, automation patterns, and integration strategies for professional development environments.

## Overview

Advanced workflows help you:

- **Automate Context Generation** for consistent results
- **Integrate with CI/CD** pipelines for team collaboration
- **Create Custom Templates** for specific use cases
- **Optimize Performance** for large projects
- **Scale Usage** across teams and organizations

## Automation Patterns

### Context Generation Scripts

Create reusable scripts for common context patterns:

```bash
#!/bin/bash
# scripts/generate-context.sh - Automated context generation

set -euo pipefail

PROJECT_ROOT="${1:-.}"
OUTPUT_DIR="${2:-./context-outputs}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🔄 Generating comprehensive project context..."

# Core context files
contextcraft bundle \
  --output "$OUTPUT_DIR/complete-context-$TIMESTAMP.md" \
  "$PROJECT_ROOT"

contextcraft tree \
  --output "$OUTPUT_DIR/structure-$TIMESTAMP.txt" \
  "$PROJECT_ROOT"

contextcraft deps \
  --output "$OUTPUT_DIR/dependencies-$TIMESTAMP.md" \
  "$PROJECT_ROOT"

contextcraft git-info \
  --log-count 10 \
  --output "$OUTPUT_DIR/git-context-$TIMESTAMP.md" \
  "$PROJECT_ROOT"

# Specialized contexts
contextcraft flatten "$PROJECT_ROOT/src" \
  --include "*.py" \
  --exclude "*test*" "*__pycache__*" \
  --output "$OUTPUT_DIR/source-code-$TIMESTAMP.md"

contextcraft flatten "$PROJECT_ROOT" \
  --include "*.md" "*.rst" "*.txt" \
  --exclude "**/node_modules/**" "**/venv/**" \
  --output "$OUTPUT_DIR/documentation-$TIMESTAMP.md"

echo "✅ Context generation complete!"
echo "📁 Files saved to: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR/"*$TIMESTAMP*
```

### Makefile Integration

```makefile
# Makefile - Context generation targets

.PHONY: context context-clean context-dev context-review

CONTEXT_DIR := context-outputs
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

# Generate all context types
context:
	@echo "Generating comprehensive project context..."
	@mkdir -p $(CONTEXT_DIR)
	poetry run contextcraft bundle --output $(CONTEXT_DIR)/bundle-$(TIMESTAMP).md
	poetry run contextcraft tree --output $(CONTEXT_DIR)/tree-$(TIMESTAMP).txt
	poetry run contextcraft deps --output $(CONTEXT_DIR)/deps-$(TIMESTAMP).md
	poetry run contextcraft git-info --output $(CONTEXT_DIR)/git-$(TIMESTAMP).md
	@echo "Context files generated in $(CONTEXT_DIR)/"

# Development-focused context
context-dev:
	@mkdir -p $(CONTEXT_DIR)
	poetry run contextcraft bundle \
		--exclude-deps \
		--git-full-diff \
		--flatten src/ tests/ \
		--output $(CONTEXT_DIR)/dev-context-$(TIMESTAMP).md

# Code review context
context-review:
	@mkdir -p $(CONTEXT_DIR)
	poetry run contextcraft bundle \
		--git-log-count 5 \
		--git-full-diff \
		--output $(CONTEXT_DIR)/review-context-$(TIMESTAMP).md

# Clean old context files
context-clean:
	@echo "Cleaning old context files..."
	find $(CONTEXT_DIR) -name "*.md" -mtime +7 -delete
	find $(CONTEXT_DIR) -name "*.txt" -mtime +7 -delete
	@echo "Old context files removed."
```

### Python Automation

```python
#!/usr/bin/env python3
"""
advanced_context.py - Advanced context generation automation
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ContextGenerator:
    def __init__(self, project_root: str = ".", output_dir: str = "context-outputs"):
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def setup_output_dir(self):
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(exist_ok=True)

    def run_contextcraft(self, command: List[str], output_file: str) -> bool:
        """Run a contextcraft command and save output."""
        try:
            full_command = ["poetry", "run", "contextcraft"] + command + [
                "--output", str(self.output_dir / output_file)
            ]

            result = subprocess.run(
                full_command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running command {' '.join(command)}: {e}")
            return False

    def generate_standard_context(self):
        """Generate standard context files."""
        contexts = [
            (["bundle"], f"complete-context-{self.timestamp}.md"),
            (["tree"], f"structure-{self.timestamp}.txt"),
            (["deps"], f"dependencies-{self.timestamp}.md"),
            (["git-info", "--log-count", "10"], f"git-context-{self.timestamp}.md"),
        ]

        for command, output_file in contexts:
            print(f"Generating {output_file}...")
            self.run_contextcraft(command, output_file)

    def generate_specialized_context(self):
        """Generate specialized context files."""
        # Source code only
        self.run_contextcraft([
            "flatten", "src/",
            "--include", "*.py",
            "--exclude", "*test*", "*__pycache__*"
        ], f"source-code-{self.timestamp}.md")

        # Documentation only
        self.run_contextcraft([
            "flatten", ".",
            "--include", "*.md", "*.rst", "*.txt",
            "--exclude", "**/node_modules/**", "**/venv/**"
        ], f"documentation-{self.timestamp}.md")

        # Tests only
        self.run_contextcraft([
            "flatten", "tests/",
            "--include", "*.py"
        ], f"tests-{self.timestamp}.md")

    def generate_custom_bundles(self):
        """Generate custom bundle configurations."""
        bundles = {
            "review": {
                "args": ["--git-log-count", "5", "--git-full-diff"],
                "filename": f"review-bundle-{self.timestamp}.md"
            },
            "debug": {
                "args": ["--exclude-deps", "--git-full-diff", "--flatten", "src/"],
                "filename": f"debug-bundle-{self.timestamp}.md"
            },
            "architecture": {
                "args": ["--exclude-git", "--flatten", "src/", "docs/"],
                "filename": f"architecture-bundle-{self.timestamp}.md"
            }
        }

        for bundle_type, config in bundles.items():
            print(f"Generating {bundle_type} bundle...")
            self.run_contextcraft(
                ["bundle"] + config["args"],
                config["filename"]
            )

    def generate_metadata(self):
        """Generate metadata about the context generation."""
        metadata = {
            "timestamp": self.timestamp,
            "project_root": str(self.project_root.absolute()),
            "output_dir": str(self.output_dir.absolute()),
            "generated_files": list(self.output_dir.glob(f"*{self.timestamp}*")),
            "git_branch": self.get_git_branch(),
            "git_commit": self.get_git_commit()
        }

        metadata_file = self.output_dir / f"metadata-{self.timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)

    def get_git_branch(self) -> Optional[str]:
        """Get current git branch."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def get_git_commit(self) -> Optional[str]:
        """Get current git commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def run_full_generation(self):
        """Run complete context generation workflow."""
        print("🔄 Starting advanced context generation...")

        self.setup_output_dir()
        self.generate_standard_context()
        self.generate_specialized_context()
        self.generate_custom_bundles()
        self.generate_metadata()

        print("✅ Context generation complete!")
        print(f"📁 Files saved to: {self.output_dir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Advanced ContextCraft automation")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output-dir", default="context-outputs", help="Output directory")

    args = parser.parse_args()

    generator = ContextGenerator(args.project_root, args.output_dir)
    generator.run_full_generation()
```

## CI/CD Integration

### GitHub Actions Workflows

```yaml
# .github/workflows/context-generation.yml
name: Generate Project Context

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM UTC

jobs:
  generate-context:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for Git context

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load Cached Dependencies
        id: cached-poetry-dependencies
        uses: actions/cache@v3
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install Dependencies
        if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
        run: poetry install --no-interaction --no-root

      - name: Install ContextCraft
        run: poetry install --no-interaction

      - name: Generate Context Files
        run: |
          mkdir -p context-outputs

          # Generate comprehensive bundle
          poetry run contextcraft bundle \
            --output context-outputs/project-bundle.md

          # Generate focused contexts
          poetry run contextcraft tree \
            --output context-outputs/project-structure.txt

          poetry run contextcraft deps \
            --output context-outputs/dependencies.md

          poetry run contextcraft git-info \
            --log-count 10 \
            --output context-outputs/git-context.md

          # Generate specialized bundles
          poetry run contextcraft bundle \
            --exclude-deps \
            --git-full-diff \
            --flatten src/ tests/ \
            --output context-outputs/development-context.md

      - name: Upload Context Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: project-context-${{ github.sha }}
          path: context-outputs/
          retention-days: 30

      - name: Comment on PR (if PR)
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const contextBundle = fs.readFileSync('context-outputs/project-bundle.md', 'utf8');

            // Truncate if too long for comment
            const maxLength = 50000;
            const truncatedBundle = contextBundle.length > maxLength
              ? contextBundle.substring(0, maxLength) + '\n\n... (truncated)'
              : contextBundle;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🤖 Generated Project Context\n\n<details>\n<summary>Click to expand project context</summary>\n\n\`\`\`markdown\n${truncatedBundle}\n\`\`\`\n\n</details>`
            });
```

### GitLab CI Integration

```yaml
# .gitlab-ci.yml
stages:
  - context
  - deploy-context

variables:
  CONTEXT_DIR: "context-outputs"

generate-context:
  stage: context
  image: python:3.11

  before_script:
    - pip install poetry
    - poetry config virtualenvs.create false
    - poetry install

  script:
    - mkdir -p $CONTEXT_DIR

    # Generate context files
    - poetry run contextcraft bundle --output $CONTEXT_DIR/project-bundle.md
    - poetry run contextcraft tree --output $CONTEXT_DIR/structure.txt
    - poetry run contextcraft deps --output $CONTEXT_DIR/dependencies.md
    - poetry run contextcraft git-info --log-count 15 --output $CONTEXT_DIR/git-context.md

    # Generate specialized contexts
    - poetry run contextcraft flatten src/ --include "*.py" --output $CONTEXT_DIR/source-code.md
    - poetry run contextcraft bundle --exclude-deps --git-full-diff --output $CONTEXT_DIR/debug-context.md

  artifacts:
    paths:
      - $CONTEXT_DIR/
    expire_in: 1 week

  only:
    - main
    - develop
    - merge_requests

deploy-context-to-pages:
  stage: deploy-context
  image: alpine:latest

  before_script:
    - apk add --no-cache pandoc

  script:
    - mkdir -p public

    # Convert Markdown to HTML
    - for file in $CONTEXT_DIR/*.md; do
        pandoc "$file" -f markdown -t html -s --css=style.css -o "public/$(basename "$file" .md).html"
      done

    # Create index page
    - echo '<h1>Project Context</h1>' > public/index.html
    - echo '<ul>' >> public/index.html
    - for file in public/*.html; do
        if [ "$(basename "$file")" != "index.html" ]; then
          echo "<li><a href=\"$(basename "$file")\">$(basename "$file" .html)</a></li>" >> public/index.html
        fi
      done
    - echo '</ul>' >> public/index.html

  artifacts:
    paths:
      - public

  only:
    - main
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        CONTEXT_DIR = 'context-outputs'
        POETRY_HOME = '/opt/poetry'
        PATH = "${POETRY_HOME}/bin:${PATH}"
    }

    stages {
        stage('Setup') {
            steps {
                sh 'python -m pip install poetry'
                sh 'poetry install'
            }
        }

        stage('Generate Context') {
            parallel {
                stage('Bundle Context') {
                    steps {
                        sh "mkdir -p ${CONTEXT_DIR}"
                        sh "poetry run contextcraft bundle --output ${CONTEXT_DIR}/project-bundle.md"
                    }
                }

                stage('Structure Context') {
                    steps {
                        sh "poetry run contextcraft tree --output ${CONTEXT_DIR}/structure.txt"
                    }
                }

                stage('Dependencies Context') {
                    steps {
                        sh "poetry run contextcraft deps --output ${CONTEXT_DIR}/dependencies.md"
                    }
                }

                stage('Git Context') {
                    steps {
                        sh "poetry run contextcraft git-info --log-count 10 --output ${CONTEXT_DIR}/git-context.md"
                    }
                }
            }
        }

        stage('Archive Context') {
            steps {
                archiveArtifacts artifacts: "${CONTEXT_DIR}/**", fingerprint: true

                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: CONTEXT_DIR,
                    reportFiles: '*.md',
                    reportName: 'Project Context Report'
                ])
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
```

## Performance Optimization

### Large Project Strategies

```bash
#!/bin/bash
# optimize-large-project.sh - Optimized context generation for large projects

set -euo pipefail

PROJECT_ROOT="${1:-.}"
OUTPUT_DIR="${2:-./context-outputs}"

echo "🔄 Optimizing context generation for large project..."

# Create focused contexts instead of one large bundle
mkdir -p "$OUTPUT_DIR/focused"

# Core architecture (exclude tests and build artifacts)
contextcraft tree \
  --ignore "tests/" "build/" "dist/" "node_modules/" "__pycache__/" \
  --output "$OUTPUT_DIR/focused/core-structure.txt" \
  "$PROJECT_ROOT"

# Main source code only (exclude tests, docs, configs)
contextcraft flatten "$PROJECT_ROOT/src" \
  --include "*.py" "*.js" "*.ts" "*.go" "*.rs" \
  --exclude "*test*" "*spec*" "*__pycache__*" \
  --output "$OUTPUT_DIR/focused/main-source.md"

# Recent changes only (last 5 commits)
contextcraft git-info \
  --log-count 5 \
  --diff-options "--stat" \
  --output "$OUTPUT_DIR/focused/recent-changes.md" \
  "$PROJECT_ROOT"

# Critical dependencies only
contextcraft deps \
  --output "$OUTPUT_DIR/focused/dependencies.md" \
  "$PROJECT_ROOT"

# Create a minimal bundle
contextcraft bundle \
  --exclude-git \
  --flatten "$PROJECT_ROOT/src/core" "$PROJECT_ROOT/src/main" \
  --output "$OUTPUT_DIR/focused/minimal-bundle.md" \
  "$PROJECT_ROOT"

echo "✅ Focused context generation complete!"
echo "📁 Optimized files saved to: $OUTPUT_DIR/focused/"
```

### Parallel Processing

```python
#!/usr/bin/env python3
"""
parallel_context.py - Parallel context generation for faster processing
"""

import concurrent.futures
import subprocess
from pathlib import Path
from typing import List, Tuple

class ParallelContextGenerator:
    def __init__(self, project_root: str = ".", output_dir: str = "context-outputs"):
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def run_command(self, command_config: Tuple[List[str], str]) -> Tuple[bool, str]:
        """Run a single contextcraft command."""
        command, output_file = command_config

        try:
            full_command = ["poetry", "run", "contextcraft"] + command + [
                "--output", str(self.output_dir / output_file)
            ]

            result = subprocess.run(
                full_command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return True, f"✅ Generated {output_file}"
        except subprocess.CalledProcessError as e:
            return False, f"❌ Failed to generate {output_file}: {e}"

    def generate_parallel_context(self):
        """Generate multiple context files in parallel."""
        commands = [
            (["tree"], "structure.txt"),
            (["deps"], "dependencies.md"),
            (["git-info", "--log-count", "10"], "git-context.md"),
            (["flatten", "src/", "--include", "*.py"], "source-code.md"),
            (["flatten", ".", "--include", "*.md", "*.rst"], "documentation.md"),
            (["bundle", "--exclude-deps"], "code-bundle.md"),
            (["bundle", "--exclude-git"], "static-bundle.md"),
        ]

        print(f"🔄 Running {len(commands)} context generation tasks in parallel...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_command = {
                executor.submit(self.run_command, cmd_config): cmd_config
                for cmd_config in commands
            }

            for future in concurrent.futures.as_completed(future_to_command):
                success, message = future.result()
                print(message)

        print("✅ Parallel context generation complete!")

if __name__ == "__main__":
    generator = ParallelContextGenerator()
    generator.generate_parallel_context()
```

## Template System

### Context Templates

Create reusable templates for common scenarios:

```bash
# templates/code-review-template.sh
#!/bin/bash
# Code Review Context Template

contextcraft bundle \
  --output "review-context.md" \
  --git-log-count 5 \
  --git-full-diff \
  --flatten src/ tests/

echo "📝 Code review context generated: review-context.md"
echo "🔗 Share this with reviewers or paste into LLM for analysis"
```

```bash
# templates/debugging-template.sh
#!/bin/bash
# Debugging Context Template

PROJECT_PATH="${1:-.}"
ISSUE_AREA="${2:-src/}"

contextcraft git-info \
  --full-diff \
  --diff-options "--stat" \
  --output "debug-git-context.md" \
  "$PROJECT_PATH"

contextcraft flatten "$ISSUE_AREA" \
  --include "*.py" "*.js" "*.ts" \
  --exclude "*test*" \
  --output "debug-code-context.md"

contextcraft bundle \
  --exclude-deps \
  --git-full-diff \
  --flatten "$ISSUE_AREA" \
  --output "debug-bundle.md" \
  "$PROJECT_PATH"

echo "🐛 Debugging context generated for $ISSUE_AREA"
echo "Files: debug-git-context.md, debug-code-context.md, debug-bundle.md"
```

```bash
# templates/architecture-template.sh
#!/bin/bash
# Architecture Analysis Template

contextcraft bundle \
  --exclude-git \
  --flatten src/ docs/ \
  --output "architecture-context.md"

contextcraft tree \
  --ignore "tests/" "build/" "__pycache__/" \
  --output "architecture-structure.txt"

contextcraft deps \
  --output "architecture-dependencies.md"

echo "🏗️ Architecture context generated"
echo "Files: architecture-context.md, architecture-structure.txt, architecture-dependencies.md"
```

### Configuration Templates

```toml
# .contextcraft/templates/minimal.toml
[tool.contextcraft]
default_output_filename_bundle = "minimal-bundle.md"
global_exclude_patterns = [
    "*.log", "*.tmp", "__pycache__/", "node_modules/",
    "build/", "dist/", ".git/", ".venv/"
]

[tool.contextcraft.bundle]
exclude_deps = true
exclude_git = true
flatten_paths = ["src/core/"]
```

```toml
# .contextcraft/templates/comprehensive.toml
[tool.contextcraft]
default_output_filename_bundle = "comprehensive-bundle.md"
default_output_filename_tree = "full-structure.txt"
default_output_filename_deps = "all-dependencies.md"
default_output_filename_git_info = "git-history.md"

global_exclude_patterns = [
    "*.log", "*.tmp", "__pycache__/",
    "node_modules/", ".git/"
]

[tool.contextcraft.bundle]
git_log_count = 15
git_full_diff = true
flatten_paths = ["src/", "tests/", "docs/"]
```

## Team Collaboration

### Shared Context Standards

```bash
# team-scripts/shared-context.sh
#!/bin/bash
# Shared team context generation standards

CONTEXT_TYPE="${1:-standard}"
OUTPUT_PREFIX="${2:-team-context}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

case "$CONTEXT_TYPE" in
  "onboarding")
    contextcraft bundle \
      --output "${OUTPUT_PREFIX}-onboarding-${TIMESTAMP}.md" \
      --flatten src/ docs/ README.md
    ;;

  "review")
    contextcraft bundle \
      --output "${OUTPUT_PREFIX}-review-${TIMESTAMP}.md" \
      --git-log-count 10 \
      --git-full-diff \
      --flatten src/ tests/
    ;;

  "architecture")
    contextcraft bundle \
      --output "${OUTPUT_PREFIX}-architecture-${TIMESTAMP}.md" \
      --exclude-git \
      --flatten src/ docs/architecture/
    ;;

  "debug")
    contextcraft bundle \
      --output "${OUTPUT_PREFIX}-debug-${TIMESTAMP}.md" \
      --git-full-diff \
      --exclude-deps \
      --flatten src/
    ;;

  *)
    contextcraft bundle \
      --output "${OUTPUT_PREFIX}-standard-${TIMESTAMP}.md"
    ;;
esac

echo "✅ Team context ($CONTEXT_TYPE) generated: ${OUTPUT_PREFIX}-${CONTEXT_TYPE}-${TIMESTAMP}.md"
```

### Documentation Integration

```bash
# docs-integration/update-context-docs.sh
#!/bin/bash
# Automatically update documentation with fresh context

# Generate fresh context for documentation
contextcraft tree --output docs/project-structure.txt
contextcraft deps --output docs/dependencies.md

# Update architecture documentation
contextcraft bundle \
  --exclude-git \
  --flatten src/core/ src/api/ \
  --output docs/architecture-context.md

# Generate API context
contextcraft flatten src/api/ \
  --include "*.py" \
  --exclude "*test*" \
  --output docs/api-context.md

echo "📚 Documentation context updated"
echo "Files updated: docs/project-structure.txt, docs/dependencies.md"
echo "               docs/architecture-context.md, docs/api-context.md"
```

## Monitoring and Analytics

### Context Generation Metrics

```python
#!/usr/bin/env python3
"""
context_metrics.py - Track context generation metrics
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ContextMetrics:
    def __init__(self, metrics_file: str = "context-metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.metrics = self.load_metrics()

    def load_metrics(self) -> Dict[str, Any]:
        """Load existing metrics or create new structure."""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        return {
            "total_generations": 0,
            "generation_history": [],
            "command_usage": {},
            "performance_stats": {}
        }

    def save_metrics(self):
        """Save metrics to file."""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)

    def record_generation(self, command: str, execution_time: float,
                         output_size: int, success: bool = True):
        """Record a context generation event."""
        self.metrics["total_generations"] += 1

        generation_record = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "execution_time": execution_time,
            "output_size": output_size,
            "success": success
        }

        self.metrics["generation_history"].append(generation_record)

        # Update command usage stats
        if command not in self.metrics["command_usage"]:
            self.metrics["command_usage"][command] = 0
        self.metrics["command_usage"][command] += 1

        # Update performance stats
        if command not in self.metrics["performance_stats"]:
            self.metrics["performance_stats"][command] = {
                "avg_time": 0.0,
                "avg_size": 0,
                "total_runs": 0
            }

        stats = self.metrics["performance_stats"][command]
        stats["total_runs"] += 1
        stats["avg_time"] = (stats["avg_time"] * (stats["total_runs"] - 1) + execution_time) / stats["total_runs"]
        stats["avg_size"] = (stats["avg_size"] * (stats["total_runs"] - 1) + output_size) / stats["total_runs"]

        self.save_metrics()

    def get_performance_report(self) -> str:
        """Generate a performance report."""
        report = ["📊 ContextCraft Performance Report", "=" * 40]

        report.append(f"Total generations: {self.metrics['total_generations']}")
        report.append(f"Commands used: {len(self.metrics['command_usage'])}")

        report.append("\n🔝 Most Used Commands:")
        sorted_commands = sorted(
            self.metrics["command_usage"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for cmd, count in sorted_commands[:5]:
            report.append(f"  {cmd}: {count} times")

        report.append("\n⚡ Performance Stats:")
        for cmd, stats in self.metrics["performance_stats"].items():
            avg_time = stats["avg_time"]
            avg_size = stats["avg_size"]
            runs = stats["total_runs"]
            report.append(f"  {cmd}: {avg_time:.2f}s avg, {avg_size:,} bytes avg ({runs} runs)")

        return "\n".join(report)

# Usage wrapper
def timed_contextcraft_run(command: str, metrics: ContextMetrics):
    """Wrapper to time contextcraft commands and record metrics."""
    import subprocess

    start_time = time.time()
    try:
        result = subprocess.run(
            ["poetry", "run", "contextcraft"] + command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        execution_time = time.time() - start_time
        output_size = len(result.stdout.encode('utf-8'))

        metrics.record_generation(command, execution_time, output_size, True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        execution_time = time.time() - start_time
        metrics.record_generation(command, execution_time, 0, False)
        return False, str(e)

if __name__ == "__main__":
    metrics = ContextMetrics()
    print(metrics.get_performance_report())
```

## Next Steps

- **[CI/CD Integration Tutorial](cicd-integration.md)** - Detailed CI/CD setup
- **[LLM Integration Guide](llm-integration.md)** - AI-specific workflows
- **[Configuration Reference](../getting-started/configuration.md)** - Advanced configuration
- **[Contributing](../development/contributing.md)** - Help improve ContextCraft
