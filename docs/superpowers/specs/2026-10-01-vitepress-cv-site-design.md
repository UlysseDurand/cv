# VitePress CV Site — Design Spec

**Date:** 2026-10-01
**Status:** Approved, ready for implementation planning
**Scope:** A new static CV website under `docs/`. No changes to `src/` or `.github/`.

---

## Context

The CV currently reaches the web through two pieces of infrastructure in two different
repositories:

1. `src/main.py` scrapes the `infos.yml` file from every starred GitHub repo, merges the
   results with `base_infos.yml`, renders `build/cv.html` from `src/cv_template.html.j2`,
   and produces RenderCV PDF/HTML output.
2. `https://uldr.fr` is a **separate Jekyll site** (not in this repository) whose
   `main.markdown-body` fetches `https://ulyssedurand.github.io/cv/index.html` at runtime
   and injects the resulting body HTML into the page.

`build/cv.html` is a bare fragment — no `<html>`, no `<head>`, no stylesheet link. It only
renders correctly because uldr.fr's `assets/css/style.css` happens to define the `.cv-*`
class names it emits. The markup and its styling live in different repositories and are
coupled only by class-name convention.

Two sections defined in `base_infos.yml` — `skills` and `extracurricular_activities` —
are never rendered by `src/cv_template.html.j2`, so they appear in the PDF but have never
appeared on the web page.

## Goals

- Reimplement uldr.fr's visual design inside this repository, so markup and styles ship
  together and no cross-site HTML injection is involved.
- Make the web CV a self-contained, responsive VitePress site that builds and runs locally.
- Ship English and French, with a language switcher.
- Render the Skills and Extracurricular Activities sections that are currently missing.
- Leave the existing Python pipeline and Pages deployment untouched.

## Non-goals

- Replacing or deprecating the Python/RenderCV pipeline. It still produces the PDF, and
  the nightly cron still runs.
- Replacing the Jekyll site at uldr.fr. This site is local-only for now.
- Auto-updating the web CV from the scraped YAML. See "Rejected: data-driven content".
- Publishing. Deployment location is deliberately undecided.

---

## Decisions

### Content is hand-written, not generated

Each CV page is a hand-edited markdown file in `docs/`. Nothing in the Python pipeline
writes into `docs/`.

**Rejected — loading YAML via Vue components.** A VitePress `src:` data loader reading
`build/infos.yml` would keep one source of truth and let the nightly scrape update the
site automatically. Rejected because it reintroduces a build-time dependency on a
gitignored, network-fetched artifact, and because the page would be generated rather than
authored.

**Accepted consequence:** adding a project now means editing `docs/index.md` and
`docs/fr/index.md` by hand. The nightly cron updates the PDF but not this site.

### Pages are frontmatter-only

Each page's body is empty; all content lives in YAML frontmatter, and `CvPage.vue` renders
it.

**Rejected — prose markdown with inline components.** The CV is ~11 projects, 4
experiences and 5 education entries, each with the same eight fields, written twice (EN +
FR). Prose-plus-inline-HTML means hand-writing roughly 40 copies of the same nested markup
and keeping them in sync by hand. Frontmatter keeps the data structured, lets one
component own formatting for every entry, and makes EN/FR diffable line by line.

**Rejected — Python generating markdown into `docs/`.** Rejected under "Content is
hand-written".

### A custom layout replaces VitePress's default theme

`docs/.vitepress/theme/Layout.vue` overrides the theme's layout slot. No sidebar, no
VitePress navigation, no default-theme styling.

VitePress is used only as a Vue + Vite static-site generator with markdown support.

### Project images are committed to the repository

Images are copied to `docs/public/images/` and referenced as `/images/<name>.png`.

The current URLs are absolute paths into the live deployment —
`https://ulyssedurand.github.io/cv/repos_images/12.png` — where the numeric filename is an
incrementing counter assigned by `ImageCacheMaker._img_id` in scrape order. If the starred
repository list changes, existing numbers silently resolve to different projects.
Committing the files removes both the ordering fragility and the runtime dependency on the
old deployment staying up.

### Local-only, no deployment

No workflow changes. `.github/workflows/build_and_deploy.yml` is untouched and continues to
deploy the RenderCV output.

---

## Architecture

```
package.json                  # vitepress ^1.6.4; scripts docs:dev / docs:build / docs:preview
docs/
├── .vitepress/
│   ├── config.ts             # locales, appearance:false, srcExclude, title
│   └── theme/
│       ├── index.ts          # export { Layout }
│       ├── Layout.vue        # banner (EN/FR switch) + intro header + <Content/> + footer
│       ├── CvPage.vue        # renders frontmatter sections into uldr.fr markup
│       ├── components/
│       │   ├── CvEntry.vue   # image card: flush left/right rows + link pills
│       │   ├── EduRow.vue    # text-only education variant
│       │   ├── SkillsGroup.vue
│       │   └── LinkPill.vue
│       └── custom.css        # port of https://uldr.fr/assets/css/style.css
├── index.md                  # English content, frontmatter only
├── fr/index.md               # French content, frontmatter only
└── public/
    └── images/               # committed project thumbnails
```

