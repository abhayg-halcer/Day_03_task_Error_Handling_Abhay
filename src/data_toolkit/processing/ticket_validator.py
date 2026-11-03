from datetime import datetime


ALLOWED_CATEGORIES = {
    "Billing", "Technical", "Account", "Delivery", "Product"
}

ALLOWED_PRIORITIES = {"Low", "Medium", "High", "Critical"}

ALLOWED_STATUSES = {"Open", "In Progress", "Resolved", "Closed"}


def validate_ticket_row(row: dict) -> list[dict]:
    """
    Validate one raw CSV ticket row.
    Return a list of detected data-quality issues.
    """
    issues = []

    ticket_id = row.get("ticket_id", "").strip()

    if not ticket_id:
        issues.append({
            "field": "ticket_id",
            "issue": "missing_ticket_id"
        })

    if not row.get("customer_id", "").strip():
        issues.append({
            "field": "customer_id",
            "issue": "missing_customer_id"
        })

    if row.get("category", "").strip() not in ALLOWED_CATEGORIES:
        issues.append({
            "field": "category",
            "issue": "invalid_or_missing_category"
        })

    if row.get("priority", "").strip() not in ALLOWED_PRIORITIES:
        issues.append({
            "field": "priority",
            "issue": "invalid_priority"
        })

    if row.get("status", "").strip() not in ALLOWED_STATUSES:
        issues.append({
            "field": "status",
            "issue": "invalid_status"
        })

    try:
        datetime.fromisoformat(row.get("created_at", "").strip())
    except ValueError:
        issues.append({
            "field": "created_at",
            "issue": "invalid_date"
        })

    duration = row.get("resolution_time_hours", "").strip()

    if duration:
        try:
            duration_value = float(duration)

            if duration_value < 0:
                issues.append({
                    "field": "resolution_time_hours",
                    "issue": "negative_duration"
                })
        except ValueError:
            issues.append({
                "field": "resolution_time_hours",
                "issue": "invalid_duration"
            })

    rating = row.get("customer_rating", "").strip()

    if rating:
        try:
            rating_value = int(rating)

            if not 1 <= rating_value <= 5:
                issues.append({
                    "field": "customer_rating",
                    "issue": "invalid_rating"
                })
        except ValueError:
            issues.append({
                "field": "customer_rating",
                "issue": "invalid_rating"
            })

    if not row.get("description", "").strip():
        issues.append({
            "field": "description",
            "issue": "blank_description"
        })

    return issues