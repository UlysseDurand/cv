"""Regression tests for the CV pipeline. Run with `python -m unittest discover -s tests`."""

import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fetcher import sort_key
from src.renderer import apply_lang

COURSES_FILE = Path(__file__).resolve().parent.parent / "data" / "courses.yml"


class ApplyLangTests(unittest.TestCase):
    def test_non_french_is_returned_unchanged(self):
        infos = {"area": "Computer Science", "area_fr": "Informatique"}
        self.assertEqual(apply_lang(infos, "en"), infos)

    def test_french_overrides_base_keys_recursively(self):
        infos = {
            "sections": {
                "education": [
                    {"area": "Computer Science", "area_fr": "Informatique"}
                ]
            }
        }
        result = apply_lang(infos, "fr")
        self.assertEqual(result["sections"]["education"][0]["area"], "Informatique")

    def test_apply_lang_does_not_mutate_the_input(self):
        infos = {"area": "Computer Science", "area_fr": "Informatique"}
        apply_lang(infos, "fr")
        self.assertEqual(infos["area"], "Computer Science")


class SortKeyTests(unittest.TestCase):
    def test_prefers_end_date_then_date_then_start_date(self):
        self.assertEqual(sort_key({"end_date": 2024, "start_date": 2020}), "2024")
        self.assertEqual(sort_key({"date": 2019}), "2019")
        self.assertEqual(sort_key({"start_date": 2018}), "2018")
        self.assertEqual(sort_key({}), "")


class CoursesDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(COURSES_FILE, "r") as f:
            cls.groups = yaml.safe_load(f)["courses"]

    def test_every_course_has_names_in_both_languages(self):
        for group, data in self.groups.items():
            for course in data["courses"]:
                self.assertTrue(course.get("name_fr"), f"{group}: {course}")
                self.assertTrue(course.get("name"), f"{group}: {course}")

    def test_teachers_is_a_list_when_present(self):
        for group, data in self.groups.items():
            for course in data["courses"]:
                self.assertIsInstance(course.get("teachers", []), list, f"{group}: {course}")

    def test_course_names_are_unique_within_a_group(self):
        for group, data in self.groups.items():
            names = [course["name_fr"] for course in data["courses"]]
            self.assertEqual(len(names), len(set(names)), group)


if __name__ == "__main__":
    unittest.main()
