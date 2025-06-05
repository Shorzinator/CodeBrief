
# `ContextCraft`

**Project Vision:**
To provide developers with a simple, extensible, and portable Python CLI toolkit that can be easily integrated into any project to generate comprehensive, structured context for Large Language Models, facilitating debugging, code understanding, and AI-assisted development.

**Core Philosophy:**
*   Developer-Centric, Modularity & Extensibility, Simplicity & Usability, Portability (via clone/PyPI), High Quality (code, tests, docs).

---

**Phase 0: Foundation & Planning (1-2 weeks)**

1.  **Detailed Requirements & Scope Definition:**
    *   **MVP (Minimum Viable Product):**
        *   Directory Tree Generator (with ignore patterns, depth control).
        *   Code Flattener (with ignore patterns, include patterns, file path comments).
        *   Basic CLI Orchestrator (using **Typer**).
        *   Basic `README.md` (using **MkDocs Material** structure from the start).
        *   **Poetry** for project/dependency management.
        *   Initial CI with **Ruff** (linting, formatting, import sorting) and **pytest**.
    *   **V1.0 Scope (Post-MVP):**
        *   Dependency Lister (Python, Node.js initially).
        *   Git Context Provider.
        *   `.llmignore` file implementation.
        *   Configuration file (`llmhelper.toml` or similar, parsed by Poetry/manually).
        *   "Bundle" command to aggregate multiple outputs, formatted with **Rich**.
        *   Clipboard integration (e.g., `pyperclip`).
        *   **Mypy (strict)** type checking in CI.
        *   **Coverage.py** reporting.
        *   **Bandit** security scanning in CI.
        *   **Release Drafter** setup with **Conventional Commits** practice.
        *   Full documentation using **MkDocs Material + mkdocstrings**.
    *   **Future Scope (Ideas for later):**
        *   Log/Output Snippet Grabber.
        *   Environment Variable Lister (with security filtering).
        *   File Content Snippet Extractor (potentially using `tree-sitter` for intelligence).
        *   SBOM generation (`Syft`) & vulnerability scanning (`Grype`) for PyPI releases.
        *   Support for more languages/dependency systems.
        *   `structlog` for advanced logging.
        *   Sentry for error tracking (if widely adopted).
        *   `hypothesis` for property-based testing.

2.  **Technology Stack Selection (Key Choices):**
    *   **Primary Language:** **Python 3.9+** (select a specific recent version like 3.11 or 3.12).
    *   **Project & Dependency Management:** **Poetry**.
    *   **CLI Framework:** **Typer**.
    *   **CLI Output Enhancement:** **Rich**.
    *   **Linting/Formatting/Import Sorting:** **Ruff**.
    *   **Type Checking:** **Mypy** (configured for strictness).
    *   **Security Linting:** **Bandit**.
    *   **Testing Framework:** **pytest** (with `pytest-cov` for coverage).
    *   **Version Control:** **Git** (hosted on GitHub).
    *   **CI/CD:** **GitHub Actions**.
    *   **Documentation:** **MkDocs** with **Material theme** and **mkdocstrings**.
    *   **Changelog Automation:** **Release Drafter** (requires Conventional Commits).

3.  **Project Structure & Architecture:**
    *   Set up project using `poetry new contextcraft`.
    *   Directory structure: `contextcraft/` (library code), `tests/`, `docs/`, `scripts/` (if any standalone helper scripts).
    *   Define CLI commands and options with Typer.
    *   Plan how modules will interact.
    *   Configuration strategy: `.llmignore`, project-level `llmhelper.toml` (or section in `pyproject.toml`).

4.  **Setup GitHub Repository:**
    *   Create repository.
    *   Initialize with Poetry (`pyproject.toml`).
    *   Add `LICENSE` (MIT or Apache 2.0), basic `README.md`.
    *   GitHub standard `.gitignore` for Python.
    *   Set up branch protection for `main` (require PRs, status checks).
    *   Create `develop` branch.
    *   Enable **Dependabot** for security and version updates.

---

**Phase 1: MVP Development (3-5 weeks)**

1.  **Environment Setup:**
    *   Install Poetry.
    *   `poetry install` to set up dev environment.
    *   Configure editor/IDE for Ruff, Mypy.

2.  **Core CLI Orchestrator (Typer):**
    *   Implement main CLI app with Typer.
    *   Stub out commands for tree generation and code flattening.

3.  **Tool 1: Directory Tree Generator:**
    *   Implement logic.
    *   Add options for depth control.
    *   Integrate basic ignore patterns (can be hardcoded or simple list initially).
    *   Use **Rich** for pleasant tree output.
    *   Write unit tests with `pytest`.

