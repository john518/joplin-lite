<template>
  <div class="pane" v-if="state.currentNote">
    <div class="editor-header">
      <input
        type="text"
        v-model="state.currentNote.title"
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
        v-model="state.currentNote.body"
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

const { state } = useApplicationStore()
const activeTab = ref('write')

const renderedMarkdown = computed(() => {
  if (!state.currentNote?.body) return '<p class="placeholder-text">Nothing to preview...</p>'
  const rawHtml = marked.parse(state.currentNote.body)
  return DOMPurify.sanitize(rawHtml)
})

// Debounced save function that calls Python API
const saveNoteToBackend = debounce(async (note) => {
  try {
    await window.pywebview.api.update_note(note.id, note.title, note.body)
    console.debug(`Auto-saved note ${note.id}`)
  } catch (err) {
    console.error('Failed to auto-save note:', err)
  }
}, 800) // Waits 800ms after the last keystroke before saving

// Watch for any deep changes in the current note and trigger the debounce
watch(
  () => state.currentNote,
  (newNote) => {
    if (newNote) {
      saveNoteToBackend(newNote)
    }
  },
  { deep: true }
)
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
