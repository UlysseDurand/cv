# VitePress CV Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local VitePress site under `docs/` that reproduces the design of https://uldr.fr, ships English and French, and adds the Skills and Extracurricular Activities sections the web CV has always been missing.

**Architecture:** VitePress is used purely as a Vue + Vite static-site generator; its default theme is replaced by a custom `Layout.vue`, so there is no sidebar and no VitePress chrome. Each CV page is a markdown file with an empty body whose entire content lives in YAML frontmatter, discriminated by `pageType: cv`. Pure functions in `docs/lib/` handle date formatting and localized labels and are unit-tested with Vitest; components in `docs/components/` stay thin wrappers over those functions. The stylesheet is a direct port of `https://uldr.fr/assets/css/style.css`, keeping the original `.cv-*` class names so the port stays diffable.

**Tech Stack:** VitePress 1.6.4, Vue 3 SFC with `<script setup lang="ts">`, TypeScript, Vitest, plain CSS with custom properties. Node 26.8.2 and npm 11.19.1 are available.

**Spec:** `docs/superpowers/specs/2026-10-01-vitepress-cv-site-design.md` — read it before starting; this plan implements it and departs from it in exactly three places, all recorded under "Deviations from the spec" below.

## Global Constraints

- VitePress pinned to `^1.6.4`. Vitest pinned to `^3`. No other runtime dependencies.
- `appearance: false` in `docs/.vitepress/config.ts`. Without it VitePress injects its own colour variables and dark-mode handling, producing a half-themed page.
- `srcExclude: ['superpowers/**']` in `docs/.vitepress/config.ts`. The spec and this plan live inside the VitePress `srcDir` and must not be built into the site.
- Locales are exactly `root` (English, `docs/index.md`) and `fr` (French, `docs/fr/index.md`).
- **Do not modify** `src/`, `requirements.txt`, `base_infos.yml`, `base_infos_fr.yml`, or `.github/`. The Python pipeline and the existing Pages deployment must keep working untouched.
- Every CV page sets `pageType: cv` in frontmatter. `Layout.vue` renders `CvPage` for those and `Content` for anything else.
- Project and experience images live in `docs/public/images/` and are referenced as `/images/<name>.png`. Never reference `https://ulyssedurand.github.io/cv/repos_images/<n>.png` — those numeric filenames are scrape-order indices that silently resolve to the wrong project when the starred list changes.
- Link labels are localized from a `kind` key, never written literally in frontmatter.
- Every image in frontmatter carries an `alt` value.
- New entries appear in the order written in the markdown file. Do not add date sorting.

## Deviations from the spec

Three places where this plan corrects the spec. Each is deliberate.

1. **Links use `kind`, not `label`.** The spec's content example writes `links: [{ label: Report, ... }]` and separately describes localizing labels. Those two statements conflict: a literal `label` cannot be localized. Frontmatter now carries `kind: report`, and `linkLabel(kind, locale)` produces the displayed text. An unrecognized `kind` degrades to the kind string itself.
2. **Added `name` and four `pdf*` frontmatter fields.** The spec lists `title` (the sub-heading under the name) but no source for the name, and no source for the PDF-download sentence. Added: `name`, `pdfHref`, `pdfBefore`, `pdfLinkText`, `pdfAfter`. The PDF sentence is split around the link because the original markup does the same.
3. **Vitest is used after all.** The spec says "no unit test suite". This plan adds Vitest for the two pure modules in `docs/lib/`, because date formatting and the label fallback have real branching that a build-success check cannot catch. Components remain verified by build output assertions and visual review — no jsdom, no `@vue/test-utils`.

## Review Focus

Five input classes the spec implies but which no task's tests naturally exercise. Each has a test pinned to the task that owns the code.

1. **An entry carrying `date` instead of `start`/`end`** — real data does this: the Lycée Niepce education entry has `date: 2019`, and most projects have `date`. A naive formatter emits `2019 - ` or an empty range. Must render `2019`. → Task 2, Task 4.
2. **A link `kind` with no entry in the label map** — must render the kind string rather than a blank pill. → Task 2.
3. **An entry with no `image`** — education entries never have one, and a project may not either. Must render the card without a 10rem-wide hole. → Task 4.
4. **A section absent from frontmatter entirely, or present but empty** — a page with no `skills` key must render no Skills heading at all, not an empty heading. → Task 4.
5. **A long summary beside a long date range at narrow viewport** — uldr.fr's `.cv-row` is an unconditional flex with a fixed 10rem image and a 5em date column, which collides below roughly 40rem. Must stack. → Task 3 (rule), Task 7 (manual check; not grep-assertable).

---

### Task 1: Toolchain scaffold

