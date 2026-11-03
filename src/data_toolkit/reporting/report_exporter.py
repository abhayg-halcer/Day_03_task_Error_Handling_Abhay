import csv
from pathlib import Path


def export_report(
    records: list[dict],
    output_file: str | Path,
) -> None:
    """
    Export a list of dictionaries to a CSV report.
    """
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not records:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(records[0].keys())

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def export_summary(
    summary: dict,
    output_file: str | Path,
) -> None:
    """
    Export summary metrics into a two-column CSV.
    """
    records = []

    records.append({
        "metric": "total_tickets",
        "value": summary["total_tickets"],
    })

    records.append({
        "metric": "average_resolution_hours",
        "value": summary["average_resolution_hours"],
    })

    for status, count in summary["status_counts"].items():
        records.append({
            "metric": f"status_{status}",
            "value": count,
        })

    for priority, count in summary["priority_counts"].items():
        records.append({
            "metric": f"priority_{priority}",
            "value": count,
        })

    export_report(records, output_file)