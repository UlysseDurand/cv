from github_scraper import retrieve_gh_star_list, retrieve_multiple_repos_graphql
import yaml
import os
from config import Config


def retrieve_yml_infos(infos):
    yml_infos_str = infos.get("infos_yml", "")
    if yml_infos_str is None:
        return {}
    else:
        infos_yml = yaml.safe_load(yml_infos_str["text"])
        infos_yml["repository"] = f"https://github.com/{infos["nameWithOwner"]}"
        infos_yml["img"] = infos["openGraphImageUrl"]
        infos_yml["name"] = infos["description"]
        for release_tag in ["report", "slides"]:
            release = infos[release_tag]
            if release is not None:
                for asset in release["releaseAssets"]["nodes"]:
                    infos_yml[release_tag] = asset["downloadUrl"]
        return infos_yml

def sort_key(entry):
    return str(entry.get("end_date") or entry.get("date") or entry.get("start_date") or "")

def fetch_cv_infos(config: Config):
    url = "https://github.com/stars/UlysseDurand/lists/curriculum"
    gh_projects = retrieve_gh_star_list(url)
    infos = retrieve_multiple_repos_graphql(gh_projects, {"infos_yml": "infos.yml"}, {"report": ("report", "report.pdf"), "slides": ("slides", "slides.pdf")})
    experiences = []
    projects = []
    for _, repo_data in infos.items():
        infos_yml = retrieve_yml_infos(repo_data)
        if "company" in infos_yml:
            experiences.append(infos_yml)
            infos_yml["summary"] = infos_yml["name"]
            del infos_yml["name"]
        elif len(infos_yml) > 0:
            projects.append(infos_yml)
    experiences.sort(key=sort_key, reverse=True)
    projects.sort(key=sort_key, reverse=True)
    with open("base_infos.yml", "r") as f:
        cv_yml = yaml.safe_load(f)
        cv_yml["sections"]["experience"] = experiences
        cv_yml["sections"]["projects"] = projects
        cv_yml["sections"]["education"].sort(key=sort_key, reverse=True)
    os.makedirs(os.path.dirname(config.fetched_infos_file), exist_ok=True)
    with open(config.fetched_infos_file, "w") as f:
        yaml.dump(cv_yml, f)