**Files:**
- Create: `package.json`
- Create: `docs/.vitepress/config.ts`
- Create: `docs/index.md` (placeholder, replaced in Task 6)
- Modify: `.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces: npm scripts `docs:dev`, `docs:build`, `docs:preview`, `test`. A working VitePress build writing to `docs/.vitepress/dist/`. Vitest runnable from the repo root.

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "cv-docs",
  "private": true,
  "type": "module",
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs",
    "test": "vitest run"
  },
  "devDependencies": {
    "vitepress": "^1.6.4",
    "vitest": "^3"
  }
}
```

- [ ] **Step 2: Install dependencies**

Run: `npm install`
Expected: exits 0; `node_modules/vitepress` exists. Commit `package-lock.json`.

- [ ] **Step 3: Add build artifacts to `.gitignore`**

Append to `.gitignore`, keeping the existing `build/` rule untouched:

```
node_modules/
docs/.vitepress/dist/
docs/.vitepress/cache/
.superpowers/
```

Do not add `package-lock.json` to `.gitignore`; it is committed.

- [ ] **Step 4: Create `docs/.vitepress/config.ts`**

```ts
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Ulysse Durand',
  description: 'Curriculum vitae',
  appearance: false,
  srcExclude: ['superpowers/**'],
  locales: {
    root: { label: 'English', lang: 'en' },
    fr: { label: 'Français', lang: 'fr' },
  },
})
```

`themeConfig` is intentionally absent. The default theme is replaced in Task 3, so nav and sidebar config would be dead weight.

- [ ] **Step 5: Create placeholder `docs/index.md`**

```markdown
---
pageType: cv
name: Ulysse Durand
title: Curriculum
about: Placeholder, replaced in Task 6.
---

Placeholder, replaced in Task 6.
```

- [ ] **Step 6: Verify the build pipeline works**

Run: `npm run docs:build`
Expected: exits 0 and `docs/.vitepress/dist/index.html` exists.

- [ ] **Step 7: Verify Vitest is runnable**

Run: `npx vitest run --passWithNoTests`
Expected: exits 0 reporting no test files found.

- [ ] **Step 8: Commit**

```bash
git add package.json package-lock.json .gitignore docs/.vitepress/config.ts docs/index.md
git commit -m "build: scaffold VitePress site under docs/"
```

---

### Task 2: Date formatting and localized labels

**Files:**
- Create: `docs/lib/dates.ts`
- Create: `docs/lib/dates.test.ts`
- Create: `docs/lib/labels.ts`
- Create: `docs/lib/labels.test.ts`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `docs/lib/dates.ts` → `interface DateRange { date?: string | number; start?: string | number; end?: string | number }` and `formatDateRange(entry: DateRange): string`
  - `docs/lib/labels.ts` → `type Locale = 'en' | 'fr'`, `type LinkKind = 'demo' | 'video' | 'repository' | 'report' | 'slides' | 'paper'`, `type SectionKey = 'education' | 'experience' | 'projects' | 'skills' | 'extracurricular'`, `linkLabel(kind: string, locale: Locale): string`, `sectionHeading(key: SectionKey, locale: Locale): string`

These are the only two modules Tasks 3–7 import. Keep them free of Vue and Vite imports so Vitest needs no environment configuration.

- [ ] **Step 1: Write the failing test for `formatDateRange`**

Create `docs/lib/dates.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { formatDateRange } from './dates'

describe('formatDateRange', () => {
  it('returns the single date when only `date` is present', () => {
    expect(formatDateRange({ date: 2019 })).toBe('2019')
    expect(formatDateRange({ date: '2025-11' })).toBe('2025-11')
  })

  it('joins start and end with a spaced hyphen', () => {
    expect(formatDateRange({ start: 2019, end: 2022 })).toBe('2019 - 2022')
    expect(formatDateRange({ start: '2026-03', end: '2026-08' })).toBe('2026-03 - 2026-08')
  })

  it('prefers `date` over start and end when all three are present', () => {
    expect(formatDateRange({ date: 2019, start: 2018, end: 2019 })).toBe('2019')
  })

  it('omits the hyphen when only one bound is present', () => {
    expect(formatDateRange({ start: 2024 })).toBe('2024')
    expect(formatDateRange({ end: 2026 })).toBe('2026')
  })

  it('returns an empty string when no dates are present', () => {
    expect(formatDateRange({})).toBe('')
  })
})
```

The first and third cases are Review Focus item 1.

- [ ] **Step 2: Run the test to verify it fails**

Run: `npx vitest run docs/lib/dates.test.ts`
Expected: FAIL — cannot resolve `./dates`.

- [ ] **Step 3: Implement `formatDateRange` in `docs/lib/dates.ts`**

Export the `DateRange` interface above. Implement `formatDateRange` as an ordered guard sequence: return `String(entry.date)` if `date` is present; otherwise if both `start` and `end` are present return `` `${start} - ${end}` ``; otherwise return `String(start ?? end ?? '')`.

