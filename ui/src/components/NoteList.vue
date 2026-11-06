<template>
  <div class="pane">
    <h3>Notes</h3>

    <ul>
      <li v-for="note in state.notes" :key="note.id"
        @click="handleNoteClick(note.id)"
        :class="{ active: state.selectedNoteId === note.id}"
      >
        {{ note.title }} <hr />
      </li>
    </ul>
  </div>
</template>

<script setup>
  import { useApplicationStore } from '../composables/useApplicationStore.js'
  const { state, selectNote } = useApplicationStore()

  const handleNoteClick = (id) => {
    // Update if the clicked notebook is not currently selected
    if (id !== state.selectedNoteId) {
      console.debug(`Selected note ${id}`)
      // selectNote(id)
    }
  }  // handleNoteClick
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
  padding-top: 8px;
  font-size: 11pt;
}

/* Active state with Joplin-style blue background */
li.active {
  background-color: #094771; /* Classic VS Code / Joplin active selection blue */
  color: #ffffff;
}

</style>
