# Data card

One section like this for **every** dataset you use. Raw files larger than 50 MB are never committed; `scripts/download_data.py` recreates `data/raw/`. A filled-in example: https://github.com/BILGI-IE-421/demo-repository/blob/main/data/README.md

## Dataset 1: The Economist Big Mac Index (bigmac_clean.csv)
- **Source and URL:** The Economist, Big Mac Index, https://github.com/TheEconomist/big-mac-data.
- **License:** The source GitHub repository provides an MIT license. See its LICENCE file for the applicable terms.
- **Date accessed:** 20 October 2026
- **Time range and granularity:** April 2000 – July 2026. One observation per economy per Big Mac Index publication date. The dataset contains 45 editions covering 56 economies, including the United States.
- **Size:** 2,056 rows × 19 columns (raw index file, as recorded in the cleaning report); 2,056 rows × 9 columns (cleaned).
- **Columns used:** date (publication date), iso_a3 (economy identifier), name (economy name), currency_code (currency), local_price (local currency), dollar_ex (exchange rate), dollar_price (US dollars), USD_raw (valuation gap), flag_extreme_raw (extreme-value indicator).
- **Known issues:** The dataset has uneven historical publication intervals and varying economy coverage. Some economy names differ across editions. The index combines euro-area economies into a single observation. It also contains unusually large valuation gaps, which may influence average-based statistics.
- **Cleaning decisions and why:** Publication dates were parsed using a consistent ISO format. Economy names were standardized, and duplicate economy-date records were checked. No duplicate records required removal. Twelve extreme valuation observations were flagged but retained to avoid removing potentially meaningful economic events. GDP-adjusted and additional currency-specific indices were excluded because the research focuses on the raw USD-based valuation measure.
- **How to regenerate:** Run python scripts/download_data.py, followed by python scripts/preprocess.py --allow-ei-snapshot when using the documented historical Energy Institute snapshot. The Big Mac source is downloaded through the GitHub API, with a direct source-file fallback.

- ## Dataset 2: Brent Crude Oil Spot Prices (brent_daily.csv)
- **Source and URL:** U.S. Energy Information Administration (EIA), Europe Brent Spot Price FOB, https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls.
- **License:** U.S. government EIA data. Consult the EIA website's reuse and attribution guidance.
- **Date accessed:** 20 October 2026
- **Time range and granularity:** May 20, 1987 – November 11, 2026. One observation per reported trading day.
- **Size:** 9,128 rows × 2 columns in the recorded raw snapshot; 9,128 rows × 2 columns after cleaning.
- **Columns used:** date (trading date), brent_usd (US dollars per barrel).
- **Known issues:**Prices are not available for every calendar day because of non-trading days, holidays, and historical reporting interruptions. The recorded snapshot contains 94 gaps longer than five calendar days. Brent prices are an international benchmark and do not directly represent domestic oil prices in each economy.
- **Cleaning decisions and why:**Dates were standardized, and prices were converted to numeric values. Missing prices, duplicate dates, and non-positive values were checked. No observations required removal in the recorded snapshot. Missing trading days were not interpolated to avoid introducing synthetic price observations. For integration with the Big Mac Index, the average Brent price over the preceding 30 calendar days was calculated for each publication date.
- **How to regenerate:**Run python scripts/download_data.py to retrieve the original EIA Excel file, followed by python scripts/preprocess.py --allow-ei-snapshot when using the historical Energy Institute snapshot. The current download and preprocessing scripts use EIA as the sole Brent data provider.

## Dataset 3: Energy Institute Oil Production and Consumption (ei_oil_balance.csv)
- **Source and URL:** Energy Institute, Statistical Review of World Energy 2026, https://www.energyinst.org/statistical-review/resources-and-data-downloads.
- **License:** Energy Institute publication and reuse terms apply. A specific unrestricted open-data license has not been established for the PDF-derived and historical datasets.
- **Date accessed:** 20 October 2026
- **Time range and granularity:** The bundled historical processed dataset covers 1965–2025, with one observation per economy per year. The separately supplied 2026 PDF provides country and aggregate oil tables for 2015–2025.
- **Size:** Original historical workbook dimensions have not been independently verified. The bundled historical dataset contains 2,833 rows × 7 columns. The separately extracted PDF tables contain 69 production rows and 102 consumption rows, each with 11 annual value columns and two metadata columns.
- **Columns used:** iso_a3 (economy identifier), year (calendar year), production_kbd (thousand barrels per day), consumption_kbd (thousand barrels per day), production_listed (reported production indicator), net_exports_kbd (production minus consumption), oil_role (exporter/importer classification).
- **Known issues:** Not all economies are individually listed in the Energy Institute production tables. Smaller producers may be represented within regional aggregates. The historical snapshot sets production to zero for economies without a separately reported production record, which can lead to misclassification. The production-consumption balance is a proxy for net export status rather than a direct measurement of international oil trade. The supplied PDF does not contain the full 1965–2025 historical series.
- **Cleaning decisions and why:** Production and consumption data were reshaped into country-year observations and standardized using economy identifiers. The historical preparation procedure combined these measures, calculated production-minus-consumption balances, and classified economies as exporters or importers. An indicator was retained to distinguish individually reported production from assumed zero production. The euro-area series was constructed by aggregating available member-economy values for the relevant years.
The separate PDF-derived extraction follows a more conservative approach: missing production is treated as unknown rather than zero. It does not invent values for years before 2015. These alternative preparation methods are documented separately because they do not produce identical analytical coverage.
- **How to regenerate:** For the historical snapshot, run python scripts/download_data.py followed by python scripts/preprocess.py --allow-ei-snapshot. This reuses the committed historical Energy Institute CSV; it does not independently reconstruct the pre-2015 source data.
For PDF-based reconstruction, place the supplied 2026 Energy Institute PDF in data/raw/ or the supported references/ location. Then run python scripts/download_data.py followed by python scripts/preprocess.py --ei-source pdf. PDF extraction requires the "Poppler pdftotext" utility. This regenerates the available 2015–2025 oil data, not the full historical series.

