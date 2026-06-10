from github_scraper import retrieve_gh_star_list, retrieve_multiple_repos_graphql
import yaml

def retrieve_yml_infos(infos):
    yml_infos_str = infos.get("infos_yml", "")
    if yml_infos_str is None:
        return {}
    else:
        infos_yml = yaml.safe_load(yml_infos_str["text"])
        infos_yml["repository"] = f"https://github.com/{infos["nameWithOwner"]}"
        infos_yml["summary"] = infos["description"]
        infos_yml["img"] = infos["openGraphImageUrl"]
        for release_tag in ["report", "slides"]:
            release = infos[release_tag]
            if release is not None:
                for asset in release["releaseAssets"]["nodes"]:
                    infos_yml[release_tag] = asset["downloadUrl"]
        return infos_yml

def main():
    url = "https://github.com/stars/UlysseDurand/lists/curriculum"
    gh_projects = retrieve_gh_star_list(url)
    infos = retrieve_multiple_repos_graphql(gh_projects, {"infos_yml": "infos.yml"}, {"report": ("report", "report.pdf"), "slides": ("slides", "slides.pdf")})

    experience = []
    projects = []
    for _, repo_data in infos.items():
        infos_yml = retrieve_yml_infos(repo_data)
        if "company" in infos_yml:
            experience.append(infos_yml)
        elif len(infos_yml) > 0:
            projects.append(infos_yml)

    with open("base_infos.yml", "r") as f:
        cv_yml = yaml.safe_load(f)
        cv_yml["sections"]["experience"] = experience
        cv_yml["sections"]["projects"] = projects

    with open("intermediate/infos.yml", "w") as f:
        yaml.dump(cv_yml, f)

if __name__ == "__main__":
    main()
