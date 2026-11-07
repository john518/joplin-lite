# Joplin Lite

<img src="./scripts/logo/joplin-lite-us.svg" height="64" width="64">

Joplin-Lite is a desktop application that duplicates a core subset of the official Joplin Desktop application but with a much smaller disk and memory footprint. The official app is built on the Electron platform, which presents a large disk footprint (500+ MB) and memory footprint (400+ MB). Joplin-Lite, on the other hand, is a `pywebview` app that uses native OS libraries for rendering the user interface and, as such, consumes significantly less computing resources.

## Main Features

- **Joplin Itegration:** Connects to the Joplin Data/API server for note access, management, and synchronization with remote storage.
- **3-Column Layout:** Mirrors the traditional Joplin Desktop interface. The first column displays a tree view of the user's notebooks, the second lists note titles for the selected folder, and the third renders the selected note.
- **Markdown & Rendered Views:** Provides access to all notes for editing markdown alongside a display toggle for rendered formats.

## Technical Stack

- `pywebview` wraps the UI and manages the underlying Joplin Data/API server.
- `Vue.js / Vite` powers the reactive user interface.
- The UI communicates with the local Joplin Data/API server through the python backend instead of directly, in order to bypass CORS restrictions in the front-end web view.

## Prequisites

- [uv](https://docs.astral.sh/uv/)
- [node/npm](https://nodejs.org/)
- [Joplin Terminal Application](https://joplinapp.org/help/apps/terminal/) which installs the Joplin Data/Api backend

## Joplin Profile Setup & Synchronization

Before running the Joplin Lite application, first install the Joplin Terminal Application. 

The Joplin Lite application connects to Joplin through the same backend as the Joplin Desktop and Terminal applications. It is called the Joplin Data/API server. So to use Joplin Lite, you must first install Joplin.

- You do NOT need to install the full Joplin Desktop application, which is built on the Electron platform and has a heavy memory and storage footprint.
- You can instead install the much-smaller terminal application. See the link in the [Prerequistes] section.

After installing the Joplin Terminal app, create an initialize a new "joplin profile" for connecting to Joplin Lite. This is needed to avoid collision with other Joplin applications. The steps for installing via the terminal application are as follows.

### Initialize a New Joplin Profile

1\. **Launch the interactive CLI wizard** to generate and populate the profile's SQLite schema:

   ```bash
   joplin --profile ~/.config/joplin-lite
   ```

Note: Don't instead create the profile using server commands directly. The Terminal App is needed in order to properly initialize the profile `database.sqlite` file.

2\. Configure sync target & credentials using the terminal UI prompt:

If you are using a remote server for synchronization, configure it from the terminal app. Check the Joplin docs for details. As an example, use these commands to configure synchronization with a self-hosted Joplin Cloud server:

```bash
    :config sync.target 9
    :config sync.9.path http://<SERVER_IP>:<PORT>
    :config sync.9.username <USERNAME>
    :config sync.9.password <API_TOKEN_OR_PASSWORD>
```

3\. Execute initial sync inside the CLI (:sync) to fetch remote keys and verify connection.

4\. Exit the CLI (:exit).

5\. Edit the profile settings file to change the port number.

To avoid conflict with the pubic Joplin desktop and terminal apps, add a new field to the settings file at `$HOME/.config/joplin-lite/settings.json` to change the port number from the default (41184) to 41183. Add this element to the file, just before the "api.token" field:

```json
"api.port": 41183,
```

Note: you can use any port number **outside** the range used by other Joplin apps (41184 to 41185).

6\. Verify connection using `test-joplin-connection.py` script.

- In one terminal, start the Joplin Data/Api server:

```bash
joplin --profile ~/.config/joplin-lite server start
```

- In a second terminal, run the test script:

```bash
uv run scripts/test-joplin-connection.py
```

If things are configured correctly, you should see output that includes the message `SUCCESS: Successfully connected to Joplin server!`. Here is a typical example:

```bash
% uv run scripts/test-joplin-connection.py

Connecting to Joplin API at http://localhost:41183...
Server response (data):
{'items': [{'id': 'ea7b94219bd5433899c6b5c95a7b52e5', 'parent_id': '', 'title': 'Welcome!', 'deleted_time': 0}, {'id': '3e552151e6d44e60867926a9abd2a579', 'parent_id': '', 'title': 'EvernoteWebClipper', 'deleted_time': 0}, {'id': 'd3ce9d2f6c15401989bd827a2dc6ee97', 'parent_id': '', 'title': 'Main', 'deleted_time': 0}], 'has_more': False}

SUCCESS: Successfully connected to Joplin server!
Found 3 total folder(s) in database.

Top-level Notebooks:
----------------------------------------
  - Welcome! (ID: ea7b94219bd5433899c6b5c95a7b52e5)
  - EvernoteWebClipper (ID: 3e552151e6d44e60867926a9abd2a579)
  - Main (ID: d3ce9d2f6c15401989bd827a2dc6ee97)
```

## Joplin Lite setup

To run Joplin Lite, from the repository directory:

```bash
cd ui && npm install
./scripts/build_run.sh
```

This will build the front end Vue3 scripts and launch the `pywebview` application. You don't need to rebuild the Vue3 code each time, so after the first time, you can instead just run the last line of the `build_run.sh` script:

```bash
PYTHONPATH=. PYTHONUNBUFFERED=1 uv run joplin_lite/joplin-lite.py
```

## Deferred / Out of Scope

- **Platform Support:** Initial development is focused on Linux and macOS. There are no plans to support Windows.
- **Packaging:** Joplin Lite is for developers familiar with working in a terminal environment and running from source code. There is no plan to make installers or provide other packaging for "one click" use.
- **Advanced Features:** Joplin todos, note tags, and WYSIWYG editing are excluded from the initial version to maintain a lightweight scope.
