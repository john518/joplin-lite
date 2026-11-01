# Joplin Lite Architecture

Joplin-Lite is a desktop application that implements the core functionality of the Joplin Desktop application in a much smaller memory footprint. The technical stack leverages the `pywebview` webview wrapper to provide a lightweight application with Python backend and html/css/js front end. The front end uses the Vue.js/Vite framework to implement the user interface as static html/css/js files. To access the Joplin note store, the Python back end launches the Joplin Data/API server as a background subprocess. HTTP requests from the html/css/js front end are relayed through the Python backend in order to avoid CORS restrictions in the webview infrastructure. Joplin Lite uses the `pywebview` JS-to-Python RPC Bridge, which allows binding Python objects directly to the javascript window object (pywebview.api.some_method()). The Python backend might also be used for other utility operations, e.g. synchronization with remote storage.

## Front End

The front end user interface is made up of custom Vue.js components:

- `App.vue` is the top-level component that includes logic for detecting when the backend server is ready.
- `Main.vue` creates and manages the 3 column UI with one child component in each column.
- `NotebookTree.vue` is the first column, showing a tree view of the user's notebooks.
- `NoteList.vue` is the middle column, showing a list of note titles for the selected notebook or "all". The component will provide limit ed sorting options. By default, notes are sorted by updated datetime in descending order.
- `NoteEditor.vue` is the last column, showing the current selected note (if any) for editing
- `useApplicationState.js` implements a Vue composable to serve as a centralized reactive state across all components, via the Vue `provide/inject` pattern. State data will include a boolean `backendReady` variable, the notebook list/tree, the selected notebook id, the current note list, the selected note if, and a list of the recently-visited note history.

## Back End

The backend will start the joplin data/api server and the webview with the frontend html file.

- `main.py` has the entry point for launching the app. It's `main()` function will start the joplin data/api server and the webview frontend. 
- `joplin-server.py` provides the actual management of and access to the joplin data/api server. Outside of this project, a new "joplin-lite" profile must be created and assigned an IP address outside the default Joplin range (41184-41194). The `joplin_server.py` has functions to read the profile settings file to obtain the port number and api token. The code also uses the `atexit` library to shut down the joplin data/api server.
- `api.py` implements the Javascript/Python bridge that enables frontend code to call functions in the backend. Its main function is to forward http requests from the frontend to the joplin data/api server and return the response to the frontend.
