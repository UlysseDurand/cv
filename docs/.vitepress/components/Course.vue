<template>
  <div class="row" :style="{ marginBottom: '0.2em' }">
    <div class="proj" :style="{ padding: '0.2em' }">
      <!-- Name + Location row -->
      <div class="flushleftright">
        <span class="flushleft" style="margin-bottom: 0.2em">
          <strong v-html="mdLinksToHtml(name)"></strong>
        </span>
        <span class="flushright">{{ location }}</span>
      </div>

      <!-- Description + Date row -->
      <div class="flushleftright">
        <span class="flushleft">
          <span v-if="description" v-html="mdLinksToHtml(description)"></span>
        </span>
        <span class="flushright">
          <template v-if="date">
            {{ date }}
          </template>
        </span>
      </div>

      <!-- Teachers row (optional) -->
      <div class="teachers" v-if="teachers.length > 0">
        <span class="teachers-list">
          <template v-for="(teacher, index) in teachers" :key="teacher">
            <Teacher :name="teacher" /><span v-if="index < teachers.length - 1"></span>
          </template>
        </span>
      </div>

      <!-- Links row (optional) -->
      <div class="links" v-if="sortedLinks.length > 0">
        <a
          v-for="link in sortedLinks"
          :key="link.url"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          class="link"
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
import Teacher from './Teacher.vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: false,
    default: '',
  },
  location: {
    type: String,
    required: false,
    default: '',
  },
  date: {
    type: [String, Number],
    required: false,
  },
  teachers: {
    type: Array,
    required: false,
    default: () => [],
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

.row {
    margin-left: 32px;
    margin-right: 32px;
    margin-top: 8px;
    padding: 8px;
    border-radius: 6px;
    background-color: var(--bg);
    overflow: hidden;

    display: flex;
    justify-content: space-between;
    gap: 1em;
    align-items: stretch;
}

.proj {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    min-height: 100%;
}

.flushleftright {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.flushleft {
    font-family: sans-serif;
    text-align: left;
    margin-bottom: 4px;
}

.flushright {
    text-align: right;
    min-width: 5em;
}

.teachers {
    font-family: sans-serif;
    font-size: 0.9rem;
    margin-bottom: 4px;
    color: var(--vp-c-text-2);
}

.teachers-label {
    font-weight: 600;
    margin-right: 0.3em;
}

.teachers-list a,
.teachers-list span {
    color: inherit;
}

.teachers-list a {
    text-decoration: underline;
}

.links {
    display: flex;
    margin-top: auto;
}

a.link {
    font-size: 1rem;
    margin: 0 0.3em;
    padding: 0.5em;
    border: none;
    cursor: pointer;
    flex: 1;
    text-align: center;
    align-items: center;
    font-weight: 5px;
    border-radius: 2px;
    background-color: var(--button-color);
}

.link:after {
    content: ""
}

.link * {
    margin-left: 0px;
    margin-bottom: 0px;
    margin-top: 0px;
    color: black;
}

.link:hover * {
    color: white;
}

</style>
