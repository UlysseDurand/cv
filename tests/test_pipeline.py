"""Regression tests for the CV pipeline. Run with `python -m unittest discover -s tests`."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fetcher import sort_key
from src.renderer import apply_lang


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


if __name__ == "__main__":
    unittest.main()
