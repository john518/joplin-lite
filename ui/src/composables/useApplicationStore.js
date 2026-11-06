/**
 * Application state management composable for Joplin Lite.
 *
 * Encapsulates the centralized reactive state, backend readiness tracking,
 * and asynchronous bridge calls for notebooks, notes, and recent note history
 * across the Vue component hierarchy.
 *
 * @returns {Object} The reactive application state and state-mutation methods.
 */

import { reactive, computed } from 'vue'

const state = reactive({
  notebooks: [],
  notes: [],
  currentNote: null,
  selectedNotebookId: null,
  selectedNoteId: null,
  noteHistory: []
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
        }

        // Set selected note from persistent store
        const noteRes = await window.pywebview.api.get_user_state_value('selectedNoteId')
        if (noteRes.success && noteRes.value !== null) {
          state.selectedNoteId = noteRes.value
        }

      }  // try
      catch (e) {
        console.warn("Failed to initialize data:", e)
      }  // catch
    }  // if (isReady)
  }  // setBackendReady

  // Fetches notebooks via the pywebview bridge
  const fetchNotebooks = async () => {
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
      console.warn("Failed to persist selectedNotebookId to storage:", e)
    }

    // Fetch notes based on whether "All" or a specific notebook is chosen
    console.debug(`Fetching notes for notebook(${notebookId})`)
    const notesObject = await window.pywebview.api.get_notes(state.selectedNotebookId)
    // console.dir(notesObject)
    state.notes = notesObject.items
  }

  const fetchNotesForNotebook = async (notebookId) => {
    try {
      let endpoint = '/notes'
      let params = { limit: 100, order_by: 'updated_time', order_dir: 'DESC' }

      // If a specific notebook is selected (not 'All' / 0), filter by parent_id
      if (notebookId !== 0) {
        // Depending on your backend API route design, you can pass a query filter
        // or a specific endpoint path like `/notebooks/${notebookId}/notes`
        params.parent_id = notebookId
      }

      const response = await window.pywebview.api.api_request(endpoint, 'GET', params)
      if (response.success) {
        state.notes = response.data.items || []
      }
    } catch (error) {
      console.error("Error fetching notes for notebook:", error)
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
    }

    // Fetch note content
    console.debug(`Fetching note(${noteId})`)
    const noteResponse = await window.pywebview.api.get_note(state.selectedNoteId)
    // console.dir(note)
    state.currentNote = noteResponse.data
  }

  return {
    state,
    setBackendReady,
    selectNotebook,
    selectNote,
  }
}
