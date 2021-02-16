import unittest
from utils import read_blocks, get_block_value, get_block_timediff, get_block_size, get_block_tx


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading dataset")
        cls._df = read_blocks('../data/blocks.json')

    def test_num_txs(self):
        print("Starting test_number_txs")
        self.assertEqual(self._df.loc[0, "num_tx"], 2650)
        self.assertEqual(self._df.loc[143, "num_tx"], 2392)
        self.assertTrue(self._df.shape[0] == 144)
        self.assertTrue(self._df.shape[1] == 4)

    def test_block_value(self):
        print("Starting test_block_value")
        block_value = get_block_value('../data/txs.json')
        self.assertAlmostEqual(block_value.loc[0, "value"], 11383.948788, 3)
        self.assertAlmostEqual(block_value.loc[143, "value"], 11012.551104, 3)
        self.assertTrue(block_value.shape[0] == 144)
        self.assertTrue(block_value.shape[1] == 2)

    def test_block_timediff(self):
        print("Starting test_block_timediff")
        block_timediff = get_block_timediff(self._df)
        self.assertEqual(block_timediff.loc[1, "timediff_sec"], 1612.0)
        self.assertEqual(block_timediff.loc[143, "timediff_sec"], 701.0)
        self.assertTrue(block_timediff.shape[0] == 144)
        self.assertTrue(block_timediff.shape[1] == 3)

    def test_block_avgsize(self):
        print("Starting test_block_avgsize")
        block_avgsize = get_block_size(self._df)
        self.assertAlmostEqual(block_avgsize.loc[0, "size"], 1.387607e+06, 0)
        self.assertAlmostEqual(block_avgsize.loc[26, "size"], 1.215300e+06, 0)
        self.assertTrue(block_avgsize.shape[0] == 27)
        self.assertTrue(block_avgsize.shape[1] == 2)

    def test_block_tx(self):
        print("Starting test_block_tx")
        block_tx = get_block_tx(self._df)
        self.assertEqual(block_tx.loc[0, "num_tx"], 2760)
        self.assertEqual(block_tx.loc[26, "num_tx"], 13412)
        self.assertTrue(block_tx.shape[0] == 27)
        self.assertTrue(block_tx.shape[1] == 2)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestData))
unittest.TextTestRunner(verbosity=2).run(suite)
