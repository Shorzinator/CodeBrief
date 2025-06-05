# <h1 style="text-align: center;">ContextCraft</h1>

## **Project Plan of Action**

**Project Vision:**
To provide developers with a simple, extensible, and portable Python CLI toolkit that can be easily integrated into any project to generate comprehensive, structured context for Large Language Models, facilitating debugging, code understanding, and AI-assisted development.

**Core Philosophy:**
*   **Developer-Centric:** Built with the developer experience in mind.
*   **Modularity & Extensibility:** Designed for easy addition of new tools and features.
*   **Simplicity & Usability:** Intuitive CLI, minimal setup, clear and useful outputs.
*   **Portability & Distribution:** Usable via direct clone or PyPI installation.
*   **High Quality:** Emphasis on robust code, thorough testing, and excellent documentation.
*   **LLM-Focused Output:** Prioritize output formats (like Markdown) that are easily digestible by LLMs.

---

**Phase 0: Foundation & Planning (Status: LARGELY COMPLETE)**

1.  **Detailed Requirements & Scope Definition (Status: REFINED)**
    *   MVP, V1.0, and Future Scope outlined (see Phase 1 & 2 for active items).
2.  **Technology Stack Selection (Status: DONE)**
    *   **Primary Language:** Python 3.9+
    *   **Project & Dependency Management:** Poetry
    *   **CLI Framework:** Typer
    *   **CLI Output Enhancement:** Rich
    *   **Linting/Formatting/Import Sorting:** Ruff
    *   **Type Checking:** Mypy (target strict)
    *   **Security Linting:** Bandit
    *   **Testing Framework:** pytest (with `pytest-cov`)
    *   **Version Control:** Git (hosted on GitHub)
    *   **Documentation:** MkDocs (Material theme, `mkdocstrings`)
    *   **Changelog Automation:** Release Drafter (with Conventional Commits)
    *   **CI/CD:** GitHub Actions
3.  **Project Structure & Architecture (Status: DONE)**
    *   Initialized project using Poetry.
    *   Using `src/contextcraft/` layout for library code.
    *   Modular design with `tools/` sub-package for specific functionalities.
    *   CLI commands defined via Typer in `src/contextcraft/main.py`.
4.  **Setup GitHub Repository (Status: IN PROGRESS/NEEDS VERIFICATION)**
    *   Repository created. (Assuming this is done by you)
    *   Initialized with Poetry (`pyproject.toml`). (DONE)
    *   `LICENSE` (MIT or Apache 2.0) & `README.md` (basic). (TODO if not done)
    *   Standard Python `.gitignore`. (DONE - Poetry likely added one)
    *   Branch protection for `main` (require PRs, status checks). (TODO if not done)
    *   `develop` branch for ongoing work. (TODO if not done)
    *   Enable **Dependabot** for security/version updates. (TODO)

---

**Phase 1: MVP Development (Status: IN PROGRESS ~4-6 weeks total estimate)**

1.  **Environment & Tooling Setup (Status: IN PROGRESS)**
    *   Poetry environment setup. (DONE)
    *   Editor/IDE configured for Ruff, Mypy. (DONE)
    *   **(TODO Next Block)** Set up **pre-commit hooks** (Ruff, Mypy, Bandit, etc.) after `flatten` command integration.
2.  **Core CLI Orchestrator (Status: DONE)**
    *   `src/contextcraft/main.py` implemented with Typer.
    *   Handles command registration and basic app structure.
3.  **Tool 1: Directory Tree Generator (`tree` command) (Status: LARGELY DONE)**
    *   Logic implemented in `src/contextcraft/tools/tree_generator.py`. (DONE)
    *   Handles `root_dir`, `--output`, and basic `--ignore` options. (DONE)
    *   Uses `rich.tree.Tree` for console output, plain text for file. (DONE)
    *   Default exclusion list (`DEFAULT_EXCLUDED_ITEMS`) implemented. (DONE)
    *   Production-level docstrings and comments added. (DONE)
    *   **(TODO)** Write comprehensive unit tests with `pytest`.
