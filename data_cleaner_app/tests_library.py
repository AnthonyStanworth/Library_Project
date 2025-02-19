import unittest
import pandas as pd
from cleaner_app import enrichDates

class TestOps(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'startDate': pd.to_datetime(['2024-01-03', '2023-09-10','2025-06-01']),
                           'endDate': pd.to_datetime(['2024-01-02', '2023-09-15', '2025-06-03'])})
        self.errors = pd.DataFrame (columns=self.df.columns)

        self.cleaned_df, self.errors_df = enrichDates(self.df, 'startDate', 'endDate', self.errors)

    def test_length(self):
        self.assertEqual(len(self.cleaned_df), 2, "Cleaned df is wrong length")
        self.assertEqual(len(self.errors_df), 1, "Errors df is wrong length")

    def test_date_combos_in_right_df(self):
        self.assertTrue((self.cleaned_df['startDate'] < self.cleaned_df['endDate']).all(), "Cleaned contains invlaid loans")
        self.assertFalse((self.errors_df['startDate'] < self.errors_df['endDate']).all(), "Errors contains valid loans")

    def test_duration_is_int(self):
        self.assertTrue(pd.api.types.is_integer_dtype(self.cleaned_df['Loan Days']), "That is not an integer column")

    def test_duration_above_zero(self):
        self.assertTrue((self.cleaned_df['Loan Days'] > 0).all(), "Some duration values are less than 0.")
        
if __name__ == '__main__':
    unittest.main()