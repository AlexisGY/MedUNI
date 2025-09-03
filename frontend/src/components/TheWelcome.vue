<script setup>
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div class="welcome-item"><DocumentationIcon />
    <h3>Documentation</h3>
    Vue’s <a href="https://vuejs.org/" target="_blank" rel="noopener">official documentation</a> provides the info to get started.
  </div>
  <div class="welcome-item"><ToolingIcon />
    <h3>Tooling</h3>
    Bundled with <a href="https://vite.dev/guide/features.html" target="_blank" rel="noopener">Vite</a>. See <a href="javascript:void(0)" @click="openReadmeInEditor"><code>README.md</code></a>.
  </div>
  <div class="welcome-item"><EcosystemIcon />
    <h3>Ecosystem</h3>
    Official libs: Pinia, Router, Test Utils, DevTools, Awesome Vue.
  </div>
  <div class="welcome-item"><CommunityIcon />
    <h3>Community</h3>
    Discord, StackOverflow, Bluesky/X for news.
  </div>
  <div class="welcome-item"><SupportIcon />
    <h3>Support Vue</h3>
    Consider <a href="https://vuejs.org/sponsor/" target="_blank" rel="noopener">sponsoring</a> the project.
  </div>
</template>