`src/`, `requirements.txt`, `base_infos*.yml` and `.github/` are unmodified.

## Component responsibilities

Each component has one job and takes data via props. None of them fetch anything or read
global state.

| Component | Responsibility |
|---|---|
| `Layout.vue` | Page chrome only: language-switch banner, `.intro` header, footer. Renders `<Content />` between them. |
| `CvPage.vue` | Reads page frontmatter via `useData()`, hands each section to the right component, owns section ordering and localized section headings. |
| `CvEntry.vue` | One experience or project card. Renders the thumbnail, the two flush left/right rows, and the row of link pills. Emits no layout decisions of its own. |
| `EduRow.vue` | One education row. Same typographic treatment as `CvEntry` without the image or link pills. |
| `SkillsGroup.vue` | One labelled skills group (e.g. "Advanced expertise") rendered as a `.cv-row` card. |
| `LinkPill.vue` | One pill button. Suppresses the `↗` pseudo-element that plain links carry. |

## Content format

A CV page is identified by `pageType: cv` in its frontmatter. `Layout.vue` reads the
frontmatter, and when `pageType` is `cv` it renders `<CvPage />` in place of `<Content />`.
Because both CV pages have empty bodies, there is nothing for `<Content />` to render
otherwise. Any page without `pageType: cv` renders normally, leaving room for future
non-CV pages without touching `Layout.vue`.

`docs/index.md`:

```markdown
---
pageType: cv
title: Curriculum
about: >-
  I am a computer science student from ENS and ECL interested in formal proofs,
  logic and computational geometry.
pdf: https://ulyssedurand.github.io/cv/Ulysse_Durand_CV.pdf
contact:
  - { label: Email, value: "ulysse.durand [at] ens-lyon.fr" }
  - { label: GitHub, href: "https://github.com/UlysseDurand", value: UlysseDurand }
  - { label: Website, href: "https://uldr.fr", value: uldr.fr }
education:
  - org: École Centrale Lyon
    orgHref: "https://www.ec-lyon.fr/en/academics/general-engineering"
    area: General Engineering & Software Development
    location: Ecully, France
    start: 2024
    end: 2026
    summary: Double Masters Degree with ENS Lyon
    summaryHref: "https://www.ens-lyon.fr/en/studies/academic-programs/joint-diplomas/double-degree-ecole-centrale-de-lyon-engineering-research"
experience:
  - org: Kitware EU
    orgHref: "https://www.kitware.eu"
    position: Software Development Intern, Developer
    location: Villeurbanne
    start: 2026-03
    end: 2026-08
    summary: >-
      Internship at Kitware, software development around the trame framework
      for scientific and medical visualization.
    image: /images/kitware.png
    alt: Kitware logo
    links:
      - { label: Repository, href: "https://github.com/UlysseDurand/tfe" }
      - { label: Report, href: "https://github.com/UlysseDurand/tfe/releases/download/report/report.pdf" }
      - { label: Slides, href: "https://github.com/UlysseDurand/tfe/releases/download/slides/slides.pdf" }
projects:
  - title: Ray tracing coursework
    date: 2026
    summary: >-
      Coursework on ray tracing techniques, implementing BRDF, Monte-Carlo
      estimators and bounding volume hierarchy.
    image: /images/ray-tracing.png
    alt: Ray traced corridor
    links:
      - { label: Report, href: "https://github.com/UlysseDurand/computer_graphics/releases/download/report/REPORT.pdf" }
skills:
  - { label: Advanced expertise, details: Rocq, Ada/SPARK, OCaml, Python }
  - label: Normal expertise
    details: C++, CUDA, PyTorch, Docker, Git, GitLab-CI, Unity/C#, C, Haskell, Rust, Web Development, Java
  - { label: Languages, details: "English (Cambridge C1 Advanced), French (native)" }
extracurricular:
  - bullet: Competitive Programming, Prologin finalist in 2022
  - bullet: Organiser of week-long hike tours for 10 to 20 people every summer (2020–2023)
---
```

`docs/fr/index.md` mirrors this structure with translated values. The `links[].label`
values are also translated — the component looks the label up in the locale's label map,
falling back to the literal string, so a missing translation degrades to English rather
than rendering blank.

### Field reference

