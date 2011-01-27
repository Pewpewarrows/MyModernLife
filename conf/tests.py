"""
This is just a reference file for examples of how to 
use django TestCase and the various assert methods.
"""

from django.test import TestCase

class AppName(TestCase):
    def test_bool(self):
        self.assertTrue(True)
        self.assertFalse(False)

    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1, 2)

    def test_closeness(self):
        # Rounds to 7 decimal places by default
        self.assertAlmostEqual(1.000000001, 1.00000005)
        self.assertNotAlmostEqual()

    def new_tests(self):
        # Introduced in Python 2.7
        self.assertGreater()
        self.assertGreaterEqual()
        self.assertLess()
        self.assertLessEqual()

        self.assertMultiLineEqual()
        self.assertRegexpMatches()
        self.assertNotRegexpMatches()

        self.assertIn()
        self.assertNotIn()
        self.assertItemsEqual()
        self.assertSetEqual()
        self.assertDictEqual()
        self.assertDictContainsSubset()
        self.assertListEqual()
        self.assertTupleEqual()
        self.assertSequenceEqual()

        self.assertIsNone()
        self.assertIsNotNone()
        self.assertIs()
        self.assertIsNot()
        self.assertIsInstance()
        self.assertIsNotInstance()

