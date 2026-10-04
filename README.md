# CV

This project is for rendering the CV as a PDF, in both English and French.

## Build

The build fetches the CV data (base info from `base_infos.yml` plus GitHub
project metadata), writes a single `build/infos.yml` containing both the
English and French strings, then renders both languages.

```sh
python -m src.main
```

No `--lang` parameter is needed: the language is not selected at fetch time
anymore. All localized variants (`*_fr` keys) are kept in `build/infos.yml`,
and each output is produced in both languages in a single run:

- `build/cv.yml` / `build/cv_fr.yml` (rendercv input)
- `build/rendercv_output/` and `build/rendercv_output_fr/` (PDFs, via rendercv)
- `build/infos.localized.yml` (per-locale data for the docs site)

The GitHub Actions workflow (`.github/workflows/build_and_deploy.yml`) runs
this single command, then builds the VitePress docs site (see below) and
publishes everything to GitHub Pages.

## Tests

```sh
python -m unittest discover -s tests
```

## Docs site (VitePress)

The public site is a VitePress project in `docs/`. It reads
`build/infos.localized.yml` (via the `yaml` package), which the Python build
produces with the `*_fr` variants already resolved per locale, so run the
Python build first.

```sh
python -m src.main
npm install
npm run docs:build      # or: npm run docs:dev
```

The site is bilingual:

- `/` serves French (the default locale, also available at `/fr/`)
- `/en/` serves English

A language switcher is shown in the page header. The `*_fr` resolution is
implemented once, in `src/renderer.py`, and the site simply picks the locale's
pre-resolved data.

When deploying, the VitePress output (`docs/.vitepress/dist`) owns the site
root, and the rendercv PDFs are published under the locale paths:
`/en/Ulysse_Durand_CV.pdf` (English) and `/fr/Ulysse_Durand_CV.pdf` (French).
