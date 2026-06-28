from jinja2 import Environment, FileSystemLoader
import yaml
import re

from config import Config

def load_infos(config):
    with open(config.fetched_infos_file) as f:
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

def render_cv_from_templates(config: Config):
    infos = load_infos(config)
    with open(config.yml_output_file, 'w') as f:
       f.write(build_yml(config, infos)) 
    with open(config.html_output_file, 'w') as f:
       f.write(build_html(config, infos)) 
