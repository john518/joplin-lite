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
  backendReady: false,
  notebooks: [],
  notes: [],
  selectedNotebookId: null,
  selectedNoteId: null,
  noteHistory: []
})

export function useApplicationStore() {

  // 1. Control backend readiness and automatically trigger data loading
  const setBackendReady = async (isReady) => {
    console.debug("Enter setBackendReady()")
    state.backendReady = isReady
    if (isReady) {
      await fetchNotebooks() // Automatically load data the moment the backend is confirmed
    }
  }

  // 2. Define the action to fetch notebooks via the pywebview bridge
  const fetchNotebooks = async () => {
    try {
      // Calls your Python backend function exposed via pywebview
      state.notebooks = await window.pywebview.api.get_notebooks()
    } catch (error) {
      console.error("Error fetching notebooks:", error)
    }
  }
  return {
    state,
    setBackendReady,
    fetchNotebooks,
  }
}
