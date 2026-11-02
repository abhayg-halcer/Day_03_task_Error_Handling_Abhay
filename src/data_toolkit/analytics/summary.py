"""Sales analytics and summary calculations."""

from data_toolkit.models.record import Record


def generate_summary(records: list[Record]) -> dict[str, int | float | str]:
    """Generate a summary of sales records."""
    if not records:
        return {
            "total_records": 0,
            "total_quantity": 0,
            "total_sales": 0.0,
            "average_sale": 0.0,
            "best_selling_product": "N/A",
        }

    total_quantity = sum(record.quantity for record in records)
    total_sales = round(sum(record.total for record in records), 2)

    quantities_by_product: dict[str, int] = {}

    for record in records:
        quantities_by_product[record.product] = (
            quantities_by_product.get(record.product, 0) + record.quantity
        )

    best_selling_product = max(
        quantities_by_product,
        key=quantities_by_product.get,
    )

    return {
        "total_records": len(records),
        "total_quantity": total_quantity,
        "total_sales": total_sales,
        "average_sale": round(total_sales / len(records), 2),
        "best_selling_product": best_selling_product,
    }
