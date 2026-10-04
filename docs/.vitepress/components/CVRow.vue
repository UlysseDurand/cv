<template>
  <div class="cv-row" :style="{ marginBottom: '0.2em' }">
    <!-- Item image (optional) -->
    <div class="cv-img-proj" v-if="img">
      <img :src="img" alt="Item image" />
    </div>

    <div class="cv-proj" :style="{ padding: '0.2em' }">
      <!-- Name + Location row -->
      <div class="cv-flushleftright">
        <span class="cv-flushleft" style="margin-bottom: 0.2em">
          <strong v-html="mdLinksToHtml(name)"></strong>
        </span>
        <span class="cv-flushright">{{ location }}</span>
      </div>

      <!-- Summary + Date row -->
      <div class="cv-flushleftright">
        <span class="cv-flushleft"> <span v-html="mdLinksToHtml(summary)"></span> </span>
        <span class="cv-flushright">
          <template v-if="date">
            {{ date }}
          </template>
          <template v-else>
            {{ start_date }} -<br />
            {{ end_date }}
          </template>
        </span>
      </div>

      <!-- Links row (optional) -->
      <div class="cv-links" v-if="sortedLinks.length > 0">
        <a
          v-for="link in sortedLinks"
          :key="link.url"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="cv-link"
        >
          <p>{{ link.label }}</p>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { mdLinksToHtml } from '../theme/utils'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  summary: {
    type: String,
    required: true,
  },
  location: {
    type: String,
    required: true,
  },
  date: {
    type: [String, Number],
    required: false,
  },
  start_date: {
    type: [String, Number],
    required: false,
  },
  end_date: {
    type: [String, Number],
    required: false,
  },
  img: {
    type: String,
    required: false,
  },
  links: {
    type: Array,
    required: false,
    default: () => [],
  },
})

const sortedLinks = computed(() => {
  const priorityOrder = ['Repository', 'Report', 'Slides']
  
  return [...props.links].sort((a, b) => {
    const aIndex = priorityOrder.indexOf(a.label)
    const bIndex = priorityOrder.indexOf(b.label)
    
    if (aIndex !== -1 && bIndex !== -1) {
      return aIndex - bIndex
    }
    if (aIndex !== -1) return -1
    if (bIndex !== -1) return 1
    return a.label.localeCompare(b.label)
  })
})
</script>

<style scoped>
/* Styles are in the global theme style.css */
</style>