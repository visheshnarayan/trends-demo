
import unittest
from home.helper.trends.healthcare.reverse import reverse_healthcare

class TestReverseNyt(unittest.TestCase):
    def test_reverse_healthcare(self):
        # run the function with test data
        result = reverse_healthcare('disease', 'healthcare', 'news')
        
        # expected result
        expected_result = ['NYT reports on healthcare', 'Healthcare in the news', 'NYT and healthcare']
        
        # assert that the result is as expected
        self.assertEqual(result, expected_result, f'Expected {expected_result}, but got {result}')