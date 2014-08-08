
import unittest
import differ
from difflib import ndiff, restore


class TestDiffContentFunctions(unittest.TestCase):

    def setUp(self):

        self.content_orignal = """
            this is a test file.
            line 2
            line 3"""

        self.content_new = """
            this is a new test file.
            line 2
            line 3 space
            line 4"""


    def test_get_diff(self):

        diff = differ.DiffContent.get_diff(self.content_orignal, self.content_new)

        self.assertEqual(
            ''.join(diff), 
            ''.join(ndiff(
                self.content_orignal, 
                self.content_new
            ))
        )

    def test_get_revised(self):

        diff = differ.DiffContent.get_diff(self.content_orignal, self.content_new)

        self.assertEqual(
            differ.DiffContent.get_revised(diff), 
            self.content_new
        )

    def test_get_original(self):

        diff = differ.DiffContent.get_diff(self.content_orignal, self.content_new)

        self.assertEqual(
            differ.DiffContent.get_original(diff), 
            self.content_orignal
        )


