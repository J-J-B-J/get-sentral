"""Test main.py"""
import unittest
from json import load, dumps

from SentralTimetable.main import *


class TestScrapeTimetable(unittest.TestCase):
    def test_empty_timetable(self):
        self.assertEqual(
            {'classes': {}, 'notices': []},
            scrape_timetable('')
        )

    def test_non_html_timetable(self):
        self.assertEqual(
            {'classes': {}, 'notices': []},
            scrape_timetable('Hi!')
        )

    def test_actual_timetable(self):
        with open('Test_HTML.html') as f:
            test_html = f.read()
        with open('Test_Json.json') as f:
            test_json = load(f)
        self.assertEqual(
            dumps(test_json),
            dumps(scrape_timetable(test_html))
        )


if __name__ == '__main__':
    unittest.main()