- [ ] **Step 4: Run the test to verify it passes**

Run: `npx vitest run docs/lib/dates.test.ts`
Expected: PASS, 5 tests.

- [ ] **Step 5: Write the failing test for the label lookups**

Create `docs/lib/labels.test.ts`:

```ts
import { describe, it, expect } from 'vitest'
import { linkLabel, sectionHeading } from './labels'

describe('linkLabel', () => {
  it('returns English labels', () => {
    expect(linkLabel('repository', 'en')).toBe('Repository')
    expect(linkLabel('slides', 'en')).toBe('Slides')
    expect(linkLabel('paper', 'en')).toBe('Paper')
  })

  it('returns French labels', () => {
    expect(linkLabel('repository', 'fr')).toBe('Dépôt')
    expect(linkLabel('slides', 'fr')).toBe('Diapositives')
    expect(linkLabel('report', 'fr')).toBe('Rapport')
  })

  it('falls back to the kind string for an unknown kind', () => {
    expect(linkLabel('transcript', 'fr')).toBe('transcript')
  })
})

describe('sectionHeading', () => {
  it('returns English headings', () => {
    expect(sectionHeading('education', 'en')).toBe('Education')
    expect(sectionHeading('extracurricular', 'en')).toBe('Extracurricular Activities')
  })

  it('returns French headings', () => {
    expect(sectionHeading('education', 'fr')).toBe('Formation')
    expect(sectionHeading('skills', 'fr')).toBe('Compétences')
    expect(sectionHeading('extracurricular', 'fr')).toBe('Activités extrascolaires')
  })
})
```

The third `linkLabel` case is Review Focus item 2.

- [ ] **Step 6: Run the test to verify it fails**

Run: `npx vitest run docs/lib/labels.test.ts`
Expected: FAIL — cannot resolve `./labels`.

- [ ] **Step 7: Implement the label lookups in `docs/lib/labels.ts`**

Export `Locale`, `LinkKind`, `SectionKey` as above. Define two module-private constant maps:

`LINK_LABELS` — `en`: `demo: 'Demo'`, `video: 'Video'`, `repository: 'Repository'`, `report: 'Report'`, `slides: 'Slides'`, `paper: 'Paper'`. `fr`: `demo: 'Démo'`, `video: 'Vidéo'`, `repository: 'Dépôt'`, `report: 'Rapport'`, `slides: 'Diapositives'`, `paper: 'Article'`.

`SECTION_HEADINGS` — `en`: `education: 'Education'`, `experience: 'Experience'`, `projects: 'Projects'`, `skills: 'Skills'`, `extracurricular: 'Extracurricular Activities'`. `fr`: `education: 'Formation'`, `experience: 'Expériences'`, `projects: 'Projets'`, `skills: 'Compétences'`, `extracurricular: 'Activités extrascolaires'`.

Both label sets are copied verbatim from the `labels` dict in `src/cv_template.html.j2`.

`linkLabel(kind, locale)` returns `LINK_LABELS[locale][kind] ?? LINK_LABELS.en[kind] ?? kind`. `sectionHeading(key, locale)` returns `SECTION_HEADINGS[locale][key] ?? SECTION_HEADINGS.en[key] ?? key`.

- [ ] **Step 8: Run the full test suite to verify it passes**

Run: `npm test`
Expected: PASS, 10 tests across 2 files.

- [ ] **Step 9: Commit**

```bash
git add docs/lib/
git commit -m "feat: add date formatting and localized label lookups"
```

---

### Task 3: Stylesheet port and layout chrome

**Files:**
- Create: `docs/.vitepress/theme/custom.css`
- Create: `docs/.vitepress/theme/Layout.vue`
- Create: `docs/.vitepress/theme/CvPage.vue` (placeholder, replaced in Task 4)
- Create: `docs/.vitepress/theme/index.ts`
- Modify: `docs/index.md`

**Interfaces:**
- Consumes: `Locale` from `docs/lib/labels.ts` (Task 2) to pick the active locale for the banner.
- Produces: the custom theme, exporting `Layout` from `docs/.vitepress/theme/index.ts`. `Layout.vue` reads frontmatter fields `pageType`, `name`, `title`, `about`, `contact[]` (`label`, optional `href`, `value`), `pdfHref`, `pdfBefore`, `pdfLinkText`, `pdfAfter`.

- [ ] **Step 1: Port the stylesheet to `docs/.vitepress/theme/custom.css`**

Copy the rule set from `https://uldr.fr/assets/css/style.css` and add the font link and two deviations. Preserve these verbatim:

