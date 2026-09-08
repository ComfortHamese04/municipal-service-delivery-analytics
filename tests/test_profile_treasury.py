import unittest

import pandas as pd

from analysis.profile_treasury import create_profile


class TreasuryProfileTests(unittest.TestCase):
    def test_create_profile(self) -> None:
        data = pd.DataFrame(
            [
                {
                    "financial_year_end.year": 2024,
                    "demarcation.code": "CPT",
                    "amount_type.code": "AUDA",
                    "amount": 100,
                },
                {
                    "financial_year_end.year": 2025,
                    "demarcation.code": "CPT",
                    "amount_type.code": "ACT",
                    "amount": None,
                },
            ]
        )

        profile = create_profile(data)

        self.assertEqual(profile["row_count"], 2)
        self.assertEqual(profile["column_count"], 4)
        self.assertEqual(profile["duplicate_row_count"], 0)
        self.assertEqual(profile["missing_values"]["amount"], 1)
        self.assertEqual(profile["financial_year_min"], 2024)
        self.assertEqual(profile["financial_year_max"], 2025)
        self.assertEqual(profile["municipality_codes"], ["CPT"])


if __name__ == "__main__":
    unittest.main()