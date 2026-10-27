<template>
  <div v-if="!isReady" class="splash-screen">
    <div class="spinner-container">
      <p>Starting {{ project_name }}...</p>
    </div>
  </div>
  <HelloWorld v-else />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HelloWorld from './components/HelloWorld.vue'

const project_name = ref("{{ cookiecutter.project_name }}")
const isReady = ref(false)

onMounted(async () => {
  // Wait for Python-Javascript bridge to be initialized and ready
  const startTime = Date.now()
  const timeoutMs = 3000

  while (Date.now() - startTime < timeoutMs) {
    if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.ping === 'function') {
      try {
        const response = await window.pywebview.api.ping()
        if (response && response.status === 'ok') {
          // await new Promise(resolve => setTimeout(resolve, 1000))  // for debug only

          isReady.value = true
          return
        }
      } catch (e) {
        // IPC pipe not fully warm yet, retry on next loop
      }
    }
    await new Promise(resolve => setTimeout(resolve, 50))
  }

  console.error("Failed to connect to Python backend within timeout.")
})
</script>

<style scoped>
.splash-screen {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fafc;
  color: #475569;
  font-family: inherit;
  font-size: 1.1rem;
}
</style>
