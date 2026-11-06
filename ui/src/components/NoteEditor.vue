<template>
  <div class="stub-pane">
    <h3>{{state.currentNote.title}}</h3>
    <div>{{ state.currentNote.body }}</div>
  </div>
</template>

<script setup>
  import { useApplicationStore } from '../composables/useApplicationStore.js'
  const { state } = useApplicationStore()
</script>

<style scoped>
.stub-pane {
  padding: 24px;
}
h3 {
  margin-top: 0;
  font-size: 14px;
  /*text-transform: uppercase;*/
  letter-spacing: 0.05em;
  color: #858585;
}
.placeholder-text {
  font-size: 13px;
  color: #6a9955;
}
</style>
