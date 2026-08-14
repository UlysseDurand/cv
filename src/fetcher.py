from github_scraper import retrieve_gh_star_list, retrieve_multiple_repos_graphql
import yaml
import os
import time
import requests
from pathlib import Path
from config import Config

IMAGES_DOWNLOAD_DIR = Path("build/repos_images")
IMAGES_SERVE_SUFFIX = "repos_images"


class ImageCacheMaker:
    """Downloads remote images to make the page serve them itself"""

    _img_id = 0

    def __init__(self, download_dir: Path, serve_url_suffix_base: str):
        """download_dir must be served at serve_url_suffix_base"""
        self._download_dir = download_dir
        self._serve_url_suffix_base = serve_url_suffix_base

    def download(self, url: str, fallback_url: str = None):
        local_path = self._download_dir / f"{self._img_id}.png"
        try:
            download_remote_image(url, local_path)
        except Exception:
            if fallback_url is None:
                raise
            print(f"    Falling back to {fallback_url}")
            download_remote_image(fallback_url, local_path)
        serve_url_suffix = f"{self._serve_url_suffix_base}/{self._img_id}.png"
        self._img_id += 1
        return "https://ulyssedurand.github.io/cv/"+serve_url_suffix


def download_remote_image(remote_url: str, local_path: str, max_retries: int = 5):
    for attempt in range(max_retries):
        response = requests.get(remote_url)

        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
                print(f"    Saved {local_path}")
            return

        if response.status_code == 429:  # Too many requests
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else (2**attempt)
            print(
                f"      Rate limited fetching {remote_url}, retrying in {wait:.1f}s "
                f"(attempt {attempt + 1}/{max_retries})..."
            )
            time.sleep(wait)
            continue

        raise Exception(
            f"Failed to download {remote_url}, status code: {response.status_code}"
        )

    raise Exception(
        f"Failed to download {remote_url} after {max_retries} retries (still rate limited)."
    )


def retrieve_yml_infos(infos, image_cache_maker):
    yml_infos_str = infos.get("infos_yml", "")
    if yml_infos_str is None:
        return {}
    else:
        infos_yml = yaml.safe_load(yml_infos_str["text"])
        infos_yml["repository"] = f"https://github.com/{infos["nameWithOwner"]}"
        infos_yml["remoteImage"] = infos["openGraphImageUrl"]
        fallback_url = f"https://opengraph.githubassets.com/1/{infos["nameWithOwner"]}"
        infos_yml["img"] = image_cache_maker.download(infos["openGraphImageUrl"], fallback_url)
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
    image_cache_maker = ImageCacheMaker(IMAGES_DOWNLOAD_DIR, IMAGES_SERVE_SUFFIX)
    os.makedirs(IMAGES_DOWNLOAD_DIR, exist_ok=True)
    for _, repo_data in infos.items():
        infos_yml = retrieve_yml_infos(repo_data, image_cache_maker)
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
