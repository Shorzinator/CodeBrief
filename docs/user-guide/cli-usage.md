# CLI Usage

ContextCraft provides several commands to help you generate project context.
You can always get help for the main application or a specific command
by using the `--help` flag.

```bash
contextcraft --help
contextcraft <command> --help
```

## `tree` Command

Generates a directory tree structure.

```bash
contextcraft tree [ROOT_DIR] [OPTIONS]
```

**Key Options:**
*   `ROOT_DIR`: The directory to generate the tree for (defaults to current directory).
*   `-o, --output FILE`: Save the tree to a specified file.
*   `-i, --ignore TEXT`: Directory or file names to ignore (can be used multiple times).

**Example:**
```bash
contextcraft tree src/ --output project_src_tree.txt --ignore __pycache__
```

## `flatten` Command

Concatenates files into a single text output.

```bash
contextcraft flatten [ROOT_DIR] [OPTIONS]
```

**Key Options:**
*   `ROOT_DIR`: The root directory to search for files (defaults to current directory).
*   `-o, --output FILE`: Save the flattened content to a specified file.
*   `--include TEXT`: File extensions, globs, or names to include (e.g., `*.py`, `.md`).
*   `--exclude TEXT`: File extensions, globs, or names to exclude (e.g., `*.log`).

**Example:**
```bash
contextcraft flatten . --include "*.py" --include "*.md" --exclude "tests/*" --output context_bundle.txt
```

*(More commands and details will be added as they are developed.)*
