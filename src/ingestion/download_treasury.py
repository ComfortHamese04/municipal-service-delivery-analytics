"""Download City of Cape Town financial facts from the Municipal Money API."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests

BASE_URL = "https://municipaldata.treasury.gov.za/api"
DEFAULT_CUBE = "incexp_v2"
DEFAULT_MUNICIPALITY = "CPT"
DEFAULT_PAGE_SIZE = 1000


def build_url(
    cube: str,
    municipality: str,
    page: int,
    page_size: int,
) -> str:
    """Build a filtered and paginated Municipal Money API URL."""
    parameters = {
        "cut": f'demarcation.code:"{municipality}"',
        "page": page,
        "pagesize": page_size,
    }
    return f"{BASE_URL}/cubes/{cube}/facts?{urlencode(parameters)}"


def fetch_json(url: str) -> dict[str, Any]:
    """Request JSON data from the API."""
    response = requests.get(
        url,
        headers={"User-Agent": "municipal-service-delivery-analytics/0.1"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def save_download(payload: dict[str, Any], output_path: Path, url: str) -> None:
    """Save the raw response and its ingestion metadata."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_bytes = json.dumps(payload, indent=2).encode("utf-8")
    output_path.write_bytes(json_bytes)

    manifest = {
        "source_url": url,
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "file_path": str(output_path),
        "file_size_bytes": len(json_bytes),
        "sha256": hashlib.sha256(json_bytes).hexdigest(),
        "record_count": len(payload.get("data", [])),
        "total_fact_count": payload.get("total_fact_count"),
    }

    manifest_path = output_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Read the command-line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cube", default=DEFAULT_CUBE)
    parser.add_argument("--municipality", default=DEFAULT_MUNICIPALITY)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/bronze/treasury_cpt_income_expenditure.json"),
    )
    return parser.parse_args()


def main() -> None:
    """Run the downloader."""
    args = parse_args()
    url = build_url(args.cube, args.municipality, args.page, args.page_size)

    print(f"Downloading page {args.page} from Municipal Money...")
    payload = fetch_json(url)
    save_download(payload, args.output, url)

    print(f"Downloaded {len(payload.get('data', []))} records.")
    print(f"Raw data saved to {args.output}")


if __name__ == "__main__":
    main()