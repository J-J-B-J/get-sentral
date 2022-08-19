"""Test main.py"""
import unittest
from json import load

from SentralTimetable.main import *


class TestScrapeTimetable(unittest.TestCase):
    def test_empty_timetable(self):
        self.assertEqual(
            scrape_timetable(''),
            {'classes': {}, 'notices': []}
        )

    def test_non_html_timetable(self):
        self.assertEqual(
            scrape_timetable('Hi!'),
            {'classes': {}, 'notices': []}
        )

    def test_actual_timetable(self):
        with open('Test_HTML.html') as f:
            test_html = f.read()
        with open('Test_Json.json') as f:
            test_json = load(f)
        self.assertEqual(
            test_json,
            scrape_timetable(test_html)
        )


if __name__ == '__main__':
    unittest.main()
