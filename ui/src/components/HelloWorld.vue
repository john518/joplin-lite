<script setup>
import { ref } from 'vue'
import pywebvueLogo from '../assets/logo.svg'

const count = ref(0)
const apiStatus = ref("")

async function checkApi() {
  try {
    apiStatus.value = 'Pinging...'
    const pong = await window.pywebview.api.ping()
    apiStatus.value = `${pong.status} at ${pong.timestamp}`
  } catch (error) {
    apiStatus.value = 'Error calling backend'
    console.error(error)
  }
}
</script>

<template>
  <div class="main">
    <h1>HelloWorld.vue</h1>

    <div>
      <button type="button" class="counter" @click="count++">
        Count is {{ count }}
      </button>
    </div>

    <div>
      <img :src="pywebvueLogo" alt="logo" width="64" height="64" />
    </div>

    <div>
      <button type="button" @click="checkApi">Ping</button>
      <span>API status: {{ apiStatus }}</span>
    </div>

  </div>
</template>

<style scoped>
    .main {
        padding-left: 2em;
    }
    button {
        margin: 1em 0;
    }
    span {
        margin-left: 1em;
    }
</style>
