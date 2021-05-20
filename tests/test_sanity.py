import unittest

class SanityCheck(unittest.TestCase):

    def test_sane(self):
        self.assertTrue(True)

    def test_flaw(self):
        self.assertNotEqual(42, 6*8)
        
