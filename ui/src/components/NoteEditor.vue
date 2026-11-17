<template>
  <div class="pane" v-if="editableNote">
    <!-- Sync Lock Notification Banner -->
    <div v-if="state.isSyncing" class="sync-lock-banner">
      <span>🔄 Synchronization in progress... Editing temporarily locked.</span>
    </div>

    <div class="editor-header">
      <input
        type="text"
        v-model="editableNote.title"
        @input="handleTitleInput"
        :disabled="state.isSyncing"
        class="title-input"
        placeholder="Note Title..."
      />
      <div class="tabs">
        <button
          tabindex="-1"
          :class="{ active: activeTab === 'write' }"
          @click="activeTab = 'write'"
        >
          Write
        </button>
        <button
          tabindex="-1"
          :class="{ active: activeTab === 'preview' }"
          @click="activeTab = 'preview'"
        >
          Preview
        </button>
      </div>
    </div>

    <div class="editor-content">
      <textarea
        v-show="activeTab === 'write'"
        v-model="editableNote.body"
        @input="handleInput"
        :disabled="state.isSyncing"
        class="markdown-textarea"
        placeholder="Write markdown here..."
      ></textarea>

      <div
        v-show="activeTab === 'preview'"
        class="markdown-preview"
        v-html="renderedMarkdown"
      ></div>
    </div>
  </div>
  <div class="pane empty-pane" v-else>
    <p class="placeholder-text">Select a note or create a new one to start editing.</p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { debounce } from 'lodash-es'
import { marked } from 'marked'
import DOMPurify from 'isomorphic-dompurify'
import { useApplicationStore } from '../composables/useApplicationStore.js'

const { state, updateNoteTitle } = useApplicationStore()
const activeTab = ref('write')

// Local mutable copy of the note for v-model binding
const editableNote = ref(null)

const renderedMarkdown = computed(() => {
  if (!editableNote.value?.body) return '<p class="placeholder-text">Nothing to preview...</p>'
  const rawHtml = marked.parse(editableNote.value.body)
  return DOMPurify.sanitize(rawHtml)
})

// Debounced save function calling Python API
const saveNoteToBackend = debounce(async (note) => {
  if (state.isSyncing) return

  try {
    await window.pywebview.api.update_note(note.id, note.title, note.body)
    console.debug(`Auto-saved note ${note.id}`)
  } catch (err) {
    console.error('Failed to auto-save note:', err)
  }
}, 800)

// Watch store's currentNote to handle note switching
watch(
  () => state.currentNote,
  (newNote) => {
    if (!newNote) {
      editableNote.value = null
      saveNoteToBackend.cancel()
      return
    }

    // If a different note was selected from the sidebar/list
    if (newNote.id !== editableNote.value?.id) {
      saveNoteToBackend.cancel() // Cancel pending saves for the old note
      editableNote.value = { ...newNote } // Clone into local state
    }
  },
  { immediate: true }
)
// Triggered by keystrokes on the local copy (body)
// Also called by handleTitleInput
const handleInput = () => {
  if (editableNote.value && !state.isSyncing) {
    saveNoteToBackend(editableNote.value)
  }
}

// Triggered by keystrokes on the title input
const handleTitleInput = (e) => {
  if (!editableNote.value)
    return

  const newTitle = e.target.value

  // 1. Instantly update the note title in the store array so NoteList.vue updates live
  updateNoteTitle(editableNote.value.id, newTitle)

  // 2. Call handleInput to schedule debounced save to backend
  handleInput()
}
</script>

<style scoped>
.pane {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px;
  box-sizing: border-box;
}

.empty-pane {
  justify-content: center;
  align-items: center;
}

.sync-lock-banner {
  background-color: #264f78;
  color: #ffffff;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 16px;
}

.title-input {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  padding: 6px 10px;
  border: 1px solid #333;
  border-radius: 4px;
  background: transparent;
  color: inherit;
}

.title-input:disabled,
.markdown-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tabs {
  display: flex;
  gap: 4px;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px;
  border-radius: 4px;
}

.tabs button {
  background: transparent;
  border: none;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  color: #858585;
  border-radius: 3px;
}

.tabs button.active {
  background: rgba(255, 255, 255, 0.1);
  color: inherit;
  font-weight: 500;
}

.editor-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.markdown-textarea {
  flex: 1;
  width: 100%;
  resize: none;
  padding: 12px;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  background: transparent;
  color: inherit;
  border: 1px solid #333;
  border-radius: 4px;
  box-sizing: border-box;
}

.markdown-textarea:focus {
  outline: none;
  border-color: #6a9955;
}

.markdown-preview {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  border: 1px solid #333;
  border-radius: 4px;
  line-height: 1.6;
}

.placeholder-text {
  font-size: 13px;
  color: #6a9955;
}
</style>
