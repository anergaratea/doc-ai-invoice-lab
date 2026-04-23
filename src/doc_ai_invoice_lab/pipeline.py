from __future__ import annotations

import re
from pathlib import Path


SUPPLIER_RULES = {
    "Azure": "cloud",
    "Amazon Web Services": "cloud",
    "Iberdrola": "utilities",
    "Canon": "office",
    "Repsol": "fuel",
    "OpenAI Research Supplies": "software",
}


def extract(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else default


def classify_supplier(supplier: str) -> str:
    for keyword, category in SUPPLIER_RULES.items():
        if keyword.lower() in supplier.lower():
            return category
    return "other"


def parse_invoice_text(text: str) -> dict:
    supplier = extract(r"Supplier:\s*(.+)", text, "Unknown")
    amount_value = extract(r"Total:\s*([0-9]+(?:\.[0-9]{2})?)", text, "0")
    currency = extract(r"Currency:\s*([A-Z]{3})", text, "EUR")
    parsed = {
        "invoice_number": extract(r"Invoice Number:\s*(.+)", text, "missing"),
        "supplier": supplier,
        "invoice_date": extract(r"Invoice Date:\s*(.+)", text, "missing"),
        "total_amount": float(amount_value),
        "currency": currency,
        "category": classify_supplier(supplier),
    }
    parsed["validation_status"] = validate_record(parsed)
    return parsed


def validate_record(record: dict) -> str:
    required_fields = ["invoice_number", "supplier", "invoice_date"]
    if any(record[field] in {"missing", "Unknown", ""} for field in required_fields):
        return "needs_review"
    if record["total_amount"] <= 0:
        return "needs_review"
    return "valid"


def analyze_invoice_folder(folder: Path) -> tuple[list[dict], list[dict]]:
    records = []
    for path in sorted(folder.glob("*.txt")):
        record = parse_invoice_text(path.read_text(encoding="utf-8"))
        record["source_file"] = path.name
        records.append(record)

    total_docs = len(records)
    valid_docs = sum(1 for record in records if record["validation_status"] == "valid")
    completeness = sum(
        1 for record in records if all(record[field] not in {"missing", "Unknown", ""} for field in ["invoice_number", "supplier", "invoice_date"])
    )
    spend_by_category = {}
    for record in records:
        spend_by_category.setdefault(record["category"], 0.0)
        spend_by_category[record["category"]] += record["total_amount"]

    summary = [
        {"metric": "documents_processed", "value": total_docs},
        {"metric": "validation_pass_rate", "value": round(valid_docs / total_docs, 4) if total_docs else 0.0},
        {"metric": "extraction_completeness", "value": round(completeness / total_docs, 4) if total_docs else 0.0},
    ]
    for category, amount in sorted(spend_by_category.items()):
        summary.append({"metric": f"spend_{category}", "value": round(amount, 2)})

    return records, summary
