<script setup>
import { computed } from 'vue'
import { Content, useData, withBase } from 'vitepress'

const { page, site } = useData()

// The root locale is French (`root`), English lives under `/en/`.
const currentLang = computed(() => (site.value.localeIndex === 'en' ? 'en' : 'fr'))

// `withBase` prefixes the configured base URL so the switcher works no matter
// which path the site is deployed under.
const languages = [
  { key: 'fr', label: 'FR', link: withBase('/') },
  { key: 'en', label: 'EN', link: withBase('/en/') },
]
</script>

<template>
  <header>
    <nav class="lang-switch">
      <a
        v-for="language in languages"
        :key="language.key"
        :href="language.link"
        class="lang-link"
        :class="{ active: currentLang === language.key }"
      >
        {{ language.label }}
      </a>
    </nav>
  </header>

  <main class="markdown-body">
    <Content />
  </main>

  <footer>
    <p>
      &copy; 2026 Ulysse DURAND -
      Design by <a href="https://lucaslaine.fr">Lucas Lainé</a>
    </p>
  </footer>
</template>

<style scoped>

.lang-switch {
    display: flex;
    justify-content: flex-end;
    gap: 0.5em;
    padding: 1em 0;
}

.lang-link {
    padding: 0.3em 0.8em;
    border-radius: 4px;
    background-color: var(--head-foot-color);
    font-family: Montserrat, sans-serif;
    font-weight: 600;
    color: var(--link);
}

.lang-link::after {
    content: "";
}

.lang-link.active {
    background-color: var(--accent);
    color: white;
}

</style>