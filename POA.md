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


**Phase 1: MVP Development (Status: IN PROGRESS ~ Target Completion: [Original estimate + any adjustments])**

1.  **Environment & Tooling Setup (Status: LARGELY DONE)**
    *   Poetry environment setup. (DONE)
    *   Editor/IDE configured for Ruff, Mypy. (DONE)
    *   Set up **pre-commit hooks** (Ruff, Mypy, Bandit, etc.) for local code quality enforcement. (DONE)

2.  **Core CLI Orchestrator (Status: DONE)**
    *   `src/contextcraft/main.py` implemented with Typer. (DONE)
    *   Handles command registration and basic app structure. (DONE)
    *   **(NEW/REFINED)** Implement `contextcraft --version` command to display the application's version (sourced from `pyproject.toml`).

3.  **Tool 1: Directory Tree Generator (`tree` command) (Status: IMPLEMENTED - TESTING PENDING)**
    *   Logic implemented in `src/contextcraft/tools/tree_generator.py`. (DONE)
    *   Handles `root_dir`, `--output`, and CLI `--ignore` options. (DONE)
    *   Uses `rich.tree.Tree` for console output, plain text for file. (DONE)
    *   Production-level docstrings and comments added. (DONE)
    *   **(REFINED TODO - IMMEDIATE FOCUS)** Write comprehensive unit and integration tests with `pytest` for `tree_generator.py`, including:
        *   Core tree generation logic.
        *   Output to console and file.
        *   Interaction with CLI `--ignore` options.
        *   **Crucially, integration with the `.llmignore` system** (verifying that patterns from a test `.llmignore` file are correctly applied).
        *   Edge cases (empty directories, permission errors if mockable, very deep trees).

4.  **Tool 2: Code Flattener (`flatten` command) (Status: IMPLEMENTED - TESTING PENDING)**
    *   Logic refactored into `src/contextcraft/tools/flattener.py`. (DONE)
    *   Integrated as a `flatten` command in `main.py` using Typer. (DONE)
    *   Implement options for `root_dir`, `output_file`, CLI `--include`, and CLI `--exclude` options. (DONE)
    *   Prepend flattened file content with a clear marker comment. (DONE)
    *   Handle `UnicodeDecodeError` for binary files gracefully. (DONE)
    *   Production-level docstrings and comments added. (DONE)
    *   **(REFINED TODO - IMMEDIATE FOCUS)** Write comprehensive unit and integration tests with `pytest` for `flattener.py`, including:
        *   Core file reading and concatenation logic.
        *   Output to console and file.
        *   Interaction with CLI `--include` and `--exclude` options.
        *   Binary file skipping.
        *   **Crucially, integration with the `.llmignore` system** (verifying that patterns from a test `.llmignore` file are correctly applied in conjunction with `--include`/`--exclude`).
        *   Edge cases (empty files, large files if performance is a concern).

5.  **Initial CI Setup (GitHub Actions) (Status: DONE)**
    *   Implemented workflows triggered on push/PR to `develop` and `main`. (DONE)
    *   Jobs for Ruff (linting/formatting), Mypy (type checking), Bandit (security), and Pytest (test execution placeholder). (DONE)

6.  **Basic Documentation (MkDocs) (Status: DONE)**
    *   Set up MkDocs with the Material theme. (DONE)
    *   Configured `mkdocstrings` for pulling API docs from code. (DONE)
    *   Created initial pages: Home, Installation, CLI Usage (for `tree` and `flatten`), and API reference structure. (DONE)

7.  **Internal Testing & Refinement (Status: ONGOING)**
    *   Continuously test implemented features on diverse local projects. (ONGOING)
    *   Refine CLI usability, output formatting, and error messages based on usage. (ONGOING)
    *   **(NEW/REFINED)** Clarify and implement the interaction between tool-specific `DEFAULT_EXCLUDED_ITEMS` (from `tree_generator.py` and `flattener.py`) and the `.llmignore` system.
        *   **Decision:** `DEFAULT_EXCLUDED_ITEMS` will only apply if *no* `.llmignore` file is found in the target `root_dir`. If an `.llmignore` is present, it (along with `CORE_SYSTEM_EXCLUSIONS` and CLI flags) becomes the sole source of ignore rules. This provides a clear model for users. *This may require minor code adjustments in the tools.*


---

**Phase 2: V1.0 Feature Development & Refinement (Status: IN PROGRESS [`.llmignore` core done] ~ Target Completion: [Original estimate + any adjustments])**

*Process for each feature: Design -> Implement -> Test (Unit & Integration) -> Document (MkDocs)*

1.  **`.llmignore` System (Status: LARGELY IMPLEMENTED - INTEGRATION TESTING PENDING)**
    *   Implement parsing of `.llmignore` file(s) using `pathspec` for `.gitignore`-style syntax. (DONE)
    *   Centralized ignore logic in `src/contextcraft/utils/ignore_handler.py`. (DONE)
    *   Integrate `.llmignore` logic into `tree` and `flatten` commands. (DONE - initial integration)
    *   Define and implement precedence: Core System Exclusions > `.llmignore` > CLI Ignores. (DONE)
    *   **(PENDING - Covered by Phase 1 Testing TODOs)** Verify full integration and precedence through comprehensive unit tests for `ignore_handler.py` and updated integration tests for `tree` and `flatten` commands that specifically cover `.llmignore` scenarios.
    *   **(NEW - Related to Phase 1, Item 7 Refinement)** Ensure tool-specific `DEFAULT_EXCLUDED_ITEMS` (from `tree_generator.py` and `flattener.py`) only apply if no `.llmignore` file is found in the target `root_dir`. Update tool logic and test this behavior.

