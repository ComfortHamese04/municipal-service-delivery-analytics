import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ingestion.validate_sources import load_config


class LoadConfigTests(unittest.TestCase):
    def test_load_config_accepts_sources_list(self) -> None:
        with TemporaryDirectory() as directory:
            config = Path(directory) / "sources.json"
            config.write_text(
                json.dumps({"sources": [{"id": "example"}]}), encoding="utf-8"
            )

            self.assertEqual(load_config(config)["sources"][0]["id"], "example")

    def test_load_config_rejects_missing_sources(self) -> None:
        with TemporaryDirectory() as directory:
            config = Path(directory) / "sources.json"
            config.write_text("{}", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "sources"):
                load_config(config)


if __name__ == "__main__":
    unittest.main()
