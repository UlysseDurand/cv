class Config:
    def __init__(self):
        self.input_file = "infos.yml"
        self.yml_template_file = "cv_template.yml.j2"
        self.html_template_file = "html_template.html.j2"
        self.yml_output_file = "cv.yml"
        self.html_output_file = "cv.html"

def get_config(**kwargs) -> Config:
    return Config()