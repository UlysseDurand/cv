from jinja2 import Environment, FileSystemLoader
from jinja2.filters import do_dictsort
import yaml
import markdown
import re
import sys

from src.config import Config, get_config

def load_infos(config):
    with open(config.input_file) as f:
        infos = yaml.safe_load(f)
    return infos

def build_yml(config: Config, infos):
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True
    )
    env.filters['to_nice_yaml'] = lambda value, indent=0: yaml.dump(
        value, default_flow_style=False, allow_unicode=True, indent=indent
    )
    template = env.get_template(config.yml_template_file)
    rendered = template.render(**infos)
    return rendered

def build_html(config: Config, infos):
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True
    )
    env.filters["mdlink"] = lambda text: re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text
    )
    template = env.get_template(config.html_template_file)
    rendered = template.render(**infos)
    return rendered

def main(config: Config):
    infos = load_infos(config)
    with open(config.yml_output_file, 'w') as f:
       f.write(build_yml(config, infos)) 
    with open(config.html_output_file, 'w') as f:
       f.write(build_html(config, infos)) 

if __name__ == '__main__':
    config = get_config()
    main(config)