```css
:root {
    --head-foot-color: #DEDEE0;
    --button-color: #dedee0;
    --bg: #F2F2F5;
    --accent: #857AED;
    --hover: #958AFD;
    --link: #000070;
}

body {
    width: min(50rem, 80vw);
    margin: 0 auto;
}

.intro .name {
    font-family: 'Readex Pro', sans-serif;
    font-weight: 700;
    font-size: 64px;
    letter-spacing: 1px;
}

.intro .title {
    font-family: 'Readex Pro', sans-serif;
    font-weight: 600;
    font-size: 64px;
    letter-spacing: 1px;
    color: var(--accent);
}

.cv-row {
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

.cv-img-proj { height: 10rem; width: 10rem; order: 2; }
.cv-flushright { text-align: right; min-width: 5em; }
```

Also carry over `.cv-proj`, `.cv-flushleftright`, `.cv-flushleft`, `.cv-links`, `a.cv-link`, `.cv-link::after { content: "" }`, `a::after { content: "↗" }`, `h2` underline rules, `.intro` border and grid rules, and `footer`.

Two deviations, both required:

```css
/* Below ~40rem the fixed 10rem image and 5em date column collide. */
@media (max-width: 40rem) {
    .cv-row { flex-direction: column; }
    .cv-img-proj { order: 0; width: 100%; height: auto; max-height: 12rem; }
    .cv-img-proj img { aspect-ratio: 16 / 9; }
    .cv-flushright { text-align: left; min-width: 0; }
}
```

and a font import at the top of the file:

```css
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&family=Readex+Pro:wght@600;700&display=swap');
```

The `@media` block is Review Focus item 5; it is verified by hand in Task 7.

- [ ] **Step 2: Create the placeholder `docs/.vitepress/theme/CvPage.vue`**

A component with an empty template. Task 4 replaces it. It must exist now because Step 3 imports it.

- [ ] **Step 3: Create `docs/.vitepress/theme/Layout.vue`**

`<script setup lang="ts">` importing `useData` from `vitepress`, `CvPage` from `./CvPage.vue`, `custom.css`, and `type Locale` from `../../lib/labels`. Derive `locale` from `lang.value === 'fr' ? 'fr' : 'en'`.

Template, in order:

1. `<nav class="banner">` containing two links, `English` to `/` and `Français` to `/fr/`, each an `<a>` with `class="nav-link"` plus `class="active"` on the one matching the current locale. This reuses the `.banner` rule the original stylesheet defines but whose markup the Jekyll layout leaves commented out.
2. `<header class="intro">` with `<h1 class="name">{{ frontmatter.name }}</h1>`, `<h2 class="title">{{ frontmatter.title }}</h2>`, `<p class="about">{{ frontmatter.about }}</p>`.
3. `<main>` containing an `<h2>Contact</h2>`, a `<ul>` of `frontmatter.contact` items — each `<li>` renders `label` then, when `href` is present, an `<a :href="item.href">{{ item.value }}</a>`, otherwise the bare `value` — then `<p>{{ frontmatter.pdfBefore }} <a :href="frontmatter.pdfHref">{{ frontmatter.pdfLinkText }}</a>{{ frontmatter.pdfAfter }}</p>`.
4. `<CvPage v-if="frontmatter.pageType === 'cv'" />` and `<Content v-else />`.
5. `<footer><p>© 2026 Ulysse Durand</p></footer>`.

"Contact" is identical in both languages, so it is not routed through `sectionHeading`.

- [ ] **Step 4: Create `docs/.vitepress/theme/index.ts`**

```ts
import Layout from './Layout.vue'
import './custom.css'

export default { Layout }
```

- [ ] **Step 5: Extend the placeholder `docs/index.md` frontmatter to cover every field `Layout.vue` reads**

Add `contact`, `pdfHref`, `pdfBefore`, `pdfLinkText`, `pdfAfter`. Task 6 replaces the whole file; this step exists so the layout renders without undefined values.

- [ ] **Step 6: Verify the chrome renders**

Run: `npm run docs:build`
Expected: exits 0.

Run: `grep -c 'ULYSSE\|Ulysse Durand' docs/.vitepress/dist/index.html`
Expected: a count of at least 1.

Run: `grep -c 'class="banner"' docs/.vitepress/dist/index.html`
Expected: `1`.

Run: `grep -o 'href="/fr/"' docs/.vitepress/dist/index.html`
Expected: exactly one match.

- [ ] **Step 7: Commit**

```bash
git add docs/.vitepress/theme/ docs/index.md
git commit -m "feat: add uldr.fr stylesheet port and custom layout chrome"
```

---

### Task 4: CV components

All five components ship together because they cannot be verified apart: a component only
reaches the built HTML through `CvPage`, so testing entry rendering before `CvPage` exists
would assert against an empty page.

