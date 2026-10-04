<script setup>
import { computed } from 'vue'
import { mdLinksToHtml } from '../theme/utils'
import Course from './Course.vue'
import infosByLang from 'virtual:infos'

const props = defineProps({
  lang: {
    type: String,
    default: 'fr',
  },
})

const labels = computed(() =>
  props.lang === 'fr'
    ? { courses: 'Cours' }
    : { courses: 'Courses' }
)

// `virtual:infos` is provided by the `cv-infos` Vite plugin in
// `docs/.vitepress/config.mts`; the `*_fr` resolution already happened in Python.
const infos = computed(() => infosByLang[props.lang] || {})

// Each group is a degree (e.g. L3, M1 ENS) with its own description, location
// and year, plus the list of courses it contains.
const groups = computed(() =>
  Object.entries(infos.value.courses || {})
    .sort(([, a], [, b]) => {
      const yearA = a.year || ''
      const yearB = b.year || ''
      // newest first
      return yearB.localeCompare(yearA, undefined, { numeric: true })
    })
    .map(([key, group]) => ({
      key,
      heading: group.description || '',
      location: group.location || '',
      year: group.year || '',
      courses: (group.courses || []).map((course) => ({
        name: course.name,
        description: course.description || '',
        teachers: course.teachers || [],
        links: course.links || {},
      })),
    }))
)
</script>

<template>
  <h1>{{ labels.courses }}</h1>

  <section v-for="group in groups" :key="group.key" class="group">
    <div class="group-header">
      <h2 class="group-title" v-html="mdLinksToHtml(group.heading)"></h2>
      <span class="group-meta">{{ group.location }}<template v-if="group.year"> · {{ group.year }}</template></span>
    </div>

    <Course
      v-for="course in group.courses"
      :key="course.name"
      :name="course.name"
      :description="course.description"
      :teachers="course.teachers"
      :links="Object.entries(course.links).map(([label, url]) => ({ label, url }))"
    />
  </section>
</template>

<style scoped>
.group {
    margin-bottom: 2em;
}

.group-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1em;
    margin: 0 32px;
    padding: 0 8px;
    border-bottom: 1px solid var(--vp-c-divider);
}

.group-title {
    font-size: 1.2rem;
    margin: 0.5em 0;
}

.group-meta {
    text-align: right;
    min-width: 5em;
    font-family: sans-serif;
    color: var(--vp-c-text-2);
}
</style>
