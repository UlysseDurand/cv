<template>
  <div class="row" :style="{ marginBottom: '0.2em' }">
    <!-- Item image (optional) -->
    <div class="img-proj" v-if="img">
      <img :src="resolvedImg" alt="Item image" />
    </div>

    <div class="proj" :style="{ padding: '0.2em' }">
      <!-- Name + Location row -->
      <div class="flushleftright">
        <span class="flushleft" style="margin-bottom: 0.2em">
          <strong v-html="mdLinksToHtml(name)"></strong>
        </span>
        <span class="flushright">{{ location }}</span>
      </div>

      <!-- Summary + Date row -->
      <div class="flushleftright">
        <span class="flushleft"> <span v-html="mdLinksToHtml(summary)"></span> </span>
        <span class="flushright">
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
import { withBase } from 'vitepress'
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

// Resolve site-relative image paths against the configured base, leaving
// absolute (http/https) URLs untouched.
const resolvedImg = computed(() =>
  /^https?:\/\//.test(props.img || '') ? props.img : withBase(props.img)
)

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
    margin-top: 16px;
    padding: 8px;
    border-radius: 6px;
    background-color: var(--bg);
    overflow: hidden;

    display: flex;
    justify-content: space-between;
    gap: 1em;
    align-items: stretch;
}

.img-proj {
    height: 10rem;
    width: 10rem;
    order: 2;
}

.img-proj img {
    max-width: 100%;
    max-height: 100%;
    aspect-ratio: 1/1;
    border-radius: 4px;
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
    margin-bottom: 16px;
}

.flushright {
    text-align: right;
    min-width: 5em;
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

.banner {
    display: flex;
    justify-content: center;
    margin-bottom: 2em;
}

.banner a {
    background-color: var(--head-foot-color);
    font-size: 1rem;
    padding: 1rem;
    border: none;
    cursor: pointer;
    flex: 1;
    text-align: center;
    color: inherit;
    text-decoration: none;
}

.banner a:hover {
    background-color: var(--hover-color);
}
</style>