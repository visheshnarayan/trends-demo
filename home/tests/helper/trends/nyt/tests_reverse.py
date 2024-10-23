
import unittest
from home.helper.trends.nyt.reverse import reverse_nyt

class TestReverseNyt(unittest.TestCase):
    def test_reverse_nyt(self):
        # run the function with test data
        result = reverse_nyt('race', 'healthcare', 'news')
        
        # expected result
        expected_result = ['NYT reports on healthcare', 'Healthcare in the news', 'NYT and healthcare']
        
        # assert that the result is as expected
        self.assertEqual(result, expected_result, f'Expected {expected_result}, but got {result}')