import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.calculation = Calculator(8,2)
        
    def test_sum(self):
        self.assertEqual(self.calculation.do_sum(), 10, 'The sum is wrong')

    def test_minus(self):
        self.assertEqual(self.calculation.do_minus(), 6, 'The subtraction is wrong')

    def test_multiply(self):
        self.assertEqual(self.calculation.do_multiply(), 16, 'The multiplication is wrong')

    def test_divide(self):
        self.assertEqual(self.calculation.do_divide(), 4, 'The division is wrong')

if __name__ == '__main__':
    unittest.main()