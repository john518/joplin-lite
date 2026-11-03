<template>
  <div class="pane">
    <h3>Notebooks</h3>
    <!-- <span>Selected notebook: {{ state.selectedNotebookId }}</span> -->

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
</template>

<script setup>
  import { useApplicationStore } from '../composables/useApplicationStore.js'
  const { state, selectNotebook } = useApplicationStore()

  const handleNotebookClick = (id) => {
    console.debug(`Selected notebook ${id}`)
    selectNotebook(id)
  }
</script>

<style scoped>
.pane {
  padding: 16px;
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
  /* Add padding, hover states, and cursor pointer here */
  cursor: pointer;
  padding: 6px 12px;
}

/* Active state with Joplin-style blue background */
li.active {
  background-color: #094771; /* Classic VS Code / Joplin active selection blue */
  color: #ffffff;
}

.icon {
  font-size: 14px;
}

</style>
