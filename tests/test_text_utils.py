import cracking_ciphers.text_utils as utils
import unittest

class TestPreprocessMethod(unittest.TestCase):
    def test_preprocess(self):
        inp = "Agz:fd,b s.df'asd' ' '  'aZ"
        out = "agzfdb sdfasd az"
        self.assertEqual(utils.preprocess_text(inp), out)

if __name__ == "__main__":
    unittest.main()

