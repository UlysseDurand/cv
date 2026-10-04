"""Central place for input files, output locations and pipeline constants."""

from pathlib import Path

# All localized variants produced by a single build. The first entry is the
# default locale and keeps the unsuffixed output names.
LOCALES = ("en", "fr")


class Config:
    def __init__(self, **kwargs):
        # Inputs
        self.base_infos_file = Path(kwargs.get("base_infos_file", "base_infos.yml"))

        # Generated data shared with the VitePress docs site.
        self.build_dir = Path(kwargs.get("build_dir", "build"))
        self.fetched_infos_file = Path(
            kwargs.get("fetched_infos_file", self.build_dir / "infos.yml")
        )
        # Per-locale resolved data (same `*_fr` resolution as the PDF render).
        self.localized_infos_file = Path(
            kwargs.get("localized_infos_file", self.build_dir / "infos.localized.yml")
        )

        # Templates
        self.yml_template_file = kwargs.get("yml_template_file", "src/cv_template.yml.j2")

        # Remote GitHub data
        self.star_list_url = kwargs.get(
            "star_list_url", "https://github.com/stars/UlysseDurand/lists/curriculum"
        )
        self.additional_files = kwargs.get("additional_files", {"infos_yml": "infos.yml"})
        self.release_tags = kwargs.get(
            "release_tags",
            {"Report": ("report", "report.pdf"), "Slides": ("slides", "slides.pdf")},
        )

        # Image cache: remote images are downloaded locally and served by the site.
        self.images_dir = Path(kwargs.get("images_dir", self.build_dir / "repos_images"))
        self.images_serve_url = kwargs.get(
            "images_serve_url", "https://ulyssedurand.github.io/cv/repos_images"
        )

    def _suffixed(self, stem: str, lang: str) -> Path:
        # English keeps the unsuffixed historical names; other languages add `_<lang>`.
        suffix = "" if lang == "en" else f"_{lang}"
        return self.build_dir / f"{stem}{suffix}"

    def rendered_yml_path(self, lang: str) -> Path:
        return self._suffixed("cv", lang).with_suffix(".yml")

    def rendercv_output_dir(self, lang: str) -> Path:
        return self._suffixed("rendercv_output", lang)


def get_config(**kwargs) -> Config:
    return Config(**kwargs)