**Files:**
- Create: `docs/components/LinkPill.vue`
- Create: `docs/components/CvEntry.vue`
- Create: `docs/components/EduRow.vue`
- Create: `docs/components/SkillsGroup.vue`
- Modify: `docs/.vitepress/theme/CvPage.vue` (replaces the Task 3 placeholder)

**Interfaces:**
- Consumes: `formatDateRange`, `DateRange` from `docs/lib/dates.ts`; `linkLabel`, `sectionHeading`, `SectionKey`, `Locale` from `docs/lib/labels.ts` (Task 2).
- Produces: five globally auto-registered VitePress components. Props:
  - `LinkPill` — `href: string`, `label: string`
  - `CvEntry` — `entry: CvEntryData`, `locale: Locale`, where `CvEntryData` is `{ title: string; titleHref?: string; meta?: string; location?: string; summary?: string; summaryHref?: string; image?: string; alt?: string; links?: Array<{ kind: string; href: string }> } & DateRange`
  - `EduRow` — `entry: EduData`, `locale: Locale`, where `EduData` is `{ org: string; orgHref?: string; area: string; location?: string; summary?: string; summaryHref?: string } & DateRange`
  - `SkillsGroup` — `group: { label: string; details: string }`

`locale` is a prop rather than a `useData()` read, so the components stay pure and `CvPage` owns locale in one place.

Frontmatter experience entries use `org` / `orgHref` / `position`, per the spec's field reference. `CvEntry` takes the generic `title` / `meta` instead, so `CvPage` maps between them — see Step 5.

- [ ] **Step 1: Create `LinkPill.vue`**

Renders `<a class="cv-link" :href="href"><p>{{ label }}</p></a>`. The `<p>` wrapper is required: the original stylesheet's `.cv-link *` rule sets `color: black` and resets margins, and it only matches element nodes.

- [ ] **Step 2: Create `CvEntry.vue`**

`<script setup lang="ts">` declaring props `entry: CvEntryData` and `locale: Locale`. Import `formatDateRange`, `linkLabel`, `LinkPill`, and the `DateRange` type.

Template, mirroring the markup emitted by `src/cv_template.html.j2`:

```vue
<div class="cv-row">
  <div v-if="entry.image" class="cv-img-proj">
    <img :src="entry.image" :alt="entry.alt ?? ''">
  </div>
  <div class="cv-proj">
    <div class="cv-flushleftright">
      <span class="cv-flushleft">
        <strong><a v-if="entry.titleHref" :href="entry.titleHref">{{ entry.title }}</a><template v-else>{{ entry.title }}</template></strong><template v-if="entry.meta">, {{ entry.meta }}</template>
      </span>
      <span class="cv-flushright">{{ entry.location }}</span>
    </div>
    <div class="cv-flushleftright">
      <span class="cv-flushleft">
        <a v-if="entry.summaryHref" :href="entry.summaryHref">{{ entry.summary }}</a><template v-else>{{ entry.summary }}</template>
      </span>
      <span class="cv-flushright">{{ formatDateRange(entry) }}</span>
    </div>
    <div v-if="entry.links?.length" class="cv-links">
      <LinkPill v-for="link in entry.links" :key="link.href" :href="link.href" :label="linkLabel(link.kind, locale)" />
    </div>
  </div>
</div>
```

`v-if="entry.image"` is Review Focus item 3. `v-if="entry.links?.length"` stops an empty link row adding stray margins.

- [ ] **Step 3: Create `EduRow.vue`**

Same structure as `CvEntry` minus the image and the link row. Title line renders `<strong>{{ org }}</strong>, {{ area }}`; `orgHref` wraps `org`, `summaryHref` wraps `summary`. Declare `locale` but leave it unused, so both row components share one signature.

- [ ] **Step 4: Create `SkillsGroup.vue`**

Renders one `.cv-row` card containing a `.cv-flushleftright` row: left span `<strong>{{ group.label }}</strong>`, right span `{{ group.details }}`. No date column, so it does not reuse `CvEntry`. This keeps the existing card language rather than inventing a style for one section.

- [ ] **Step 5: Replace `CvPage.vue` with the real implementation**

`<script setup lang="ts">` importing `useData` from `vitepress`, `sectionHeading`, `SectionKey`, `Locale`, `CvEntry`, `EduRow`, `SkillsGroup`, and the `CvEntryData` type. Derive `locale` from `lang.value === 'fr' ? 'fr' : 'en'` and read `frontmatter.value`.

Add the section-presence guard, used by all five sections:

```ts
const has = (key: SectionKey): boolean => {
  const v = frontmatter.value[key]
  return Array.isArray(v) && v.length > 0
}
```

This guard is Review Focus item 4: a missing `skills` key must produce no Skills heading at all, not an empty one. Wrap each section in `<template v-if="has('<key>')">` so the `<h2>` is inside the guard.

