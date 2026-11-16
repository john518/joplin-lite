<template>
  <div class="pane">
    <h3>Notebooks</h3>
    <!-- <span>Selected notebook: {{ state.selectedNotebookId }}</span>[cite: 1] -->

    <div class="notebook-list-container">
      <ul>
        <li
          :class="{ active: state.selectedNotebookId === 'all' }"
          @click="handleNotebookClick('all')"
        >
          <span class="icon">📁</span> All Notes
        </li>
        <li v-for="nb in state.notebooks" :key="nb.id"
          @click="handleNotebookClick(nb.id)"
          :class="{ active: state.selectedNotebookId === nb.id }"
        >
          <span class="icon">📘</span> {{ nb.title }}
        </li>
      </ul>
    </div>

    <!-- Bottom Pane Footer with Sync Button -->
    <div class="pane-footer">
      <button
        class="sync-btn"
        :disabled="isSyncing"
        @click="triggerSync"
      >
        <span :class="{ 'spin': isSyncing }" class="icon">🔄</span>
        {{ isSyncing ? 'Synchronizing...' : 'Sync with Remote' }}
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useApplicationStore } from '../composables/useApplicationStore.js'
  const { state, selectNotebook, triggerSync } = useApplicationStore()

  const isSyncing = ref(false)

  const handleNotebookClick = (id) => {
    if (id !== state.selectedNotebookId && !isSyncing.value) {
      console.debug(`Selected notebook ${id}`)
      selectNotebook(id)
    }
  }
</script>

<style scoped>
.pane {
  padding: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-sizing: border-box;
}

.notebook-list-container {
  flex-grow: 1;
  overflow-y: auto;
}

h3 {
  margin-top: 0;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #858585;
}

ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

li {
  cursor: pointer;
  padding: 6px 12px;
}

li.active {
  background-color: #094771; /* Classic VS Code / Joplin active selection blue[cite: 1] */
  color: #ffffff;
}

.icon {
  font-size: 14px;
}

.pane-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #333;
}

.sync-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: #252526;
  color: #cccccc;
  border: 1px solid #3c3c3c;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.sync-btn:hover:not(:disabled) {
  background-color: #2a2d2e;
  color: #ffffff;
  border-color: #007acc;
}

.sync-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spin {
  display: inline-block;
  animation: spin 1s linear infinite;
}
</style>
