from pathlib import Path
import sys

import gradio as gr
import pandas as pd

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from doc_ai_invoice_lab.pipeline import analyze_invoice_folder, parse_invoice_text


INVOICES_DIR = ROOT / "data" / "invoices"


def analyze_folder():
    records, summary = analyze_invoice_folder(INVOICES_DIR)
    return pd.DataFrame(records), pd.DataFrame(summary)


def inspect_invoice(text: str):
    return pd.DataFrame([parse_invoice_text(text)])


example_invoice = (INVOICES_DIR / "invoice_001.txt").read_text(encoding="utf-8")

with gr.Blocks(title="Doc AI Invoice Lab") as demo:
    gr.Markdown(
        """
        # Doc AI Invoice Lab
        Parse invoice-like documents, validate fields and inspect KPI summaries.
        """
    )
    with gr.Tab("Batch Analysis"):
        batch_button = gr.Button("Analyze Sample Folder", variant="primary")
        batch_records = gr.Dataframe(label="Parsed invoices")
        batch_summary = gr.Dataframe(label="KPIs")
        batch_button.click(analyze_folder, outputs=[batch_records, batch_summary])

    with gr.Tab("Single Invoice"):
        invoice_text = gr.Textbox(label="Invoice text", value=example_invoice, lines=16)
        inspect_button = gr.Button("Parse Invoice", variant="primary")
        inspect_output = gr.Dataframe(label="Structured output")
        inspect_button.click(inspect_invoice, inputs=[invoice_text], outputs=[inspect_output])


if __name__ == "__main__":
    demo.launch()
