import unittest
from app import math


class TestMy(unittest.TestCase):
    def test_useless_math(self):
        print("Hello")
        self.assertEqual(math(2, 2), 2)

    def test_new(self):
        self.assertEqual(math(10, 12), 22)

