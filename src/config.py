class Config:
    def __init__(self, **kwargs):
        self.lang = kwargs.get("lang", "en")
        self.base_infos_file = kwargs.get("base_infos_file", f"base_infos{'_fr' if self.lang == 'fr' else ''}.yml")
        self.fetched_infos_file = kwargs.get("fetched_infos_file", f"build/infos{'_fr' if self.lang == 'fr' else ''}.yml")
        self.yml_template_file = kwargs.get("yml_template_file", "src/cv_template.yml.j2")
        self.html_template_file = kwargs.get("html_template_file", "src/cv_template.html.j2")
        suffix = "_fr" if self.lang == "fr" else ""
        self.yml_output_file = kwargs.get("yml_output_file", f"build/cv{suffix}.yml")
        self.html_output_file = kwargs.get("html_output_file", f"build/cv{suffix}.html")

def get_config(**kwargs) -> Config:
    return Config(**kwargs)
