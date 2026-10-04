from jinja2 import Environment, FileSystemLoader
import copy
import os
import yaml

from .config import Config, LOCALES


def apply_lang(infos, lang):
    """Return a copy of infos with the `_fr` variants applied when lang is French."""
    infos = copy.deepcopy(infos)
    if lang != "fr":
        return infos

    def process(obj):
        if isinstance(obj, dict):
            # First process all values recursively
            for key in list(obj.keys()):
                obj[key] = process(obj[key])
            # Then replace _fr keys
            for key in list(obj.keys()):
                if key.endswith("_fr"):
                    base_key = key[:-3]
                    obj[base_key] = obj[key]
            return obj
        elif isinstance(obj, list):
            return [process(item) for item in obj]
        return obj

    return process(infos)


def load_infos(config: Config):
    with open(config.fetched_infos_file) as f:
        infos = yaml.safe_load(f)
    # Courses are authored separately from the fetched CV data and only feed the
    # docs site. Attaching them here means `apply_lang` resolves their `*_fr`
    # keys the same way, and they end up in `infos.localized.yml` for free.
    with open(config.courses_file) as f:
        infos["courses"] = yaml.safe_load(f)["courses"]
    return infos


def _make_env(**filters):
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters.update(filters)
    return env


def _to_yml_scalar(value):
    if value is None or value == '':
        return ''
    s = yaml.safe_dump(
        value,
        default_flow_style=False,
        allow_unicode=True,
        width=10**6,
    )
    if s.endswith('\n...\n'):
        s = s[:-len('\n...\n')]
    return s


def build_yml(config: Config, infos, lang):
    env = _make_env(to_yml_scalar=_to_yml_scalar)
    template = env.get_template(config.yml_template_file)
    return template.render(lang=lang, **infos)


def render_cv_from_templates(config: Config):
    infos = load_infos(config)
    os.makedirs(config.build_dir, exist_ok=True)
    localized_by_lang = {}
    for lang in LOCALES:
        # The yml template expects the localized values already applied: it
        # only switches section titles and locale based on `lang`.
        localized_infos = apply_lang(infos, lang)
        localized_by_lang[lang] = localized_infos
        with open(config.rendered_yml_path(lang), 'w') as f:
            f.write(build_yml(config, localized_infos, lang))
    # The docs site consumes `infos.localized.yml`, so the `*_fr` resolution
    # logic lives only here (Python) instead of being reimplemented in TypeScript.
    with open(config.localized_infos_file, 'w') as f:
        yaml.dump(localized_by_lang, f, allow_unicode=True)
