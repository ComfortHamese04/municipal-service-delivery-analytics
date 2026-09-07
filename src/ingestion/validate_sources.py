"""Validate configured source endpoints and write a reproducible run manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CheckResult:
    source_id: str
    url: str
    checked_at_utc: str
    reachable: bool
    status_code: int | None
    content_type: str | None
    content_length: int
    sha256_prefix: str | None
    error: str | None


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload.get("sources"), list):
       raise TypeError("Configuration must contain a 'sources' list")
    return payload


def check_source(source: dict[str, Any], timeout: int = 30) -> CheckResult:
    source_id = str(source["id"])
    url = str(source["healthcheck_url"])
    checked_at = datetime.now(UTC).isoformat()
    user_agent = os.getenv(
        "HTTP_USER_AGENT", "municipal-service-delivery-analytics/0.1"
    )
    request = Request(url, headers={"User-Agent": user_agent})

    try:
        with urlopen(request, timeout=timeout) as response:
            sample = response.read(65_536)
            return CheckResult(
                source_id=source_id,
                url=url,
                checked_at_utc=checked_at,
                reachable=True,
                status_code=response.status,
                content_type=response.headers.get("Content-Type"),
                content_length=len(sample),
                sha256_prefix=hashlib.sha256(sample).hexdigest()[:16],
                error=None,
            )
    except HTTPError as error:
        return CheckResult(
            source_id, url, checked_at, False, error.code, None, 0, None, str(error)
        )
    except (URLError, TimeoutError) as error:
        return CheckResult(
            source_id, url, checked_at, False, None, None, 0, None, str(error)
        )


def validate(config_path: Path, output_dir: Path, timeout: int) -> Path:
    config = load_config(config_path)
    results = [check_source(source, timeout) for source in config["sources"]]
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    destination = output_dir / f"source_validation_{timestamp}.json"
    manifest = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "config": str(config_path),
        "results": [asdict(result) for result in results],
    }
    destination.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/metadata"))
    parser.add_argument(
        "--timeout", type=int, default=int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destination = validate(args.config, args.output, args.timeout)
    print(f"Validation manifest written to {destination}")


if __name__ == "__main__":
    main()
