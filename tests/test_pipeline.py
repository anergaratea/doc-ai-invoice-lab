from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from doc_ai_invoice_lab.pipeline import parse_invoice_text


def test_parse_invoice_text_extracts_fields():
    text = """Invoice Number: INV-1
Supplier: Azure Cloud España
Invoice Date: 2026-01-08
Currency: EUR
Total: 100.50
"""
    record = parse_invoice_text(text)
    assert record["category"] == "cloud"
    assert record["validation_status"] == "valid"
