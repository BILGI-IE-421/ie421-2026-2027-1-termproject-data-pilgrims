"""Recreate 2015–2025 oil table extracts from the included Energy Institute PDF.

Prerequisite: poppler's `pdftotext` executable must be installed. The PDF's
printed pages 31 (production) and 36 (consumption) correspond to PDF pages
32 and 37. The extracted table values are *not* inferred for other years.

Usage:
    python scripts/extract_ei_pdf.py

Outputs:
    data/ei_pdf_2026/EI_2026_production.csv
    data/ei_pdf_2026/EI_2026_consumption.csv
    data/ei_pdf_2026/EI_2026_extracted_data.json
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "references" / "EI_Statistical_Review_2026.pdf"
OUTPUT = ROOT / "data" / "ei_pdf_2026"
YEARS = list(range(2015, 2026))


def extract_table(page_text: str, series: str) -> list[dict]:
    """Parse printed table cells; use None for source dashes rather than invented zeros."""
    rows: list[dict] = []
    for line in page_text.splitlines():
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) < 12:
            continue
        entity, values = parts[0], parts[1:12]
        if not entity or entity.startswith(("Thousand", "Back to", "Growth", "*", "Note")):
            continue
        if not all(re.fullmatch(r"[\d,]+|[–—-]", value) for value in values):
            continue
        aggregate = (entity.startswith(("Total ", "Other ", "Eastern Africa", "Western Africa", "Middle Africa"))
                     or entity in {"World", "Non-OECD", "OECD", "EU", "Europe", "Africa"})
        row = {"entity": entity, "series": series, "is_aggregate": aggregate}
        for year, value in zip(YEARS, values):
            row[str(year)] = None if value in {"–", "—", "-"} else int(value.replace(",", ""))
        rows.append(row)
    return rows


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(f"Required Energy Institute PDF not found: {PDF}")
    if not shutil.which("pdftotext"):
        raise RuntimeError("Install Poppler / pdftotext to regenerate PDF tables; pre-extracted CSVs are bundled.")
    result = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], check=True,
                            capture_output=True, text=True)
    pages = result.stdout.split("\f")
    production = extract_table(pages[31], "production_kbd")
    consumption = extract_table(pages[36], "consumption_kbd")
    if not (len(production) == 69 and len(consumption) == 102):
        raise ValueError(f"Unexpected table dimensions: production={len(production)}, consumption={len(consumption)}")
    for name, rows in (("production", production), ("consumption", consumption)):
        world = [row for row in rows if row["entity"] == "Total World"]
        if len(world) != 1 or world[0]["2025"] is None:
            raise ValueError(f"Missing published world total in {name} table")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, rows in (("production", production), ("consumption", consumption)):
        path = OUTPUT / f"EI_2026_{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["entity", "is_aggregate"] + list(map(str, YEARS)))
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k) for k in writer.fieldnames})
    payload = {"source_pdf": PDF.name, "year_range": [2015, 2025],
               "unit": "thousand barrels per day", "production": production, "consumption": consumption}
    (OUTPUT / "EI_2026_extracted_data.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Extracted {len(production)} production rows and {len(consumption)} consumption rows (2015–2025).")


if __name__ == "__main__":
    main()
