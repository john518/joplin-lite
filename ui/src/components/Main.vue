<template>
  <div class="app-container">
    <!-- Column 1: Notebook Tree -->
    <aside class="col notebook-tree-col" :style="{ width: notebookTreeWidth + 'px' }">
      <NotebookTree />
    </aside>

    <!-- Resizer Divider 1 -->
    <div class="resizer" @mousedown="initResize(1, $event)"></div>

    <!-- Column 2: Note List -->
    <section class="col note-list-col" :style="{ width: noteListWidth + 'px' }">
      <NoteList />
    </section>

    <!-- Resizer Divider 2 -->
    <div class="resizer" @mousedown="initResize(2, $event)"></div>

    <!-- Column 3: Note Editor -->
    <main class="col note-editor-col">
      <NoteEditor />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NotebookTree from './NotebookTree.vue'
import NoteList from './NoteList.vue'
import NoteEditor from './NoteEditor.vue'

// Reactive widths for the first two columns
const notebookTreeWidth = ref(240)
const noteListWidth = ref(280)

const initResize = (colIndex, event) => {
  event.preventDefault() // Prevents text highlighting while dragging
  const startX = event.clientX
  const startWidth = colIndex === 1 ? notebookTreeWidth.value : noteListWidth.value

  const onMouseMove = (e) => {
    const delta = e.clientX - startX
    if (colIndex === 1) {
      notebookTreeWidth.value = Math.max(160, Math.min(450, startWidth + delta))
    } else if (colIndex === 2) {
      noteListWidth.value = Math.max(200, Math.min(600, startWidth + delta))
    }
  }

  const onMouseUp = () => {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #1e1e1e;
  color: #cccccc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.col {
  height: 100%;
  overflow-y: auto;
}

.notebook-tree-col {
  flex-shrink: 0;
  background-color: #252526;
  /*border-right: 1px solid #333333;*/
  background-color: var(--bg-column-notebooks);
  border-right: 1px solid var(--app-border);
}

.note-list-col {
  flex-shrink: 0;
  /*background-color: #2d2d2d;*/
  /*border-right: 1px solid #333333;*/
  background-color: var(--bg-column-notelist);
  border-right: 1px solid var(--app-border);
}

.note-editor-col {
  flex-grow: 1;
  /*background-color: #1e1e1e;*/
  background-color: var(--bg-column-editor);
  color: var(--app-text-main);
}

.resizer {
  width: 4px;
  cursor: col-resize;
  background-color: transparent;
  transition: background-color 0.2s;
  z-index: 10;
}

.resizer:hover {
  background-color: #007acc;
}
</style>