Add the experience mapper, since frontmatter uses `org`/`position` while `CvEntry` takes `title`/`meta`:

```ts
const toEntry = (e: ExperienceData): CvEntryData => ({
  title: e.org,
  titleHref: e.orgHref,
  meta: e.position,
  location: e.location,
  summary: e.summary,
  summaryHref: e.summaryHref,
  image: e.image,
  alt: e.alt,
  links: e.links,
  date: e.date,
  start: e.start,
  end: e.end,
})
```

where `ExperienceData` is `EduRow`'s `EduData` minus `area`, plus `position: string` and the image and link fields — the shape written in `docs/index.md` by Task 6. Projects need no mapping: their frontmatter already uses `title`.

Section bodies, in this order:

- **Education** — `<EduRow v-for="e in frontmatter.education" :key="e.org + e.area" :entry="e" :locale="locale" />`
- **Experience** — `<CvEntry v-for="e in frontmatter.experience" :key="e.org + e.start" :entry="toEntry(e)" :locale="locale" />`
- **Projects** — `<CvEntry v-for="p in frontmatter.projects" :key="p.title" :entry="p" :locale="locale" />`
- **Skills** — `<SkillsGroup v-for="s in frontmatter.skills" :key="s.label" :group="s" />`
- **Extracurricular** — a `<ul>` of `<li>{{ item.bullet }}</li>`, matching the square-bulleted style the original uses for contact items.

- [ ] **Step 6: Verify every component renders through a real build**

Temporarily replace `docs/index.md` with:

```markdown
---
pageType: cv
name: Ulysse Durand
title: Curriculum
about: Temporary content for Task 4 verification.
contact: [{ label: Email, value: "ulysse.durand [at] ens-lyon.fr" }]
pdfHref: "https://ulyssedurand.github.io/cv/Ulysse_Durand_CV.pdf"
pdfBefore: "Download the PDF"
pdfLinkText: "here"
pdfAfter: "."
education:
  - org: Lycée Niepce
    area: Science
    location: Chalon-sur-Saône, France
    summary: French Baccalaureate
    date: 2019
experience:
  - org: Kitware EU
    position: Software Development Intern
    location: Villeurbanne
    start: 2026-03
    end: 2026-08
    summary: Software development around the trame framework.
    image: /images/kitware.png
    alt: Kitware logo
    links:
      - { kind: repository, href: "https://github.com/UlysseDurand/tfe" }
      - { kind: slides, href: "https://example.invalid/slides.pdf" }
  - org: Entry Without An Image
    position: Test
    summary: Verifies the missing-image path.
    date: 2019
    links:
      - { kind: transcript, href: "https://example.invalid/t" }
projects:
  - title: Ray tracing coursework
    date: 2026
    summary: Implementing BRDF, Monte-Carlo estimators and BVH.
skills:
  - { label: Advanced expertise, details: Rocq, Ada/SPARK, OCaml, Python }
extracurricular:
  - bullet: Competitive Programming, Prologin finalist in 2022
---

Body intentionally empty.
```

Run: `npm run docs:build`
Expected: exits 0.

- [ ] **Step 7: Assert the rendered output**

Run: `grep -c 'cv-img-proj' docs/.vitepress/dist/index.html`
Expected: `1`. Only the Kitware entry has an image — confirms Review Focus item 3.

Run: `grep -o '>Software Development Intern<' docs/.vitepress/dist/index.html`
Expected: one match. Confirms the `position` → `meta` mapper ran.

Run: `grep -o '2026-03 - 2026-08' docs/.vitepress/dist/index.html`
Expected: one match. Confirms `formatDateRange` is wired in.

Run: `grep -o '>2019<' docs/.vitepress/dist/index.html | wc -l`
Expected: `2`. One from the image-less experience entry, one from the `date: 2019` education entry — Review Focus item 1 end to end.

Run: `grep -o '>Repository<\|>Slides<\|>transcript<' docs/.vitepress/dist/index.html | sort -u`
Expected: `>Repository<`, `>Slides<`, `>transcript<`. The unknown kind renders its own string — Review Focus item 2.

Run: `for s in Education Experience Projects Skills "Extracurricular Activities"; do printf '%s: ' "$s"; grep -c ">$s<" docs/.vitepress/dist/index.html; done`
Expected: `1` for each of the five.

Run: `grep -o 'Prologin finalist in 2022' docs/.vitepress/dist/index.html`
Expected: one match.

- [ ] **Step 8: Verify an absent section renders no heading**

Replace `docs/index.md` frontmatter with only `pageType`, `name`, `title`, `about`, `contact`, the four `pdf*` fields, and one `projects` entry.

Run: `npm run docs:build`
Expected: exits 0.

Run: `grep -c '>Skills<\|>Extracurricular Activities<\|>Education<\|>Experience<' docs/.vitepress/dist/index.html`
Expected: `0`. Confirms Review Focus item 4.

