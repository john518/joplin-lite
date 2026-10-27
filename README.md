# Joplin Lite

A lightweight, high-performance desktop application built with Python (`pywebview`), a native local backend, and a Vue/Vite reactive UI (`ui/`).

## Overview

[Provide a brief description of what this custom desktop utility does.]

## Core Features

- **Modern Desktop Shell:** Wrapped via `pywebview` to leverage native OS rendering engines with minimal resource overhead.
- **Reactive UI:** Built using Vue.js and Vite inside the `ui/` directory.
- **Local Data Integration:** Communicates with local application backends or API layers.

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)
- [Node.js & npm](https://nodejs.org/) (Frontend asset management)

### Running the App

Use the provided build and execution script to compile the frontend assets and launch the application:

```bash
./scripts/build_run.sh

Development

    Backend: Python logic lives in joplin-lite/

    Frontend: Vue/Vite source code lives in ui/

    Testing: Run tests using uv run pytest
