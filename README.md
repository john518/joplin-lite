# Joplin Lite

Joplin-Lite is a desktop application that duplicates a core subset of the official Joplin Desktop application but with a much smaller disk and memory footprint. The official app is built on the Electron platform, which presents a large disk footprint (500+ MB) and memory footprint (400+ MB). Joplin-Lite, on the other hand, is a `pywebview` app that uses native OS libraries for rendering the user interface and, as such, consumes significantly less computing resources.

## Main Features

- **Joplin Itegration:** Connects to the Joplin Data/API server for note access, management, and synchronization with remote storage.
- **3-Column Layout:** Mirrors the traditional Joplin Desktop interface. The first column displays a tree view of the user's notebooks, the second lists note titles for the selected folder, and the third renders the selected note.
- **Markdown & Rendered Views:** Provides access to all notes for editing markdown alongside a display toggle for rendered formats.

## Technical Stack

- `pywebview` wraps the UI and manages the underlying Joplin Data/API server.
- `Vue.js / Vite` powers the reactive user interface.
- The UI communicates with the local Joplin Data/API server through the python backend instead of directly, in order to bypass CORS restrictions in the front-end web view.

## Deferred / Out of Scope

- **Platform Support:** Initial development is focused on Linux and macOS. There are no plans to support Windows.
- **Packaging:** Joplin Lite is for developers familiar with working in a terminal environment and running from source code. There is no plan to make installers or provide other packaging for "one click" use.
- **Advanced Features:** Joplin todos, note tags, and WYSIWYG editing are excluded from the initial version to maintain a lightweight scope.