- [ ] **Step 9: Restore the placeholder and commit**

Run: `git checkout docs/index.md`

```bash
git add docs/components/ docs/.vitepress/theme/CvPage.vue
git commit -m "feat: add CV components and render all five sections"
```

---

### Task 5: Commit project images

**Files:**
- Create: `docs/public/images/` — 15 PNG files

**Interfaces:**
- Consumes: `build/repos_images/*.png`, produced by `python src/main.py --lang en`. On a fresh clone, regenerate with that command first, or download each file from `https://ulyssedurand.github.io/cv/repos_images/<n>.png`.
- Produces: the image filenames referenced as `/images/<name>.png` by Tasks 6 and 7.

- [ ] **Step 1: Copy and rename the images**

Run:

```bash
mkdir -p docs/public/images
cd build/repos_images
cp 12.png ../../../docs/public/images/kitware.png
cp 0.png  ../../../docs/public/images/mahindra-university.png
cp 1.png  ../../../docs/public/images/adacore.png
cp 2.png  ../../../docs/public/images/lsc-i2m.png
cp 13.png ../../../docs/public/images/mesh-manipulation.png
cp 14.png ../../../docs/public/images/ray-tracing.png
cp 6.png  ../../../docs/public/images/var-wgan.png
cp 5.png  ../../../docs/public/images/music-led-garland.png
cp 3.png  ../../../docs/public/images/cad-vr-unity.png
cp 4.png  ../../../docs/public/images/hiking-planner.png
cp 8.png  ../../../docs/public/images/ocaml-interpreter.png
cp 9.png  ../../../docs/public/images/minic-riscv.png
cp 10.png ../../../docs/public/images/automatic-proof-formal-grammars.png
cp 11.png ../../../docs/public/images/naive-parsing-ocaml.png
cp 7.png  ../../../docs/public/images/3d-scanner.png
```

The numeric source names are scrape-order indices from `ImageCacheMaker._img_id` in `src/fetcher.py`. Index 12 is Kitware, 0 is Mahindra, 1 is AdaCore, 2 is LSC, and 13 through 7 are the projects in the order listed above — confirm each rendered thumbnail against the entry text during the Task 7 visual review, since a mis-mapped index would be visually obvious but silently wrong.

- [ ] **Step 2: Verify all 15 files landed**

Run: `ls docs/public/images | wc -l`
Expected: `15`.

- [ ] **Step 3: Commit**

```bash
git add docs/public/images/
git commit -m "chore: commit project images for the CV site"
```

---

### Task 6: English content

**Files:**
- Modify: `docs/index.md` (replaces the placeholder)

**Interfaces:**
- Consumes: every component and lib function from Tasks 2–4, and the image filenames from Task 5.
- Produces: the complete English CV page.

- [ ] **Step 1: Write the full frontmatter**

Source the content from `base_infos.yml` for contact, education, skills and extracurricular entries, and from `build/infos.yml` for the four experiences and eleven projects. Required shape:

- `pageType: cv`, `name: Ulysse Durand`, `title: Curriculum`, `about` — the paragraph "I am a computer science student from ENS and ECL interested in formal proofs, logic and computational geometry."
- `contact` — Email written as `ulysse.durand [at] ens-lyon.fr` to match the existing obfuscation, GitHub to `https://github.com/UlysseDurand`, Website to `https://uldr.fr`.
- `pdfHref` — `https://ulyssedurand.github.io/cv/Ulysse_Durand_CV.pdf`. `pdfBefore` "Please download my LaTeX curriculum ", `pdfLinkText` "here", `pdfAfter` ", or enjoy its html version in the following."
- `education` — 5 entries, most recent first: École Centrale Lyon, ENS Lyon (Master), ENS Lyon (Bachelor), CPGE Blaise Pascal, Lycée Niepce. The last carries `date: 2019`, not `start`/`end`. None has an image.
- `experience` — 4 entries, most recent first, with `image` and `alt` on each: `images/kitware.png` 2026-03 to 2026-08; `images/mahindra-university.png` 2025-04 to 2025-07; `images/adacore.png` 2024-04 to 2024-07; `images/lsc-i2m.png` 2023-05 to 2023-07.
- `projects` — 11 entries using `title` and `date`, with images: `ray-tracing.png`, `mesh-manipulation.png`, `var-wgan.png`, `music-led-garland.png`, `cad-vr-unity.png`, `hiking-planner.png`, `ocaml-interpreter.png`, `minic-riscv.png`, `automatic-proof-formal-grammars.png`, `naive-parsing-ocaml.png`, `3d-scanner.png`.
- `skills` — the 3 groups from `base_infos.yml`, verbatim.
- `extracurricular` — the 2 bullets from `base_infos.yml`, verbatim.

