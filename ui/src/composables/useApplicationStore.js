/**
 * Application state management composable for Joplin Lite.
 *
 * Encapsulates the centralized reactive state, backend readiness tracking,
 * and asynchronous bridge calls for notebooks, notes, and recent note history
 * across the Vue component hierarchy.
 *
 * @returns {Object} The reactive application state and state-mutation methods.
 */

import { reactive, readonly } from 'vue'

const state = reactive({
  notebooks: [],
  notes: [],
  currentNote: null,
  selectedNotebookId: null,
  selectedNoteId: null,
  noteHistory: [],
  isSyncing: false,
})

export function useApplicationStore() {

  // Control backend readiness and automatically trigger data loading
  const setBackendReady = async (isReady) => {
    console.debug(`Enter setBackendReady(${isReady})`)
    if (isReady) {
      try {
         // Automatically load data once the backend is confirmed
        await fetchNotebooks()

        // Set selected notebook from persistent store
        const notebookRes = await window.pywebview.api.get_user_state_value('selectedNotebookId')
        if (notebookRes.success && notebookRes.value !== null) {
          state.selectedNotebookId = notebookRes.value
          fetchNotes(notebookRes.value)
        }

        // Set selected note from persistent store
        const noteRes = await window.pywebview.api.get_user_state_value('selectedNoteId')
        if (noteRes.success && noteRes.value !== null) {
          state.selectedNoteId = noteRes.value
          // console.debug(`In setBackendReady(), selectedNoteId ${noteRes.value}`)
          fetchNote(noteRes.value)
        }

      }  // try
      catch (e) {
        console.warn("Failed to initialize data:", e)
      }  // catch
    }  // if (isReady)
  }  // setBackendReady

  // Fetches notebooks via the pywebview bridge
  const fetchNotebooks = async () => {
    console.debug("Fetching notebooks")
    try {
      // Calls your Python backend function exposed via pywebview
      state.notebooks = await window.pywebview.api.get_notebooks()
    } catch (error) {
      console.error("Error fetching notebooks:", error)
    }
  }

  // Selects a notebook by ID, saves the preference locally, and fetches its notes.
  //   * @param {number|string} notebookId - The ID of the notebook, or 0 for "All Notes".
  const selectNotebook = async (notebookId) => {
    state.selectedNotebookId = notebookId
    state.selectedNoteId = null // Clear note selection when switching notebooks

    // Update persistent storage
    try {
      await window.pywebview.api.save_user_state_value('selectedNotebookId', notebookId)
    } catch (e) {
      console.error("Failed to persist selectedNotebookId to storage:", e)
    }

    fetchNotes(notebookId)
  }

  // Fetches note list from pywebview bridge
  const fetchNotes = async (notebookId) => {
    // Fetch notes for selected notebook
    try {
      console.debug(`Fetching notes for notebook(${notebookId})`)
      const notesObject = await window.pywebview.api.get_notes(state.selectedNotebookId)
      // console.dir(notesObject)
      state.notes = notesObject.items
    }
    catch (e) {
      console.error(`Failed to fetch notes for notebook ${notebookId}`, e)
    }
  }

  // Selects a note by ID, saves the preference locally, and fetches its contents.
  //   * @param {number|string} notebookId - The ID of the notebook, or 0 for "All Notes".
  const selectNote = async (noteId) => {
    state.selectedNoteId = noteId

    // Update persistent storage
    try {
      await window.pywebview.api.save_user_state_value('selectedNoteId', noteId)
    } catch (e) {
      console.warn("Failed to persist selectedNoteId to storage:", e)
      // Retrieve note title and body from Joplin
    }

    // Get the note title and body
    fetchNote(noteId)
  }

  // Fetches note contents from pywebview bridge
  const fetchNote = async(noteId) => {
    console.debug(`Fetching note(${noteId})`)
    const noteResponse = await window.pywebview.api.get_note(noteId)
    // console.dir(note)
    state.currentNote = noteResponse.data
  }

  // Synchronizes local joplin data/api server with remote store
  const triggerSync = async () => {
      if (state.isSyncing) return

      // 1. Call Python backend via pywebview API
      const res = await window.pywebview.api.trigger_sync()
      if (!res.success) {
        console.error('Failed to start sync:', res.error_data)
        return
      }

      state.isSyncing = true
      state.syncError = null

      // 2. Recursive polling function
      const checkStatus = async () => {
        try {
          const statusRes = await window.pywebview.api.get_sync_status()

          if (statusRes.success && !statusRes.data.is_syncing) {
            state.isSyncing = false

            if (statusRes.data.error) {
              state.syncError = statusRes.data.error
              console.error('Sync failed:', statusRes.data.error)
            } else {
              console.debug('Sync completed successfully')
              // TODO: Refresh your notebooks/notes lists here if necessary
              // e.g., await loadNotebooks()
            }
          } else {
            // Keep polling recursively every 1.5 seconds
            setTimeout(checkStatus, 1500)
          }
        } catch (err) {
          console.error('Error polling sync status:', err)
          state.isSyncing = false
        }
      }

      setTimeout(checkStatus, 1500)
    }

  return {
    state: readonly(state),
    setBackendReady,
    selectNotebook,
    selectNote,
    triggerSync,
  }
}
