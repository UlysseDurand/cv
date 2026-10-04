import '@fontsource-variable/readex-pro'
import '@fontsource/montserrat'
import './style.css'
import Layout from './Layout.vue'
import CVRow from '../components/CVRow.vue'
import CVPage from '../components/CVPage.vue'

import type { Theme } from 'vitepress'

export default {
    Layout,
    enhanceApp({ app }) {
        app.component('CVRow', CVRow)
        app.component('CVPage', CVPage)
    }
} satisfies Theme