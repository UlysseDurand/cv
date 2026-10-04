import subprocess

from .config import Config, LOCALES, get_config
from .fetcher import fetch_cv_infos
from .renderer import render_cv_from_templates


def main(config: Config):
    print("Fetching CV infos (all languages)...")
    fetch_cv_infos(config)
    print("Rendering CV from templates...")
    render_cv_from_templates(config)
    for lang in LOCALES:
        yml_file = config.rendered_yml_path(lang)
        # rendercv resolves `--output-folder` relative to the input file's directory.
        output_folder = config.rendercv_output_dir(lang).relative_to(yml_file.parent)
        print(f"Rendering {lang} CV with rendercv...")
        subprocess.run(
            ["rendercv", "render", str(yml_file), "--output-folder", str(output_folder)],
            check=True,
        )


if __name__ == '__main__':
    main(get_config())
