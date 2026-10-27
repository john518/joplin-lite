# Project Guidelines & Agent Instructions (`AGENTS.md`)

This document outlines the architectural context, tech stack, and coding standards for developers and AI agents working on this project.

## Tech Stack

- **Core Language:** Python 3.10+
- **Desktop Framework:** `pywebview` (using native OS web-rendering libraries)
- **Frontend UI:** Vue.js / Vite (`ui/`)
- **Data Backend:** `pywebview js_api` argument (class)
- **Package Management & Execution:** `uv`
- **Testing Framework:** `pytest`

---

## Coding Standards & Conventions

### 1. File System Operations
- **Prefer `pathlib.Path`:** Use Python's built-in `pathlib.Path` instead of the legacy `os.path` library for all path manipulations, file resolution, directory checks, and reading/writing operations where practical.

### 2. Documentation
- **Mandatory Docstrings:** Every Python file, class, and function must include a clear, descriptive docstring explaining its purpose, parameters, and return types.

### 3. Top-Level Scripts (`uv`)
- **Inline Script Metadata:** Top-level executable scripts must include a `uv` inline script metadata block (PEP 723 format) at the very top of the file to manage dependencies explicitly.
  - *Example:*
    ```python
    # /// script
    # dependencies = [
    #     "requests",
    # ]
    # ///
    ```

---

## Testing Guidelines

- **Framework:** All unit and integration tests must use **`pytest`**.
- **Directory Structure:** Test files should reside in a dedicated `tests/` folder mirroring the source code module layout.
- **Running Tests:** Execute tests locally using:
  ```bash
  uv run pytest
  ```