| Field | Used by | Notes |
|---|---|---|
| `pageType` | `Layout.vue` | Must be `cv`. Selects `CvPage` over `Content`. |
| `title` | `Layout.vue` | Sub-heading under the name. EN `Curriculum`, FR `Curriculum`. |
| `about` | `Layout.vue` | Short paragraph in `.intro`. |
| `pdf` | `Layout.vue` | Link to the RenderCV PDF, as on uldr.fr today. |
| `contact[]` | `Layout.vue` | `label`, optional `href`, `value`. Rendered as square-bulleted list. |
| `education[]` | `EduRow.vue` | `org`, `orgHref?`, `area`, `location`, `summary`, `summaryHref?`, `start`, `end` or `date`. |
| `experience[]` | `CvEntry.vue` | `org`, `orgHref?`, `position`, `location`, `summary`, `image?`, `alt?`, `start`, `end`, `links[]`. |
| `projects[]` | `CvEntry.vue` | `title`, `summary`, `date` or `start`/`end`, `image?`, `alt?`, `links[]`. |
| `skills[]` | `SkillsGroup.vue` | `label`, `details`. |
| `extracurricular[]` | `CvPage.vue` | `bullet`. Rendered as a square-bulleted list. |

## Styling

`custom.css` ports `https://uldr.fr/assets/css/style.css`, preserving the design tokens:

```css
:root {
  --head-foot-color: #DEDEE0;
  --button-color: #dedee0;
  --bg: #F2F2F5;
  --accent: #857AED;
  --hover: #958AFD;
  --link: #000070;
}
```

Fonts are Readex Pro 600/700 (`.intro .name`, `.intro .title`) and Montserrat 500 (`p`, `h2`,
`li`), loaded from Google Fonts. `body` is `width: min(50rem, 80vw); margin: 0 auto`.

Two required additions beyond a straight port:

- **`appearance: false` in `config.ts`.** VitePress otherwise injects its own colour
  variables and dark-mode handling, producing a half-themed page on machines set to dark.
  uldr.fr has no dark mode and neither will this.
- **Responsive `.cv-row`.** uldr.fr's `.cv-row` is an unconditional `display: flex` with a
  fixed `10rem` image and a `5em` date column. Below roughly 40rem the summary and date
  columns collide, so a `@media` rule stacks the image above the content and lets the date
  column size to content.

The `.cv-*` class names are retained so the port stays diffable against the original
stylesheet.

## i18n

Standard VitePress locale configuration:

```ts
locales: {
  root: { label: 'English', lang: 'en' },
  fr:    { label: 'Français', lang: 'fr' },
}
```

`docs/index.md` is the root locale; `docs/fr/index.md` maps to `/fr/`. Section headings and
link-pill labels come from a per-locale string map (`Education`/`Formation`,
`Skills`/`Compétences`, `Extracurricular Activities`/`Activités extrascolaires`,
`Repository`/`Dépôt`, `Report`/`Rapport`, `Slides`/`Diapositives`, `Demo`/`Démo`,
`Video`/`Vidéo`, `Paper`/`Article`). This matches the label set already defined in
`src/cv_template.html.j2`.

The switcher occupies the `.banner` slot at the top of the page — a rule uldr.fr's
stylesheet already defines but whose markup is currently commented out in its
`_layouts/default.html`. Reusing it avoids inventing new chrome.

## Failure modes

- **Malformed frontmatter** fails the VitePress build with a YAML parse error naming the
  file. There is no partially rendered page.
- **A missing or mistyped image path** renders a broken thumbnail. Mitigated by requiring
  `alt` text on every image so the omission is visible during review, and by visual review
  of both locales before finishing.
- **A missing label translation** falls back to the literal `links[].label` value.
- **Unknown frontmatter keys** are ignored silently by VitePress. Acceptable: the
  component props are the contract, and extra keys are harmless.

## Verification

No unit test suite — this is a static site with no runtime logic beyond rendering.

1. `npm run docs:build` exits with status 0.
2. `npm run docs:dev` serves `/` and `/fr/`; both render header, contact, all five
   sections, and the footer.
3. Visual comparison against the live `https://uldr.fr` and the approved replica mockup:
   same fonts, same colours, same card treatment, same pill buttons.
4. Narrow-viewport check at roughly 375px confirming `.cv-row` stacking.
5. `git status` shows no modification to `src/` or `.github/`.

## Implementation notes

- **This spec lives inside the VitePress `srcDir`.** `docs/superpowers/specs/` would
  otherwise be built into the site. `config.ts` must set
  `srcExclude: ['superpowers/**']`.
- `.superpowers/` (mockup working directory) must be added to `.gitignore`, alongside
  `node_modules/`, `docs/.vitepress/dist/` and `docs/.vitepress/cache/`.
- No changes to `.gitignore`'s existing `build/` rule — the Python build output stays
  ignored.
- Entry ordering is explicit in the markdown files; no automatic sorting by date. Sorting
  is currently done by `sort_key` in `src/fetcher.py`, which this site does not use.

## Open questions

None. All design decisions were resolved with the requester: purpose, content source,
deployment target, languages, layout approach, visual reference, and the two additional
sections.