4.  **Tool 2: Code Flattener (`flatten` command) (Status: TODO - CURRENT FOCUS)**
    *   Refactor existing `flatten.py` script into `src/contextcraft/tools/flattener.py`.
    *   Integrate as a `flatten` command in `main.py` using Typer.
    *   Implement options for `root_dir`, `output_file`, basic `--ignore` (names), and `--include` (file extensions/patterns).
    *   Prepend flattened file content with a clear marker comment indicating original path (e.g., Markdown-friendly `# --- File: path/to/file.ext ---`).
    *   Handle `UnicodeDecodeError` for binary files gracefully.
    *   Add production-level docstrings and comments.
    *   Write comprehensive unit tests with `pytest`.
5.  **Initial CI Setup (GitHub Actions) (Status: TODO)**
    *   Implement workflows triggered on push/PR to `develop` and `main`.
    *   Jobs for:
        *   **Ruff:** Linting and formatting checks.
        *   **Mypy:** Static type checking.
        *   **Bandit:** Security vulnerability scanning.
        *   **Pytest:** Running unit tests with code coverage reporting (`pytest-cov`).
6.  **Basic Documentation (MkDocs) (Status: TODO)**
    *   Set up MkDocs with the Material theme.
    *   Configure `mkdocstrings` for pulling docs from code.
    *   Create initial pages: Home (`README.md` content), Installation, CLI Usage (for `tree` and `flatten`).
7.  **Internal Testing & Refinement (Status: ONGOING)**
    *   Continuously test implemented features on diverse local projects.
    *   Refine CLI usability, output formatting, and error messages based on usage.

---

**Phase 2: V1.0 Feature Development & Refinement (Status: PLANNED ~5-10 weeks post-MVP)**

*Process for each feature: Design -> Implement -> Test (Unit & Integration) -> Document (MkDocs)*

1.  **`.llmignore` System:**
    *   Implement parsing of `.llmignore` file(s) (similar to `.gitignore` syntax, supporting glob patterns).
    *   Integrate `.llmignore` logic into `tree` and `flatten` commands, and future tools.
    *   Define precedence (e.g., project `.llmignore` overrides global/default ignores).
2.  **Configuration File:**
    *   Implement support for a project-level configuration file (e.g., in `pyproject.toml` under `[tool.contextcraft]` or a dedicated `contextcraft.toml`).
    *   Allow users to set default values for common options (e.g., default output filename, common ignores).
3.  **Tool 3: Dependency Lister (`deps` command):**
    *   Implement logic to identify and list project dependencies.
    *   Initial support for Python: `pyproject.toml` (Poetry/PEP 621), `requirements.txt`.
    *   Initial support for Node.js: `package.json`.
    *   Design for extensibility to support more languages/package managers later.
4.  **Tool 4: Git Context Provider (`git-info` command):**
    *   Implement functionality to extract relevant Git information:
        *   `git status --short` (changed/untracked files).
        *   `git diff HEAD` (uncommitted changes to tracked files).
        *   `git log -n 5 --oneline` (recent commits).
        *   Current branch name.
    *   Handle cases gracefully if not in a Git repository.
5.  **"Bundle" Command (`bundle` command):**
    *   The flagship command to aggregate context from multiple tools.
    *   Allow users to specify which context pieces to include (e.g., tree, specific flattened files, deps, git-info).
    *   Format the combined output as a single **Markdown (.md) file**, with clear sections for each piece of context.
    *   Utilize `Rich` for any console progress/summary.
6.  **Clipboard Integration:**
    *   Add a global option (e.g., `--to-clipboard` or a dedicated command) to copy the output of commands (especially `bundle`) directly to the system clipboard (using `pyperclip` or similar).
