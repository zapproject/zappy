from default_tx import DefaultTx
import unittest

class DefaultTxTest(unittest.TestCase):
    def test_instance(self):
        defaultTx = DefaultTx("5555555555", 5, 51416566)
        self.assertEqual(defaultTx.address, "5555555555")
        self.assertEqual(defaultTx.gas, 5)
        self.assertEqual(defaultTx.gasPrice, 51416566)
