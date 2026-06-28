from config import Config, get_config
from fetcher import fetch_cv_infos
from renderer import render_cv_from_templates
import os

def main(config: Config):
    print("Fetching CV infos...")
    fetch_cv_infos(config)
    print("Rendering CV from templates...")
    render_cv_from_templates(config)
    os.system(f"rendercv render {config.yml_output_file}")

if __name__ == '__main__':
    config = get_config()
    main(config)
