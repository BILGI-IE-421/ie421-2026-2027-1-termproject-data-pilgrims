# AI usage statement

List every use of an AI assistant (ChatGPT, Claude, Copilot, Gemini, etc.) in this project. Every member must be able to explain all submitted code and figures.

| Date | Tool | Task (what you asked) | Where it is used (file/section) | What you verified and how |
|---|---|---|---|---|
| 2026-11-16 | Claude | Asked for an M2 implementation plan, source accessibility checks, and an explanation of differences between Big Mac datasets. | Planning; `data/README.md` | Compared the Big Mac files and identified differences caused by euro-area members, Croatia, and Venezuela. |
| 2026-11-16 | Claude | Requested scripts for downloading, cleaning, reshaping, and merging Big Mac, Brent, and Energy Institute data. | `scripts/download_data.py`, `scripts/preprocess.py` | Ran the original scripts in VS Code and compared output row counts with the cleaning report. |
| 2026-11-16 | Claude | Explored the 2014–2016 oil crash using Norway, Canada, Brazil, South Africa, and Japan. | Exploration only; not submitted | Results were not included in the repository. |
| 2026-11-16 | Claude | Investigated the FRED series and compared it with EIA Brent data. | Historical source investigation | Compared observations. FRED was subsequently removed from the active pipeline. |
| 2026-11-16 | Claude | Revised the merged analytical dataset, aligned variables with RQ1–RQ3, and added JSON exports. | `scripts/preprocess.py`, `data/` | Checked dataset columns, joins, and CSV/JSON record counts. |
| 2026-11-16 | Claude | Requested oil-market regime classification, GitHub API ingestion, EDA, and initial static figures. | `scripts/download_data.py`, `scripts/preprocess.py`, `scripts/eda.ipynb`, `scripts/figures.py` | Reviewed outputs against project requirements; the seasonality tests and API checksum were not independently repeated. |
| 2026-11-17 | Claude | Asked for explanations of Big Mac valuation distributions and exporter/importer comparisons. | `scripts/eda.ipynb`, `data/README.md` | Reviewed interpretations and identified a possible unusual Saudi Arabian price observation requiring verification. |
| 2026-11-18 | ChatGPT | Requested improvements to data preparation, validation, and reproducibility. | `scripts/download_data.py`, `scripts/preprocess.py` | Checked script structure and processed dataset dimensions; full original-source regeneration remains unverified. |
| 2026-11-18 | ChatGPT | Requested one canonical merged dataset and matching CSV/JSON exports. | `scripts/preprocess.py`, `data/merged_dataset.csv`, `data/json/` | Checked dataset dimensions, unique identifiers, and CSV/JSON record counts. |
| 2026-11-18 | ChatGPT | Redesigned figures using accessible colors, stronger annotations, and research-question-specific visualizations. | `scripts/figures.py`, `visuals/` | Regenerated and visually reviewed the three figures against course visualization principles. |
| 2026-11-18 | ChatGPT | Revised the EDA notebook to include missing-value analysis, distributions, temporal patterns, correlations, and sensitivity checks. | `scripts/eda.ipynb` | Executed the notebook and reviewed outputs and methodological explanations. |
| 2026-11-18 | ChatGPT | Integrated the revised notebook, three figures, and Energy Institute reference documentation into the project package. | `scripts/eda.ipynb`, `visuals/`, `README.md` | Checked the package structure and generated figures. |
| 2026-11-18 | ChatGPT | Removed FRED as an alternative Brent provider and retained EIA as the intended source. | `scripts/download_data.py`, `scripts/preprocess.py`, `scripts/figures.py` | Updated source references and checked syntax; a fresh EIA-only download remains unverified. |
| 2026-11-18 | ChatGPT | Extracted Energy Institute oil tables from the 2026 PDF and added a PDF-based preprocessing option. | `scripts/preprocess.py`, Energy Institute source data | Tested extraction structure; complete historical coverage before 2015 remains unverified. |
| 2026-11-18 | ChatGPT | Combined Energy Institute PDF extraction into `preprocess.py` to follow the required repository structure. | `scripts/preprocess.py` | Tested Python syntax and PDF extraction; complete regeneration remains unverified. |
| 2026-11-18 | ChatGPT | Drafted and formatted four data cards following the IE 421 template. | `data/README.md` | Reviewed descriptions, variables, data limitations, and regeneration instructions. |
| 2026-11-18 | ChatGPT | Prepared HTML for two static figures with interpretations and source descriptions. | `index.html` | Reviewed HTML structure and image paths; live GitHub Pages deployment remains unverified. |
| 2026-11-18 | ChatGPT | Revised the repository README, execution instructions, exploratory findings, and AI usage disclosure. | `README.md`, `AI_USAGE.md` | Reviewed content against project requirements and available outputs. |

Sections written entirely in our own words: data card, limitations, conclusions.