## Dataset 4: Combined Big Mac and Oil Analysis Dataset (merged_dataset.csv)
- **Source and URL:** Derived by Data Pilgrims from three data sources: "The Economist Big Mac Index: https://github.com/TheEconomist/big-mac-data", "EIA Brent crude oil prices: https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls", "Energy Institute Statistical Review: https://www.energyinst.org/statistical-review/resources-and-data-downloads".
- **License:** Derived dataset incorporating material governed by the respective source terms.
- **Date accessed:** 20 October 2026
- **Time range and granularity:** April 2000 – July 2026. One observation per economy per Big Mac Index edition, excluding the United States as the reference economy.
- **Size:** 2,011 rows × 18 columns. The input datasets have different granularities and are joined rather than concatenated.
- **Columns used:** date (publication date), iso_a3 (economy identifier), name (economy name), currency_code (currency), local_price (local currency), dollar_ex (exchange rate), USD_raw (valuation gap), USD_raw_chg (valuation gap change), consecutive (consecutive edition indicator), flag_extreme_raw (extreme-value indicator), oil_role (exporter/importer classification), net_exports_kbd (oil balance), ei_year (reference year), brent_avg_30d (30-day average Brent price), brent_logchg_since_prev (Brent logarithmic change), months_since_prev (months between editions), brent_shock_size (standardized Brent movement), oil_regime (calm/high-movement classification).
- **Known issues:** The source datasets operate at different time resolutions: edition-based, daily, and annual. Oil-role coverage is incomplete for some economies. The current panel contains 198 observations without an oil-role classification, 74 without a Big Mac valuation-change measure, and 27 without a Brent interval-change measure. Earlier Energy Institute zero-production assumptions can influence exporter/importer comparisons. The relationships examined are observational and do not establish causation.
- **Cleaning decisions and why:** Big Mac observations provide the primary analytical timeline. The United States was excluded because its valuation gap is zero by construction. Brent prices were aggregated into 30-day averages and joined by publication date. Annual Energy Institute records were joined using economy identifiers and the previous calendar year to avoid incorporating future annual information.
Changes in Big Mac valuation gaps were calculated for economies appearing in consecutive editions. Brent movements were standardized to account approximately for differences between annual and semiannual intervals. Calm and high-movement intervals were distinguished using the median standardized absolute Brent change. Missing derived values were preserved rather than filled with invented observations.
The merged dataset was checked for duplicate economy-date identifiers; none were detected.
- **How to regenerate:** Run python scripts/download_data.py followed by python scripts/preprocess.py --allow-ei-snapshot to regenerate the analysis using newly downloaded Big Mac and EIA data together with the historical Energy Institute snapshot.
Alternatively, run python scripts/preprocess.py --ei-source pdf after downloading the other raw sources to construct a PDF-derived version with narrower oil-data coverage. The resulting panel may differ from the bundled historical snapshot.
The canonical output is data/merged_dataset.csv, with a JSON version at data/json/merged_dataset.json. Both are generated by the preprocessing pipeline.

## General Notes on Data Quality and Reproducibility

All date-only variables use the YYYY-MM-DD format. Since the analysis uses calendar dates rather than timestamps, no timezone conversion is applied.
The combined dataset preserves source-specific granularity through documented aggregation and matching rules.
The historical Energy Institute snapshot and the PDF-derived extraction are distinct source modes. Their results must not be described as interchangeable.
The data-cleaning and merging procedures are implemented in scripts/preprocess.py, while scripts/eda.ipynb documents the exploratory analysis.
The project investigates statistical associations between oil-market movements and Big Mac valuation gaps. Its findings should not be interpreted as direct causal effects.
