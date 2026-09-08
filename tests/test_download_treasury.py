import unittest

from ingestion.download_treasury import calculate_page_count


class PageCountTests(unittest.TestCase):
    def test_complete_pages(self) -> None:
        self.assertEqual(calculate_page_count(2000, 1000), 2)

    def test_partial_final_page(self) -> None:
        self.assertEqual(calculate_page_count(72777, 1000), 73)


if __name__ == "__main__":
    unittest.main()