"""Download City of Cape Town financial facts from the Municipal Money API."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests

BASE_URL = "https://municipaldata.treasury.gov.za/api"
DEFAULT_CUBE = "incexp_v2"
DEFAULT_MUNICIPALITY = "CPT"
DEFAULT_PAGE_SIZE = 1000

def calculate_page_count(total_records: int, page_size: int) -> int:
    """Calculate how many API pages are required."""
    return math.ceil(total_records / page_size)

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

def download_pages(
    cube: str,
    municipality: str,
    page_size: int,
    max_pages: int,
) -> dict[str, Any]:
    """Download and combine multiple API pages."""
    first_url = build_url(cube, municipality, page=1, page_size=page_size)
    first_payload = fetch_json(first_url)

    total_records = int(first_payload.get("total_fact_count", 0))
    available_pages = calculate_page_count(total_records, page_size)
    pages_to_download = min(available_pages, max_pages)

    all_records = list(first_payload.get("data", []))

    for page_number in range(2, pages_to_download + 1):
        print(f"Downloading page {page_number} of {pages_to_download}...")
        page_url = build_url(
            cube,
            municipality,
            page=page_number,
            page_size=page_size,
        )
        page_payload = fetch_json(page_url)
        all_records.extend(page_payload.get("data", []))

    combined_payload = dict(first_payload)
    combined_payload["data"] = all_records
    combined_payload["downloaded_fact_count"] = len(all_records)
    combined_payload["downloaded_page_count"] = pages_to_download

    return combined_payload


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
    parser.add_argument(
    "--max-pages",
    type=int,
    default=1,
    help="Maximum number of API pages to download",
)
    return parser.parse_args()



def main() -> None:
    """Run the downloader."""
    args = parse_args()

    first_page_url = build_url(
        args.cube,
        args.municipality,
        page=1,
        page_size=args.page_size,
    )

    print("Starting Municipal Money download...")
    payload = download_pages(
        cube=args.cube,
        municipality=args.municipality,
        page_size=args.page_size,
        max_pages=args.max_pages,
    )

    save_download(payload, args.output, first_page_url)

    print(f"Downloaded {len(payload.get('data', []))} records.")
    print(f"Raw data saved to {args.output}")

if __name__ == "__main__":
    main()