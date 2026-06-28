class Config:
    def __init__(self, **kwargs):
        self.fetched_infos_file = kwargs.get("fetched_infos_file", "build/infos.yml")
        self.yml_template_file = kwargs.get("yml_template_file", "src/cv_template.yml.j2")
        self.html_template_file = kwargs.get("html_template_file", "src/cv_template.html.j2")
        self.yml_output_file = kwargs.get("yml_output_file", "build/cv.yml")
        self.html_output_file = kwargs.get("html_output_file", "build/cv.html")

def get_config(**kwargs) -> Config:
    return Config(**kwargs)