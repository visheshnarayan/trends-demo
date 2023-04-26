import unittest
from home.helper.transform import reverse_doc

class TestReverseDoc(unittest.TestCase):
    def test_reverse_doc(self):
        strs = ["This is a test", "Another test"]
        base = "test"
        rel1 = "is"
        rel2 = "another"
        
        result = reverse_doc(strs, base, rel1, rel2)
        
        expected_result = [
            (strs[0], [3, 1, -1]), 
            (strs[1], [1, -1, 0])
        ]
        
        self.assertEqual(result, expected_result)