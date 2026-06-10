class Config:
    def __init__(self):
        self.input_file = "intermediate/infos.yml"
        self.yml_template_file = "src/cv_template.yml.j2"
        self.html_template_file = "src/cv_template.html.j2"
        self.yml_output_file = "intermediate/cv.yml"
        self.html_output_file = "intermediate/cv.html"

def get_config(**kwargs) -> Config:
    return Config()