7.  **Testing Enhancements:**
    *   Increase unit test coverage towards a high target (e.g., >90%).
    *   Implement integration tests for CLI commands and their interactions.
    *   Consider property-based testing with `hypothesis` for key parsing/logic functions.
8.  **Documentation Overhaul & DX:**
    *   Comprehensive documentation for all commands, options, `.llmignore` syntax, configuration files.
    *   Tutorials or example use cases.
    *   `CONTRIBUTING.md`: Guidelines for development setup, running tests, coding style, PR process.
    *   Implement **Conventional Commits** for commit messages.
    *   Set up **Release Drafter** GitHub Action for automated changelog generation based on Conventional Commits and PR labels.

---

**Phase 3: Release & Distribution (Status: PLANNED - Post V1.0 features)**

1.  **PyPI Release:**
    *   Prepare project for PyPI distribution using Poetry.
    *   Update `pyproject.toml` with classifiers, keywords, homepage URL, etc.
    *   CI/CD: Enhance GitHub Actions workflow to:
        *   Build wheel and source distribution on tagged commits.
        *   Generate SBOM (`Syft`) and scan for vulnerabilities (`Grype`).
        *   Automatically publish to PyPI (or TestPyPI first).
2.  **Versioning Strategy:**
    *   Strict Semantic Versioning (e.g., `v0.1.0` for MVP, `v1.0.0` for stable V1.0).
    *   Use `poetry version <semver>` and Git tags for releases.
    *   Maintain `CHANGELOG.md` (automated via Release Drafter).
3.  **Community & Feedback:**
    *   Utilize GitHub Issues for bug tracking and feature requests.
    *   Establish clear contribution guidelines in `CONTRIBUTING.md`.
    *   (Optional) Consider CLA assistant if external contributions become significant.

---

**Phase 4: Maintenance & Future Iteration (Status: ONGOING - Post V1.0)**

1.  **Bug Fixes & Enhancements:**
    *   Address reported issues and implement prioritized enhancements.
2.  **New Features (from "Future Scope" backlog):**
    *   **Log/Output Snippet Grabber:** Utility to fetch recent lines from specified log/output files.
    *   **Environment Variable Lister:** Securely list relevant (non-sensitive) environment variables.
    *   **File Content Snippet Extractor:** Extract specific code blocks/functions (potentially using `tree-sitter`).
    *   **Support for more languages/dependency systems:** Expand dependency lister and default ignores.
    *   **Interactive mode for ad-hoc exclusions:** For `tree`, `flatten`, etc.
    *   **Advanced Logging:** Integrate `structlog` for more detailed structured logging if needed.
    *   **Error Tracking:** Consider Sentry for automated error reporting if adoption is wide.
3.  **Dependency Management:**
    *   Regularly review and update dependencies using `poetry update` and Dependabot alerts.
4.  **CI/CD Maintenance:**
    *   Keep CI workflows up-to-date with new Python versions, tools, and testing needs.
5.  **Documentation Sustainability:**
    *   Ensure documentation remains current with all code changes and new features.

---

**Cross-Cutting Concerns & Best Practices (Actively Implementing):**

*   **Code Quality:** Ruff for linting/formatting, Mypy for static typing, Bandit for security.
*   **Testing:** Pytest for unit/integration tests, aiming for high coverage.
*   **Version Control:** Git with Conventional Commits, feature branches, PRs.
*   **Dependency Management:** Poetry for robust and reproducible environments.
*   **CLI Design:** Typer for an intuitive and well-documented CLI, Rich for enhanced UX.
*   **Documentation:** MkDocs (Material, mkdocstrings) for comprehensive and accessible docs.
*   **Automation:** GitHub Actions for CI/CD, Release Drafter for changelogs, Dependabot for updates.
*   **Pre-commit Hooks:** Local enforcement of code quality standards before commits.
*   **`src`-Layout:** Standard project structure for Python packages.
*   **Modularity:** Code organized into logical modules and sub-packages.
*   **Error Handling:** Graceful error reporting with clear, user-friendly messages.
