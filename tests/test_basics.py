from unittest import TestCase
from pyzer import add_one

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertEqual(add_one(5), 6)
