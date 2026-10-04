<script setup>
import { computed } from 'vue'
import { Content, useData, withBase } from 'vitepress'

const { page, site } = useData()

// The root locale is French (`root`), English lives under `/en/`.
const currentLang = computed(() => (site.value.localeIndex === 'en' ? 'en' : 'fr'))

const labels = computed(() =>
  currentLang.value === 'fr'
    ? { cv: 'CV', courses: 'Cours' }
    : { cv: 'Resume', courses: 'Courses' }
)

// `withBase` prefixes the configured base URL so the switcher works no matter
// which path the site is deployed under.
const languages = [
  { key: 'fr', label: 'FR', link: withBase('/') },
  { key: 'en', label: 'EN', link: withBase('/en/') },
]

const links = computed(() => [
  { key: 'cv', label: labels.value.cv, link: withBase(currentLang.value === 'en' ? '/en/' : '/') },
  { key: 'courses', label: labels.value.courses, link: withBase(currentLang.value === 'en' ? '/en/courses' : '/fr/courses') },
])

</script>

<template>
  <header>
    <nav class="site-nav">
      <a
        v-for="link in links"
        :key="link.key"
        :href="link.link"
        class="nav-link"
      >
        {{ link.label }}
      </a>
    </nav>
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
      <a href="https://vitepress.dev">VitePress</a> -
      &copy; 2026 Ulysse DURAND -
      Design by <a href="https://lucaslaine.fr">Lucas Lainé</a>
    </p>
  </footer>
</template>

<style scoped>

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1em;
}

.site-nav,
.lang-switch {
    display: flex;
    gap: 0.5em;
    padding: 1em 0;
}

.site-nav {
    justify-content: flex-start;
}

.lang-switch {
    justify-content: flex-end;
}

.nav-link {
    padding: 0.3em 0.8em;
    border-radius: 4px;
    font-family: Montserrat, sans-serif;
    font-weight: 600;
    color: var(--link);
}

.nav-link:hover {
    background-color: var(--head-foot-color);
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

.nav-link::after {
    content: "";
}

.lang-link.active {
    background-color: var(--accent);
    color: white;
}

</style>