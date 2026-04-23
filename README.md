# Doc AI Invoice Lab

`Doc AI Invoice Lab` is an open-source portfolio project that demonstrates how to build a practical invoice-processing pipeline with transparent rules, validations and KPI reporting.

The repo focuses on an important real-world pattern: documents do not become useful just because you extract text from them. You need structured outputs, classification, validation and monitoring.

## What it shows

- invoice field extraction with regex-based parsers
- supplier and expense classification
- validation checks for operational quality
- portfolio-style KPI reporting
- an interactive Gradio dashboard

## Why this is portfolio-worthy

This project connects well with enterprise AI engineering because it turns a business workflow into a reproducible pipeline:

- ingestion
- extraction
- classification
- validation
- KPI analysis

## Repository structure

```text
doc-ai-invoice-lab/
├── app.py
├── requirements.txt
├── data/
│   └── invoices/
├── src/
│   └── doc_ai_invoice_lab/
└── tests/
```

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Example output

For every invoice, the pipeline produces:

- invoice number
- supplier
- invoice date
- total amount
- currency
- category
- validation status

The dashboard also aggregates:

- extraction completeness
- validation pass rate
- spend by supplier
- spend by category

## Design choices

- Uses synthetic sample invoices to make the repo self-contained
- Keeps the parser transparent and easy to explain in interviews
- Leaves room for future OCR or VLM integration

## Suggested next steps

- Add OCR ingestion for scanned PDFs
- Replace rules with transformer-based extraction
- Add confidence scores and human-in-the-loop review queues
- Export structured outputs to a database or API

## License

MIT