Use `kind` for every link, never a literal label: `demo`, `video`, `repository`, `report`, `slides`, `paper`. Where `build/infos.yml` gives an entry both a summary and a linked summary, put the text in `summary` and the URL in `summaryHref`.

Body stays empty.

- [ ] **Step 2: Verify the build**

Run: `npm run docs:build`
Expected: exits 0.

- [ ] **Step 3: Verify content completeness**

Run: `grep -c 'class="cv-row"' docs/.vitepress/dist/index.html`
Expected: `23`. That is 5 education rows + 4 experience cards + 11 project cards + 3 skills cards. Every card-emitting component uses `cv-row`, so a count other than 23 means an entry was dropped or duplicated.

Run: `grep -o 'Ray tracing coursework\|Music Reacting LED Garland\|3D Scanner' docs/.vitepress/dist/index.html | sort -u | wc -l`
Expected: `3`.

Run: `grep -o 'Rocq, Ada/SPARK, OCaml, Python' docs/.vitepress/dist/index.html`
Expected: one match.

- [ ] **Step 4: Commit**

```bash
git add docs/index.md
git commit -m "docs: add English CV content"
```

---

### Task 7: French content and final verification

**Files:**
- Create: `docs/fr/index.md`

**Interfaces:**
- Consumes: everything from Tasks 2–7.
- Produces: the complete French CV page at `/fr/`, plus a verified build.

- [ ] **Step 1: Write the full French frontmatter**

Mirror `docs/index.md` field for field — identical keys, identical order, identical image paths. Translate values only:

- `title: Curriculum` stays `Curriculum`. `about` becomes "Je suis un étudiant en informatique de l'ENS et de l'ECL intéressé par les preuves formelles, la logique et la géométrie algorithmique."
- `pdfBefore` "Téléchargez mon curriculum LaTeX ", `pdfLinkText` "ici", `pdfAfter` ", ou consultez sa version html ci-dessous."
- Education, experience and project summaries in French, using the `*_fr` values already present in `build/infos.yml`.
- Location `Hyderabad, Inde` for Mahindra; the other locations keep their French spellings already in the data.
- `skills` and `extracurricular` translated.
- Do not translate `kind` values. `linkLabel` localizes them.

- [ ] **Step 2: Verify both locales build**

Run: `npm run docs:build`
Expected: exits 0, and both `docs/.vitepress/dist/index.html` and `docs/.vitepress/dist/fr/index.html` exist.

- [ ] **Step 3: Verify French headings are localized**

Run: `grep -o '>Formation<\|>Expériences<\|>Projets<\|>Compétences<\|>Activités extrascolaires<' docs/.vitepress/dist/fr/index.html | sort -u | wc -l`
Expected: `5`.

Run: `grep -o '>Education<\|>Experience<\|>Skills<' docs/.vitepress/dist/fr/index.html | wc -l`
Expected: `0`.

Run: `grep -o '>Dépôt<\|>Diapositives<\|>Rapport<\|>Article<' docs/.vitepress/dist/fr/index.html | sort -u`
Expected: whichever of these appear, all localized. Every French pill must be accented-decoded properly, not rendered as `D&eacute;pôt`.

- [ ] **Step 4: Verify the spec is not built into the site**

Run: `ls docs/.vitepress/dist/superpowers`
Expected: no such file or directory.

Run: `npm test`
Expected: PASS, 10 tests.

- [ ] **Step 5: Verify nothing outside `docs/` was touched**

Run: `git diff --stat main...HEAD -- src/ .github/ requirements.txt base_infos.yml base_infos_fr.yml`
Expected: empty output.

- [ ] **Step 6: Visual review, both locales, by hand**

Run: `npm run docs:dev`

Check, in both `/` and `/fr/`:

1. Fonts render — Readex Pro on the 64px name and title, Montserrat on body text. If Readex Pro falls back to a sans-serif, the `@import` in Step 1 of Task 3 is missing or malformed.
2. The title renders in purple `#857AED`; body links in `#000070`; cards in `#F2F2F5`.
3. Every project thumbnail shows the correct project. Compare against the `image` values in Task 5 Step 1 — a wrong index is obvious here and nowhere else.
4. Link pills read Repository/Report/Slides in English and Dépôt/Rapport/Diapositives in French, and plain links carry the `↗` arrow while pills do not.
5. Narrow the viewport to roughly 375px: cards stack, the image moves above the text, and dates sit flush left rather than colliding. This is the manual half of Review Focus item 5.
6. The EN/FR banner in `.banner` links to `/` and `/fr/` and marks the current one active.

Stop the dev server when finished.

- [ ] **Step 7: Commit**

```bash
git add docs/fr/index.md
git commit -m "docs: add French CV content"
```