2.  **Configuration File (Status: TODO - SUGGESTED NEXT FEATURE POST-TESTING)**
    *   Implement support for a project-level configuration file.
        *   **Preferred Location:** `pyproject.toml` under a dedicated `[tool.contextcraft]` section.
        *   **Alternative (if `pyproject.toml` becomes too crowded):** A dedicated `contextcraft.toml` or `.contextcraft.toml` file in the project root.
    *   Allow users to set default values for common options, such as:
        *   Default output filename for `bundle` or `flatten` (e.g., `llm_context.md`).
        *   Project-wide default include/exclude patterns (these would be additive to or provide a base for `.llmignore` - precedence needs careful consideration).
        *   Default tools to run for the `bundle` command.
    *   Ensure clear documentation on configuration file usage and precedence (CLI options generally override config file settings, which in turn might influence or be combined with `.llmignore` defaults).
    *   Write unit tests for configuration loading and application.

3.  **Tool 3: Git Context Provider (`git-info` command) (Status: TODO)**
    *   Implement functionality to extract relevant Git information using direct `git` CLI calls (via `subprocess`).
        *   Current branch name.
        *   `git status --short` (changed/untracked files).
        *   `git diff HEAD --name-status` (uncommitted changes to tracked files - names and status).
        *   Optionally, `git diff HEAD` for full diff content of uncommitted changes (can be large, make it configurable).
        *   `git log -n <count> --oneline` (recent commits, configurable count).
    *   Handle cases gracefully if not in a Git repository (e.g., clear message, no output for this section).
    *   Output format should be clean text, easily embeddable in the final Markdown bundle.
    *   Write unit tests (may involve mocking `subprocess` calls or testing against a temporary Git repository).

4.  **Tool 4: Dependency Lister (`deps` command) (Status: TODO)**
    *   Implement logic to identify and list project dependencies.
    *   Initial support for Python:
        *   `pyproject.toml` (Poetry `[tool.poetry.dependencies]` and `[tool.poetry.group.<group>.dependencies]`; PEP 621 `[project.dependencies]`).
        *   `requirements.txt` (and variants like `requirements-dev.txt` if specified).
    *   Initial support for Node.js: `package.json` (`dependencies`, `devDependencies`).
    *   Design for extensibility: Create a clear plugin-like or strategy pattern to easily add parsers for other languages/package managers in the future (e.g., `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `go.mod`, `Cargo.toml`).
    *   Output format should be a clean list, suitable for the Markdown bundle (e.g., language, dependency file, list of dependencies with versions).
    *   Write unit tests with example dependency files.

5.  **"Bundle" Command (`bundle` command) (Status: TODO - DEPENDS ON OTHER TOOLS)**
    *   The flagship command to aggregate context from multiple tools (`tree`, `flatten` [selected files/dirs], `deps`, `git-info`).
    *   Allow users to specify which context pieces to include via CLI options (e.g., `--no-tree`, `--no-deps`, `--flatten-path src/app --flatten-path src/utils`).
    *   Default behavior should be to include a "sensible" set of context pieces (e.g., tree, deps, git status, key source files if a heuristic can be developed or configured).
    *   Format the combined output as a single, well-structured **Markdown (.md) file**, with clear H2/H3 headings for each section (e.g., "Directory Tree", "Dependencies (Python)", "File: src/main.py").
    *   Utilize `Rich` for console progress, summary, or if printing parts of the bundle to the console.
    *   Write integration tests that invoke the bundle command and verify the structure and content of the output Markdown.

6.  **Clipboard Integration (Status: TODO)**
    *   Add a global option (e.g., `--to-clipboard` / `-c`) applicable to commands that produce significant text output (`flatten`, `bundle`, potentially `tree`, `deps`, `git-info`).
    *   Use a cross-platform library like `pyperclip` to copy the output to the system clipboard.
    *   Provide clear feedback to the user (e.g., "Output copied to clipboard.").
    *   Test on different OS if possible (or rely on `pyperclip`'s own testing).

7.  **Testing Enhancements (Status: ONGOING - Foundational tests in Phase 1 & for `.llmignore`)**
    *   **Target:** Achieve and maintain high unit test coverage (e.g., >90%) for all core logic. CI can report on this.
    *   **Integration Tests:** Expand integration tests for CLI commands, ensuring options interact correctly and outputs are as expected for various scenarios (especially for the `bundle` command).
    *   **(NEW CONSIDERATION)** Explore **snapshot testing** for the `tree` command's output and the `bundle` command's Markdown output. This involves saving an "expected output" file and comparing against it. `pytest-snapshot` is a good library for this. This makes it easy to detect unintended changes in complex textual output.
    *   Consider property-based testing with `hypothesis` for particularly complex parsing or logic functions (e.g., advanced pattern matching if we were to build it ourselves, or complex parts of the dependency parser).

8.  **Documentation Overhaul & Developer Experience (DX) (Status: TODO - Initial docs in Phase 1)**
    *   Write comprehensive documentation in MkDocs for all commands, options, the `.llmignore` syntax, configuration file usage, and the `bundle` command's capabilities.
    *   Create tutorials or example use cases demonstrating how to effectively use `ContextCraft` for different scenarios (e.g., debugging with an LLM, onboarding a new developer).
    *   Develop `CONTRIBUTING.md`: Detailed guidelines for setting up the development environment, running tests, coding style (referencing pre-commit setup), and the Pull Request process.
    *   Enforce **Conventional Commits** for all commit messages (already started).
    *   Set up **Release Drafter** GitHub Action for automated changelog generation based on Conventional Commits and PR labels (this makes releases much smoother).

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
