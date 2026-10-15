"""Small, testable helpers for JomiCheck Lite.

This file contains plain Python only so beginners can test the search and warning
rules without starting the Streamlit interface.
"""

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).parent / "data" / "plots.json"


def load_records(path: Path | str = DATA_FILE) -> list[dict[str, Any]]:
    """Read fictional plot/deed records from a JSON file."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)
    if not isinstance(records, list):
        raise ValueError("The JSON data must contain a list of records.")
    required_fields = {
        "plot_id", "deed_id", "owner_name", "area_decimal", "location",
        "registration_date", "mutation_status", "acquisition_status",
        "pending_cases", "deed_status", "ownership_history",
    }
    for index, record in enumerate(records):
        missing = required_fields.difference(record)
        if missing:
            raise ValueError(f"Record {index + 1} is missing fields: {', '.join(sorted(missing))}")
    return records


def find_plot_records(records: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    """Find records by exact plot ID or deed ID, ignoring letter case.

    A deed lookup returns all deed entries for that plot, so conflicts are visible.
    """
    term = query.strip().casefold()
    if not term:
        return []

    plot_matches = [record for record in records if record["plot_id"].casefold() == term]
    if plot_matches:
        plot_id = plot_matches[0]["plot_id"]
        return sorted(
            [record for record in records if record["plot_id"] == plot_id],
            key=lambda record: (record["registration_date"], record["deed_id"]),
        )

    deed_match = next(
        (record for record in records if record["deed_id"].casefold() == term),
        None,
    )
    if deed_match is None:
        return []

    plot_id = deed_match["plot_id"]
    return sorted(
        [record for record in records if record["plot_id"] == plot_id],
        key=lambda record: (record["registration_date"], record["deed_id"]),
    )


def get_warnings(plot_records: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Apply transparent, rule-based checks to records for one plot.

    These flags are only demo indicators. They do not establish fraud or legal status.
    """
    if not plot_records:
        return []

    warnings: list[dict[str, str]] = []
    unique_records = {record["deed_id"]: record for record in plot_records}.values()
    records_list = list(unique_records)

    active_records = [
        record for record in records_list
        if str(record["deed_status"]).casefold() == "active"
    ]
    if len(active_records) > 1:
        descriptions = "; ".join(
            f"{record['deed_id']} ({record['owner_name']})" for record in active_records
        )
        warnings.append({
            "code": "active_deed_conflict",
            "title": "Multiple active deeds for one plot",
            "message": (
                f"These records are all marked Active for the same plot: {descriptions}. "
                "The prototype cannot determine which record is correct; compare the records "
                "and request official review."
            ),
        })

    for record in records_list:
        mutation_status = str(record["mutation_status"]).strip()
        if mutation_status.casefold() != "completed":
            warnings.append({
                "code": "mutation_not_completed",
                "title": f"Mutation not completed — {record['deed_id']}",
                "message": (
                    f"The demo record lists mutation as '{mutation_status}'. "
                    "Check the official mutation record before relying on this information."
                ),
            })

        cases = record.get("pending_cases", [])
        if cases:
            case_text = "; ".join(str(case) for case in cases)
            warnings.append({
                "code": "pending_case",
                "title": f"Listed case or dispute — {record['deed_id']}",
                "message": (
                    f"The demo data lists: {case_text}. This is a fictional flag and must be "
                    "checked against authoritative records."
                ),
            })

        acquisition_status = str(record.get("acquisition_status", "Clear")).strip()
        if acquisition_status.casefold() != "clear":
            warnings.append({
                "code": "acquisition_flag",
                "title": f"Acquisition status needs review — {record['deed_id']}",
                "message": (
                    f"The demo record shows acquisition status '{acquisition_status}'. "
                    "Confirm the status with an authorized source."
                ),
            })

        deed_status = str(record.get("deed_status", "Active")).strip()
        if deed_status.casefold() != "active":
            warnings.append({
                "code": "deed_not_active",
                "title": f"Deed is not marked Active — {record['deed_id']}",
                "message": (
                    f"This record's deed status is '{deed_status}'. It should not be treated as "
                    "a currently active deed in this prototype."
                ),
            })

    return warnings


def get_unique_plot_ids(records: list[dict[str, Any]]) -> list[str]:
    """Return the unique plot IDs in sorted order."""
    return sorted({record["plot_id"] for record in records})
