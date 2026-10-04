<script setup>
import { computed } from 'vue'
import { transformLinks } from '../theme/utils'
import infosByLang from 'virtual:infos'

const props = defineProps({
  lang: {
    type: String,
    default: 'fr',
  },
})

const labels = computed(() =>
  props.lang === 'fr'
    ? {
        contact: 'Contact',
        education: 'Formation',
        experience: 'Expériences',
        projects: 'Projets',
      }
    : {
        contact: 'Contact',
        education: 'Education',
        experience: 'Experience',
        projects: 'Projects',
      }
)

// `virtual:infos` is provided by the `cv-infos` Vite plugin in
// `docs/.vitepress/config.mts`; the `*_fr` resolution already happened in Python.
const infos = computed(() => infosByLang[props.lang] || {})

const education = computed(() =>
  (infos.value.sections.education || []).map((e) => ({
    name: `${e.area}${e.institution ? `, ${e.institution}` : ''}`,
    summary: e.summary,
    location: e.location,
    start_date: e.start_date,
    end_date: e.end_date,
    date: e.date,
    img: e.img,
    links: transformLinks(e.links),
  }))
)

const experience = computed(() =>
  (infos.value.sections.experience || []).map((e) => ({
    name: e.position || e.company,
    summary: e.summary,
    location: e.location,
    start_date: e.start_date,
    end_date: e.end_date,
    img: e.img,
    links: transformLinks(e.links),
  }))
)

const projects = computed(() =>
  (infos.value.sections.projects || []).map((p) => ({
    name: p.name,
    summary: p.summary,
    location: p.location || '',
    start_date: p.start_date,
    end_date: p.end_date,
    date: p.date,
    img: p.img,
    links: transformLinks(p.links),
  }))
)

const email = computed(() => infos.value.email_display || infos.value.email)

const github = computed(() => {
  const networks = infos.value.social_networks || []
  const network = networks.find((n) => (n.network || '').toLowerCase() === 'github')
  return network ? network.username : ''
})
</script>

<template>
  <header class="intro">
    <h1 class="name">ULYSSE DURAND</h1><br />
    <h2 class="title">CURRICULUM</h2><br />
    <p class="about">
      {{ infos.desc }} <br />
      {{ infos.desc2 }}
    </p>
  </header>

  <h2>{{ labels.contact }}</h2>

  <ul>
    <li>Email: {{ email }}</li>
    <li>
      GitHub:
      <a :href="`https://github.com/${github}`">{{ github }}</a>
    </li>
  </ul>

  <h2>{{ labels.education }}</h2>

  <CVRow v-for="e in education" :key="e.name + e.start_date" v-bind="e" />

  <h2>{{ labels.experience }}</h2>

  <CVRow v-for="e in experience" :key="e.name + e.start_date" v-bind="e" />

  <h2>{{ labels.projects }}</h2>

  <CVRow v-for="p in projects" :key="p.name + (p.start_date || p.date)" v-bind="p" />
</template>
