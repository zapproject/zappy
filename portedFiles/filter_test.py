from filter import Filter
import unittest

class TestFilter(unittest.TestCase):
    def test_instance(self):
        filterTest = Filter(11, 22, "123123123", "321321321", "221221221", "11111", 123)
        self.assertEqual(filterTest.fromBlock, 11)
        self.assertEqual(filterTest.toBlock, 22)
        self.assertEqual(filterTest.provider, "123123123")
        self.assertEqual(filterTest.subscriber, "321321321")
        self.assertEqual(filterTest.terminator, "221221221")
        self.assertEqual(filterTest.endpoint, "11111")
        self.assertEqual(filterTest.id, 123)