4.  **Tool 2: Code Flattener:**
    *   Implement logic.
    *   Add file path comments.
    *   Integrate basic ignore/include patterns.
    *   Write unit tests with `pytest`.

5.  **Initial CI Setup (GitHub Actions):**
    *   Workflow for **Ruff** (check & format), **pytest** on every push/PR to `develop` and `main`.
    *   Workflow for **Mypy**.

6.  **Basic Documentation (MkDocs):**
    *   Set up MkDocs with Material theme.
    *   Create initial pages: Installation, Basic Usage for MVP features.

7.  **Internal "Release" & Testing:**
    *   Test MVP thoroughly on your own projects.
    *   Refine CLI, output, and docs.

---

**Phase 2: V1.0 Feature Development & Refinement (5-10 weeks)**

*Iterate: Design -> Implement (with Typer/Rich) -> Test (pytest, mypy) -> Document (MkDocs + mkdocstrings)*

1.  **`.llmignore` System:**
    *   Implement robust parsing.
    *   Integrate into relevant tools.

2.  **Configuration File:**
    *   Decide format (e.g., `[tool.contextcraft]` in `pyproject.toml` or separate `llmhelper.toml`).
    *   Implement parsing.

3.  **Tool 3: Dependency Lister:**
    *   Implement parsers for Python (`pyproject.toml`, `requirements.txt`), Node.js (`package.json`).

4.  **Tool 4: Git Context Provider:**
    *   Use `subprocess`. Parse output. Graceful error handling.

5.  **"Bundle" Command:**
    *   Design aggregation logic. Use **Rich** for well-formatted bundled output (e.g., Markdown rendering within Rich).

6.  **Clipboard Integration:**
    *   Add `--to-clipboard` option using `pyperclip`.

7.  **Robust Error Handling & User Feedback:**
    *   Use Typer's error handling, provide clear messages.

8.  **Testing Enhancements:**
    *   Aim for high test coverage (`pytest-cov`), report to CI.
    *   Integrate **Bandit** into CI for security checks.

9.  **Documentation Overhaul (MkDocs + mkdocstrings):**
    *   Detailed `README.md` (can be `index.md` in MkDocs).
    *   Full usage guide for each command, `.llmignore`, config.
    *   Use `mkdocstrings` to pull API docs from code.
    *   `CONTRIBUTING.md`: Set up dev env (Poetry), run tests, coding style (Conventional Commits, Ruff).
    *   Set up **Release Drafter** GitHub Action; start writing commit messages using **Conventional Commits**.

---

**Phase 3: Release & Distribution (Ongoing with V1.0)**

1.  **Versioning Strategy:**
    *   Semantic Versioning. Start with `v0.1.0` for a stable MVP, `v1.0.0` for full-featured release.
    *   Use `poetry version <semver>` to update `pyproject.toml`.
    *   Git tags for releases.

2.  **Distribution Method:**
    *   **Primary (V1.0+):** Publish to **PyPI** as a wheel.
        *   Poetry handles `poetry build` and `poetry publish`.
        *   CI: Add SBOM generation (`Syft`) and vulnerability scanning (`Grype`) *before* publishing.
    *   **Secondary:** Cloning the GitHub repository remains an option for developers.

3.  **Community & Feedback:**
    *   GitHub Issues for bugs/features.
    *   Encourage PRs (with CLA assistant if contributions grow).

---

**Phase 4: Maintenance & Future Iteration (Ongoing)**

1.  **Bug Fixes & Enhancements:**
    *   Address issues. Implement "Future Scope" items.
    *   Refactor as needed.

2.  **Dependency Management with Poetry & Dependabot:**
    *   `poetry update` regularly. Review Dependabot PRs.

3.  **Keep CI/CD Healthy:**
    *   Maintain tests, update workflows for new Python versions/tools.

4.  **Documentation Updates:**
    *   Keep docs in sync.

---

**Best Practices Woven In (Recap of Enhancements):**

*   **Modern Python Tooling:** Poetry, Typer, Rich, Ruff, Mypy.
*   **Comprehensive Testing:** pytest, coverage, bandit, (future: hypothesis).
*   **Robust CI/CD:** GitHub Actions with linting, testing, type checking, security scans.
*   **Professional Documentation:** MkDocs Material, mkdocstrings.
*   **Automated Releases/Changelogs:** Conventional Commits, Release Drafter.
*   **Security Awareness:** Bandit, Dependabot, SBOM/Grype for releases.
*   **Developer Experience:** Clear CLI, excellent docs, easy contribution.

