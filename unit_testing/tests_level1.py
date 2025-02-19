import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calculation = Calculator(8,2)
        self.assertEqual(calculation.do_sum(), 10, 'The sum is wrong')

    def test_minus(self):
        calculation = Calculator(8,2)
        self.assertEqual(calculation.do_minus(), 6, 'The subtraction is wrong')

    def test_multiply(self):
        calculation = Calculator(8,2)
        self.assertEqual(calculation.do_multiply(), 16, 'The multiplication is wrong')

    def test_divide(self):
        calculation = Calculator(8,2)
        self.assertEqual(calculation.do_divide(), 4, 'The division is wrong')

if __name__ == '__main__':
    unittest.main()