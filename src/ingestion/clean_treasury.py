"""Clean Bronze Treasury data for the Silver layer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

COLUMN_RENAMES = {
    "demarcation.code": "municipality_code",
    "demarcation.label": "municipality_name",
    "function.code": "function_code",
    "function.label": "function_name",
    "function.category_label": "function_category",
    "function.subcategory_label": "function_subcategory",
    "item.code": "item_code",
    "item.label": "item_name",
    "item.position_in_return_form": "item_position",
    "item.return_form_structure": "item_structure",
    "item.composition": "item_composition",
    "financial_year_end.year": "financial_year",
    "period_length.length": "period_length",
    "financial_period.period": "financial_period",
    "amount_type.code": "amount_type_code",
    "amount_type.label": "amount_type_name",
    "amount": "amount",
}

DEFAULT_INPUT = Path(
    "data/bronze/treasury_cpt_income_expenditure.json"
)

DEFAULT_OUTPUT = Path(
    "data/silver/treasury_cpt_income_expenditure.csv"
)

def load_bronze(input_path: Path) -> pd.DataFrame:
    """Load Treasury records from the Bronze JSON file."""
    with input_path.open(encoding="utf-8") as file:
        payload = json.load(file)

    records = payload.get("data")

    if not isinstance(records, list):
        raise TypeError("The Bronze JSON must contain a data list")

    return pd.DataFrame(records)

def clean_records(data: pd.DataFrame) -> pd.DataFrame:
    """Rename, standardise and validate Treasury records."""
    missing_columns = set(COLUMN_RENAMES) - set(data.columns)

    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(f"Required columns are missing: {missing_list}")

    cleaned = data.rename(columns=COLUMN_RENAMES).copy()

    text_columns = [
        "municipality_code",
        "municipality_name",
        "function_code",
        "function_name",
        "function_category",
        "function_subcategory",
        "item_code",
        "item_name",
        "item_structure",
        "item_composition",
        "period_length",
        "amount_type_code",
        "amount_type_name",
    ]

    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    integer_columns = [
        "item_position",
        "financial_year",
        "financial_period",
    ]

    for column in integer_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce",
        ).astype("Int64")

    cleaned["amount"] = pd.to_numeric(
        cleaned["amount"],
        errors="coerce",
    ).astype("Float64")

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    return cleaned

def save_silver(
    data: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save cleaned Treasury records as a Silver CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

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
    """Run the Bronze-to-Silver cleaning pipeline."""
    args = parse_args()

    bronze_data = load_bronze(args.input)
    silver_data = clean_records(bronze_data)
    save_silver(silver_data, args.output)

    print(f"Loaded {len(bronze_data)} Bronze records.")
    print(f"Saved {len(silver_data)} Silver records.")
    print(f"Silver data saved to {args.output}")


if __name__ == "__main__":
    main()

