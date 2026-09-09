import unittest

import pandas as pd

from ingestion.clean_treasury import COLUMN_RENAMES, clean_records


class TreasuryCleaningTests(unittest.TestCase):
    def test_clean_records(self) -> None:
        row = {
            column: "Example"
            for column in COLUMN_RENAMES
        }

        row.update(
            {
                "demarcation.code": " CPT ",
                "item.code": "0700",
                "item.position_in_return_form": "6",
                "financial_year_end.year": "2025",
                "financial_period.period": "1",
                "amount": "7808.50",
            }
        )

        data = pd.DataFrame([row, row])
        cleaned = clean_records(data)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.loc[0, "municipality_code"], "CPT")
        self.assertEqual(cleaned.loc[0, "item_code"], "0700")
        self.assertEqual(cleaned.loc[0, "financial_year"], 2025)
        self.assertEqual(cleaned.loc[0, "amount"], 7808.50)


if __name__ == "__main__":
    unittest.main()