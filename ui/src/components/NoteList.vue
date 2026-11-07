<template>
  <div class="pane">
    <div class="header-container">
      <h3>Notes</h3>
      <button class="new-note-btn" @click="createNote" title="New Note (Ctrl+N)">
        +
      </button>
    </div>

    <ul>
      <li v-for="note in state.notes" :key="note.id"
        @click="handleNoteClick(note.id)"
        :class="{ active: state.selectedNoteId === note.id}"
      >
        <span class="note-title">{{ note.title }}</span>
        <hr />
      </li>
    </ul>
  </div>
</template>

<script setup>
  import { onMounted, onUnmounted } from 'vue'
  import { useApplicationStore } from '../composables/useApplicationStore.js'
  const { state, selectNote } = useApplicationStore()

  const handleNoteClick = (id) => {
    // Update if the clicked notebook is not currently selected
    if (id !== state.selectedNoteId) {
      console.debug(`Selected note ${id}`)
      selectNote(id)
    }
}  // handleNoteClick


  const createNote = async () => {
    try {
      const response = await window.pywebview.api.create_note({
        title: 'Untitled Note',
        body: '',
        // If selectedNotebookId is 0 (All Notes), pass null or omit it
        parent_id: state.selectedNotebookId === 0 ? null : state.selectedNotebookId
      })

      if (response.success && response.data) {
        const newNote = response.data
        state.notes.unshift(newNote)
        selectNote(newNote.id)
        console.debug(`Created note ${newNote.id}`)
      }
    } catch (err) {
      console.error('Failed to create note:', err)
    }
  }

  // Keyboard shortcut listener for Ctrl+N / Cmd+N
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'n') {
      e.preventDefault()
      createNote()
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
  })
</script>

<style scoped>
.pane {
  padding: 16px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

h3 {
  margin-top: 0;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #858585;
}

.new-note-btn {
  background: transparent;
  border: 1px solid #444;
  color: #ccc;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.new-note-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: #6a9955;
}

ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

li {
  /* Add padding, hover states, and cursor pointer here */
  cursor: pointer;
  padding-left: 8px;
  padding-top: 8px;
  font-size: 11pt;
}

/* Active state with Joplin-style blue background */
li.active > span {
  background-color: #094771; /* Classic VS Code / Joplin active selection blue */
  color: #ffffff;
}

/* Ensure the list item constrains its children */
ul li {
  overflow: hidden;
}

.note-title {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  padding: 0;
  padding-left: 6px;
  padding-top: 8px;
}

hr {
  margin: 0;
  /*background-color: #333333;*/

}

</style>
