from config import Config, get_config
from fetcher import fetch_cv_infos
from renderer import render_cv_from_templates
import os
import argparse

def main(config: Config):
    print(f"Fetching CV infos (lang={config.lang})...")
    fetch_cv_infos(config)
    print("Rendering CV from templates...")
    render_cv_from_templates(config)
    output_folder = f"rendercv_output{'_fr' if config.lang == 'fr' else ''}"
    os.system(f"rendercv render {config.yml_output_file} --output-folder {output_folder}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["en", "fr"], default="en", help="Language for the CV")
    args = parser.parse_args()
    config = get_config(lang=args.lang)
    main(config)
