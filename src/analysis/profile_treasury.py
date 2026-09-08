"""Profile downloaded Municipal Money records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

DEFAULT_INPUT = Path(
    "data/bronze/treasury_cpt_income_expenditure.json"
)
DEFAULT_OUTPUT = Path(
    "data/metadata/treasury_cpt_profile.json"
)

def load_records(input_path: Path) -> pd.DataFrame:
    """Load API records from a Bronze JSON file."""
    with input_path.open(encoding="utf-8") as file:
        payload = json.load(file)

    records = payload.get("data")

    if not isinstance(records, list):
        raise TypeError("The JSON payload must contain a data list")

    return pd.DataFrame(records)
def create_profile(data: pd.DataFrame) -> dict[str, object]:
    """Calculate basic data-quality and coverage statistics."""
    financial_years = pd.to_numeric(
        data["financial_year_end.year"],
        errors="coerce",
    )

    amounts = pd.to_numeric(
        data["amount"],
        errors="coerce",
    )

    return {
        "row_count": len(data),
        "column_count": len(data.columns),
        "duplicate_row_count": int(data.duplicated().sum()),
        "missing_values": {
            column: int(count)
            for column, count in data.isna().sum().items()
        },
        "financial_year_min": int(financial_years.min()),
        "financial_year_max": int(financial_years.max()),
        "municipality_codes": sorted(
            data["demarcation.code"].dropna().unique().tolist()
        ),
        "amount_types": sorted(
            data["amount_type.code"].dropna().unique().tolist()
        ),
        "amount_min": float(amounts.min()),
        "amount_max": float(amounts.max()),
    }

def save_profile(
    profile: dict[str, object],
    output_path: Path,
) -> None:
    """Save the profiling results as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(profile, indent=2),
        encoding="utf-8",                                                                                                                                                                                                             
    )

def parse_args() -> argparse.Namespace:
    """Read command-line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    return parser.parse_args()


def main() -> None:
    """Run the Treasury data profiler."""
    args = parse_args()
    data = load_records(args.input)
    profile = create_profile(data)
    save_profile(profile, args.output)

    print(f"Profiled {profile['row_count']} records.")
    print(f"Profile saved to {args.output}")


if __name__ == "__main__":
    main()
    