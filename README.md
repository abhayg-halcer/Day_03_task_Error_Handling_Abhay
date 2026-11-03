# Customer Support Ticket Data Pipeline

A modular Python CLI application for loading, validating, cleaning, and analyzing customer support ticket CSV data.

## Features
- CSV loading with file and schema error handling.
- Duplicate normalized header detection.
- Ticket validation and data-quality reporting.
- Duplicate ticket ID detection.
- Optional customer rating normalization.
- Ticket analytics and SLA breach analysis.
- CSV report generation, structured exceptions, and application logging.

## Setup
Requires Python 3.10 or newer.
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

## Usage
```bash
python3 -m data_toolkit.cli data/tickets.csv --output-dir outputs
```

## Ticket CSV Schema
`ticket_id`, `customer_id`, `category`, `priority`, `status`, `created_at`, `resolution_time_hours`, `customer_rating`, `description`

## Validation Rules
- Ticket and customer IDs must be present.
- Category, priority, and status must use supported values.
- Creation dates must be valid datetimes.
- Resolution time must be numeric and non-negative.
- Resolved and closed tickets require a resolution time.
- Open and in-progress tickets must not have a resolution time.
- Customer ratings are optional; invalid ratings are normalized and reported.
- The first occurrence of a duplicate ticket ID is retained.
- Duplicate CSV headers after trimming and case normalization are rejected.

## SLA Thresholds
| Priority | Resolution target |
|---|---:|
| Critical | 4 hours |
| High | 8 hours |
| Medium | 24 hours |
| Low | 72 hours |

## Generated Reports
- `data_quality_report.csv`
- `summary_metrics.csv`
- `sla_breach_by_priority.csv`

## Logging
Application logs are written to `logs/app.log`.

## Tests
```bash
python3 -m pytest -v
python3 -m pytest --cov=data_toolkit --cov-report=term-missing
```
