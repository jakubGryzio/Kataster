import unittest
import main

class TestSyntaxValidator(unittest.TestCase):

    def test_reader(self):
        self.assertEqual(len(main.reader()), 194)

    def test_backSlashContainer(self):
        self.assertTrue(main.containsBackSlash("ergihreigoer/eijgerojg"))
        self.assertTrue(main.containsBackSlash("/"))
        self.assertTrue(main.containsBackSlash("regre/"))
        self.assertFalse(main.containsBackSlash("//"))
        self.assertFalse(main.containsBackSlash(""))

    def test_matchDigitsBefore(self):
        self.assertTrue(main.matchDigitsBeforeBackSlash("22-234/"))
        self.assertTrue(main.matchDigitsBeforeBackSlash("2-234/"))
        self.assertTrue(main.matchDigitsBeforeBackSlash("2-2/"))
        self.assertTrue(main.matchDigitsBeforeBackSlash("2-23456789/"))
        self.assertTrue(main.matchDigitsBeforeBackSlash("23-2345/"))
        self.assertFalse(main.matchDigitsBeforeBackSlash("23a-2345/"))
        self.assertFalse(main.matchDigitsBeforeBackSlash("a-2345/"))
        self.assertFalse(main.matchDigitsBeforeBackSlash("a - 2345/"))
        self.assertFalse(main.matchDigitsBeforeBackSlash("a 345/"))
        self.assertFalse(main.matchDigitsBeforeBackSlash(""))

    def test_OFUChecker(self):
        self.assertTrue(main.isOFU("/R"))
        self.assertTrue(main.isOFU("/Wsr"))
        self.assertTrue(main.isOFU("/Ti"))
        self.assertFalse(main.isOFU("Ti"))
        self.assertFalse(main.isOFU("/Ksrsfa"))
        self.assertFalse(main.isOFU("/123"))
        self.assertFalse(main.isOFU("11245"))
        self.assertTrue(main.isOFU("/Ksr R"))
        self.assertFalse(main.isOFU("23-456/Ksr/R"))

if __name__ == "__main__":
    unittest.main()
