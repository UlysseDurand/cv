/// <reference types="vitepress/client" />

// Provided by the `cv-infos` Vite plugin in `docs/.vitepress/config.mts`,
// from `build/infos.localized.yml`.
declare module 'virtual:infos' {
  const infosByLang: Record<string, any>
  export default infosByLang
}
