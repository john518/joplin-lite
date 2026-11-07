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

  return {
    state,
    setBackendReady,
    selectNotebook,
    selectNote,
  }
}
